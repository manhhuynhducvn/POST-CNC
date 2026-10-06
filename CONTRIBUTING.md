# Quy trình đóng góp POST-CNC

## Một thay đổi post hợp lệ

Mỗi thay đổi làm ảnh hưởng đến G-code cần có:

- Máy hoặc nhóm máy bị ảnh hưởng.
- Rule liên quan, nếu có.
- Lý do thay đổi.
- Ví dụ G-code trước và sau, hoặc mô tả hành vi trước và sau.
- Fixture đã chạy.
- Người review kỹ thuật.
- Trạng thái test trên máy mô phỏng hoặc máy thật.

## Luồng thay đổi

1. Tạo branch cho thay đổi.
2. Mô tả vấn đề bằng một issue hoặc phần mô tả trong pull request.
3. Sửa post custom và tài liệu mapping rule.
4. Chạy post với fixture đại diện.
5. Kiểm tra các thay đổi ngoài phạm vi dự kiến.
6. Review G-code và rủi ro chuyển động.
7. Dry run trên máy nếu thay đổi ảnh hưởng đến chuyển động, tool change, spindle, coolant, tọa độ hoặc kết thúc chương trình.
8. Chỉ phát hành sau khi có phê duyệt.

## Trạng thái post

- `draft`: đang phát triển, không dùng sản xuất.
- `candidate`: đã xuất được G-code và đang chờ kiểm thử.
- `approved`: đã được xác nhận cho đúng máy và đúng phạm vi.
- `deprecated`: không dùng cho chương trình mới nhưng vẫn giữ để truy vết.
- `retired`: không còn được phép sử dụng.

## Phân biệt loại thay đổi

- Thay đổi syntax hoặc format: vẫn cần kiểm tra output.
- Thay đổi logic chuyển động: cần review an toàn và dry run.
- Thay đổi tool change, home, work offset hoặc program end: cần xác nhận theo manual máy và trên máy thật.
- Cập nhật upstream: cần so sánh revision cũ/mới trước khi merge vào post custom.
