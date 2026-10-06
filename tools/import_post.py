"""Import a CPS unchanged and start a draft machine intake; never approve a post."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 32 * 1024 * 1024
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
FILE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.cps\Z", re.I)
HEADER = "| Base ID | Đường dẫn | Revision | URL nguồn | Tệp/URL đầu vào | Ngày lấy | SHA-256 | Engine tối thiểu | License/điều kiện | Máy sử dụng |"
SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"


def safe_id(value: str) -> str:
    if not ID_PATTERN.fullmatch(value) or ".." in value or value.upper() == "UNKNOWN":
        raise ValueError(f"ID/revision không hợp lệ: {value!r}")
    return value


def clean(value: str) -> str:
    if any(ch in value for ch in "|\r\n") or any(ord(ch) < 32 for ch in value):
        raise ValueError("Dữ liệu nhập không được chứa | hoặc ký tự điều khiển.")
    return value


def ask(label: str, default: str | None = "UNKNOWN") -> str:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        value = clean(input(f"{label}{suffix}: ").strip())
        if value:
            return value
        if default is not None:
            return default
            print("Trường này bắt buộc.")


def read_source(source: str) -> tuple[str, bytes, str]:
    """Read a local CPS or HTTPS CPS (including HTTPS redirects only)."""
    if source.lower().startswith(("http://", "https://")):
        if not source.lower().startswith("https://"):
            raise ValueError("Chỉ chấp nhận URL HTTPS; tải thủ công nếu nguồn là HTTP.")
        if urlsplit(source).query or urlsplit(source).fragment:
            raise ValueError("Không nhập URL chứa query/fragment/token; hãy tải file rồi dùng đường dẫn local.")
        name = unquote(Path(urlsplit(source).path).name)
        with urlopen(source, timeout=20) as response:
            final_url = urlsplit(response.geturl())
            if final_url.scheme.lower() != "https" or final_url.query or final_url.fragment:
                raise ValueError("URL chuyển hướng không hợp lệ; chỉ chấp nhận HTTPS không chứa query/token.")
            data = response.read(MAX_BYTES + 1)
    else:
        if "://" in source:
            raise ValueError("Chỉ hỗ trợ tệp local hoặc URL HTTPS.")
        path = Path(source).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        name = path.name
        if path.stat().st_size > MAX_BYTES:
            raise ValueError("Tệp quá 32 MiB.")
        data = path.read_bytes()
        source = str(path)
    if not FILE_PATTERN.fullmatch(name):
        raise ValueError("Tên tệp nguồn phải là tên .cps thông thường, không chứa ký tự đặc biệt.")
    if not data or len(data) > MAX_BYTES:
        raise ValueError("Tệp CPS rỗng hoặc quá 32 MiB.")
    return name, data, source


def intake_machine(machine_id: str, path: str, revision: str, digest: str) -> None:
    """Write only draft documentation; never overwrite an existing machine."""
    machine = ROOT / "machines" / f"{machine_id}.md"
    post_dir = ROOT / "posts" / machine_id
    if machine.exists() or post_dir.exists():
        print(f"Máy {machine_id} đã có hồ sơ/thư mục post; không ghi đè. Kiểm tra mapping upstream thủ công.")
        return
    prompts = {
        "Hãng/model máy": "Hãng và model máy vật lý",
        "Controller/phiên bản": "Controller và phiên bản",
        "Loại gia công, trục, động học": "Loại gia công, trục và động học",
        "Option thực tế": "Option đã lắp (ATC, probing, coolant, TCP...)",
        "Đơn vị/giới hạn liên quan": "Đơn vị và giới hạn liên quan",
        "WCS và bù dao": "WCS và bù dao",
        "Quy trình ATC": "Quy trình thay dao/ATC đã xác minh",
        "Retract/home và hệ tọa độ": "Retract/home và hệ tọa độ đã xác minh",
        "Spindle/coolant/M-code phụ": "Spindle, coolant và M-code đã xác minh",
        "Post/properties hiện dùng": "Post và properties hiện dùng",
        "Người phụ trách": "Người phụ trách CAM/kỹ thuật xưởng",
    }
    answers = {field: ask(question) for field, question in prompts.items()}
    manual = ask("Tài liệu máy (nguồn/trang hoặc UNKNOWN)")
    template = (ROOT / "machines" / "_template-machine.md").read_text(encoding="utf-8")
    template = template.replace("# Máy: <machine-id>", f"# Máy: {machine_id}")
    for field, value in answers.items():
        old = f"| {field} | UNKNOWN | |"
        if old not in template:
            raise RuntimeError(f"Không tìm thấy trường máy: {field}")
        source = "Người nhập (chờ đối chiếu manual)" if value != "UNKNOWN" else ""
        template = template.replace(old, f"| {field} | {value} | {source} |")
    template = template.replace(
        "## Tài liệu và chương trình tham chiếu\n\nChưa cung cấp.",
        f"## Tài liệu và chương trình tham chiếu\n\nTài liệu: {manual}. "
        "Chưa có chương trình tham chiếu đã review.\n\n"
        f"Post nhập: {path} (revision khai báo: {revision}; SHA-256: {digest}).",
    )
    post_template = (ROOT / "posts" / "_template-post" / "README.md").read_text(encoding="utf-8")
    post_template = post_template.replace("<machine-id>", machine_id)
    post_template = post_template.replace("Upstream/revision/hash: UNKNOWN", f"Upstream/revision/hash: {path}; {revision}; {digest}")
    post_dir.mkdir()
    machine.write_text(template, encoding="utf-8")
    (post_dir / "README.md").write_text(post_template, encoding="utf-8")
    checklist = (ROOT / "posts" / "_template-post" / "RELEASE-CHECKLIST.md").read_bytes()
    (post_dir / "RELEASE-CHECKLIST.md").write_bytes(checklist)
    print(f"Đã tạo hồ sơ draft {machine.relative_to(ROOT)} và checklist/mapping tại {post_dir.relative_to(ROOT)}.")
    print("Chưa tạo CPS custom; kỹ thuật viên phải đọc upstream và chốt rule trước khi sửa.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Nhập CPS gốc và tạo hồ sơ máy draft; không phát hành post.")
    parser.add_argument("--path", required=True, help="Đường dẫn file .cps local hoặc URL HTTPS trực tiếp tới .cps")
    args = parser.parse_args()
    name, data, input_source = read_source(args.path)
    digest = hashlib.sha256(data).hexdigest()
    print(f"Tệp: {name}; SHA-256: {digest}")
    base_id = safe_id(ask("Base ID (tên định danh post nền)", default=None))
    revision = ask("Revision chính thức (không biết để UNKNOWN)")
    if revision != "UNKNOWN":
        safe_id(revision)
    folder_revision = revision if revision != "UNKNOWN" else f"unverified-{digest[:12]}"
    source_url = ask("URL nguồn chính thức/nhà cung cấp (UNKNOWN nếu chưa rõ)")
    if source_url != "UNKNOWN" and not source_url.startswith("https://"):
        raise ValueError("URL nguồn cần bắt đầu bằng https://; nếu không có, nhập UNKNOWN.")
    engine = ask("Engine Autodesk tối thiểu (UNKNOWN nếu chưa xác minh)")
    license_terms = ask("License/điều kiện sử dụng và phân phối (UNKNOWN nếu chưa rõ)")
    machine_id = ask("ID máy vật lý để tạo hồ sơ (Enter để bỏ qua)", default="")
    if machine_id:
        safe_id(machine_id)
    dest = ROOT / "upstream" / base_id / folder_revision / name
    relative = dest.relative_to(ROOT).as_posix()
    manifest = ROOT / "upstream" / "MANIFEST.md"
    text = manifest.read_text(encoding="utf-8")
    if HEADER not in text or SEPARATOR not in text:
        raise ValueError("Header MANIFEST không đúng mẫu; chưa nhập file.")
    if dest.exists():
        old_digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        if old_digest != digest:
            raise FileExistsError(f"Trùng đường dẫn nhưng khác nội dung: {relative}; hãy kiểm tra revision.")
        if f"| {relative} |" not in text:
            raise ValueError(f"File đã tồn tại nhưng thiếu trong manifest: {relative}. Hãy đối chiếu thủ công.")
        print(f"Đã có cùng tệp tại {relative}; không ghi đè hoặc thêm manifest trùng.")
        if machine_id:
            intake_machine(machine_id, relative, revision, digest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("xb") as output:
        output.write(data)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != digest:
        dest.unlink()
        raise IOError("SHA-256 bản lưu khác nguồn; đã xóa bản lưu lỗi.")
    row = [base_id, relative, revision, source_url,
           input_source if input_source.startswith("https://") else f"local:{name}",
           date.today().isoformat(), digest, engine, license_terms,
           f"Dự kiến: {machine_id}" if machine_id else "UNKNOWN"]
    line = "| " + " | ".join(row) + " |"
    try:
        manifest.write_text(text.rstrip() + "\n" + line + "\n", encoding="utf-8")
    except OSError:
        dest.unlink()
        raise
    print(f"Đã lưu nguyên trạng tại {relative}; cập nhật upstream/MANIFEST.md.")
    if machine_id:
        intake_machine(machine_id, relative, revision, digest)
    else:
        print("Chưa có ID máy: mới nhập upstream, chưa lập hồ sơ/mapping máy.")
    print("Metadata do người nhập khai báo cần kỹ thuật viên xác minh; chưa test, chưa approved.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, EOFError) as error:
        print(f"Lỗi: {error}", file=sys.stderr)
        sys.exit(1)