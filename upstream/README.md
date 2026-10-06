# Post gốc

Lấy post phù hợp từ Autodesk Post Library: https://cam.autodesk.com/posts/ hoặc nguồn nhà cung cấp được xác nhận.

Giữ nguyên file và thông báo bản quyền. Ghi điều kiện sử dụng/phân phối của từng post; license của cam-posteditor không tự áp dụng cho CPS.

Tổ chức: `<base-id>/<revision>/<original-name>.cps`. Nếu không xác minh được revision, lưu dưới `unverified-<12 ký tự SHA-256>/` và ghi `UNKNOWN` trong manifest; không tự nhận đó là revision của Autodesk. MANIFEST ghi nguồn, tên file/URL đầu vào và hash để tái lập. Đường dẫn local đầu vào chỉ ghi tên tệp (tránh lộ đường dẫn máy cá nhân); URL chính thức do người nhập khai báo phải được đối chiếu. Không có post gốc nào được tải ở giai đoạn khởi tạo này.

Chạy lệnh tương tác từ thư mục gốc repo (yêu cầu Python 3.10+):

```powershell upstream/README.md
python tools/import_post.py --path "C:/duong-dan/post-goc.cps"
```

Hoặc truyền URL HTTPS trực tiếp trỏ đến tệp `.cps`, không kèm query/token. Trang danh sách Post Library không phải URL trực tiếp tới CPS; nếu chỉ có trang web, tải file về và dùng đường dẫn local. Script không xác minh CPS phù hợp máy hay giấy phép; không dùng upstream trực tiếp trong sản xuất.
