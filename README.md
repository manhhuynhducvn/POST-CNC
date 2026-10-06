# POST-CNC

Repository quản lý Post Processor cho các máy CNC của công ty.

Mục tiêu của repository là biến toolpath từ Fusion 360 thành G-code phù hợp với từng máy CNC, đồng thời áp dụng các quy tắc vận hành chung của công ty. Repository sử dụng post processor Autodesk/Fusion làm nền và chỉ thay đổi những phần cần thiết.

## Phạm vi

POST-CNC quản lý:

- Post processor gốc và revision đã sử dụng.
- Post processor custom theo từng máy thực tế.
- Quy tắc công ty và cách triển khai quy tắc trên từng controller.
- Thông số máy, controller, M-code và vị trí an toàn.
- Bộ chương trình mẫu và G-code đã được xác nhận.
- Lịch sử thay đổi, review và trạng thái phê duyệt.

POST-CNC không làm thay cho lập trình CAM. Lập trình viên vẫn chịu trách nhiệm về mô hình 3D, phôi, đồ gá, dao, toolpath, chiều cao an toàn và mô phỏng trong Fusion 360.

## Quy trình tổng quát

```text README.md
Mô hình 3D + phôi + đồ gá
        ↓
Lập trình CAM trong Fusion 360
        ↓
Chọn đúng post custom của máy
        ↓
G-code theo quy tắc công ty và controller
        ↓
Review, mô phỏng, dry run
        ↓
Gia công và kiểm tra sản phẩm
```

## Cấu trúc repository

```text README.md
POST-CNC/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/
│   ├── repository-workflow.md
│   ├── fusion-user-workflow.md
│   └── adding-a-machine.md
├── rules/
│   ├── README.md
│   ├── R001-operation-transition.md
│   ├── R002-safe-retract.md
│   ├── R003-home-position.md
│   ├── R004-tool-change.md
│   ├── R005-spindle.md
│   ├── R006-coolant.md
│   ├── R007-header.md
│   ├── R008-footer.md
│   ├── R009-coordinate-system.md
│   ├── R010-program-end.md
│   ├── _template-rule.md
│   └── CHANGE-REQUESTS.md
├── machines/
│   ├── README.md
│   └── _template-machine.md
├── upstream/
│   ├── README.md
│   └── MANIFEST.md
├── posts/
│   ├── README.md
│   └── _template-post/
│       ├── README.md
│       └── RELEASE-CHECKLIST.md
├── tests/
│   ├── README.md
│   ├── fixtures/README.md
│   ├── expected/README.md
│   └── review/README.md
└── releases/
    └── README.md
```

## Cách sử dụng hằng ngày

Lập trình viên CAM chỉ sử dụng **release đã được phê duyệt** cho đúng máy (xem `releases/`); không lấy file `.cps` đang phát triển trong `posts/<machine-id>/` để chạy sản xuất. Họ tiếp tục khai báo phôi, đồ gá, gốc tọa độ, dao, operation và chiều cao an toàn trong Fusion 360 như quy trình CAM của công ty.

File `.cps` phát hành phải được sao chép vào thư mục Post Library/Posts của Fusion 360 hoặc được cung cấp qua thư viện dùng chung của công ty. Người dùng CAM không chỉnh sửa file post trong lúc lập trình.

## Nhập post và bắt đầu hồ sơ máy

Từ thư mục gốc repo, với Python 3.10+:

```powershell README.md
python tools/import_post.py --path "C:/duong-dan/post-goc.cps"
```

Có thể thay đường dẫn local bằng URL HTTPS trực tiếp tới `.cps` (không query/token). Script hỏi metadata, tính SHA-256, lưu nguyên trạng vào upstream và cập nhật manifest. Cung cấp ID máy để tiếp tục hỏi thông tin máy, tạo hồ sơ/mapping/checklist draft; dữ liệu chưa rõ để UNKNOWN. Script không tự sửa CPS hoặc duyệt post. Xem [hướng dẫn nhập upstream](upstream/README.md) và [quy trình máy mới](docs/adding-a-machine.md).

Rule chung được quản lý trong `rules/`, mỗi máy có bảng mapping riêng; yêu cầu đặc thù ghi rõ phạm vi máy. Xem [rule chung và riêng](rules/README.md).

## Khi có máy mới

Khi có máy mới, quy trình mặc định là:

1. Thu thập thông tin máy và controller.
2. Chọn post Autodesk phù hợp làm upstream.
3. Ghi revision, nguồn và ngày lấy post vào `upstream/MANIFEST.md`.
4. Tạo hồ sơ máy trong `machines/<machine-id>.md`.
5. Tạo mapping trong `posts/<machine-id>/`. Nếu chưa có rule hay yêu cầu thay đổi, ghi kiểu triển khai `baseline`, giữ upstream nguyên trạng và lưu properties đã xác minh; chỉ tạo CPS custom khi có khác biệt cần sửa.
6. Nếu có rule, áp dụng các rule có liên quan và ghi rõ mapping từ rule sang code.
7. Tạo hoặc chọn fixture CAM đại diện.
8. So sánh với post upstream và G-code kỳ vọng.
9. Review kỹ thuật, kiểm chứng tại xưởng theo quy trình của máy và xác nhận sản phẩm mẫu khi cần.
10. Chỉ đưa post vào `releases/` với trạng thái `approved` khi người phụ trách đã xác nhận bằng chứng.

Câu “có máy mới” trong phạm vi repository này có nghĩa là bắt đầu đúng quy trình trên. Không được phát hành post chỉ dựa trên tên hãng hoặc tên controller; cần xác nhận model máy, option máy và quy trình vận hành thực tế.

## Nguyên tắc an toàn

- Không sửa G-code thủ công như một bước sản xuất bình thường.
- Không dùng post custom trên máy khác nếu chưa được xác nhận.
- Không thay upstream mà không ghi revision và chạy lại kiểm thử.
- Không giả định hai máy cùng controller có cùng M-code hoặc cùng vị trí thay dao.
- Không coi G-code đã post là an toàn chỉ vì post không báo lỗi.
- Luôn review và dry run trước lần chạy thực tế đầu tiên sau khi đổi post.

Các rule khởi tạo hiện chỉ là **đề xuất để thảo luận**, chưa có rule nào được duyệt hoặc post sẵn sàng sử dụng. Ghi các thao tác sửa tay lặp lại vào `rules/CHANGE-REQUESTS.md`, rồi đánh giá để đưa thành rule và test thay vì mặc định xóa lệnh theo tên G-code.

`rules/` là tài liệu yêu cầu của công ty. Cách thực thi có thể khác giữa FANUC, Mitsubishi, Okuma và từng model máy; vì vậy post custom theo máy là nguồn thực thi, còn rule là nguồn yêu cầu.
