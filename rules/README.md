# Company Rules

Company Rule là yêu cầu về hành vi của chương trình NC do công ty mong muốn. Rule không phải là một câu lệnh G-code cố định và không phải rule nào cũng áp dụng cho mọi máy hoặc mọi setup.

Mỗi rule cần trả lời:

- Mục tiêu và lý do.
- Điều kiện áp dụng.
- Hành vi bắt buộc.
- Ngoại lệ an toàn.
- Cách triển khai theo controller/máy.
- Tình huống test.
- Người phê duyệt.

`rules/` là nguồn yêu cầu. `posts/<machine-id>/README.md` ghi cách rule được triển khai trên post cụ thể. Nếu rule và manual máy mâu thuẫn, phải dừng và xử lý như một yêu cầu kỹ thuật; không tự ưu tiên rule công ty.

## Rule chung hay riêng từng máy?

- Rule chung mô tả **mục tiêu/hành vi có điều kiện** (ví dụ: chuyển operation an toàn); có thể nhiều máy cùng tham chiếu, không tự động áp dụng cho tất cả.
- Mỗi máy có **mapping riêng** trong `posts/<machine-id>/README.md`: trạng thái áp dụng/không áp dụng/chưa xác định, điều kiện, ngoại lệ, property hay phần code, test và người xác nhận. Cùng một rule có thể dùng property ở máy A, cần thay đổi CPS ở máy B, hoặc không áp dụng ở máy C.
- Nếu chỉ một máy hoặc nhóm máy có yêu cầu đặc thù, tạo rule có phạm vi máy rõ ràng bằng `_template-rule.md`, link trong mapping; không nhân bản toàn bộ bộ rule cho mỗi máy.
- Trường hợp do đồ gá/job khác nhau thuộc trách nhiệm CAM trừ khi đã xác nhận một điều kiện post có thể biểu đạt và kiểm thử an toàn. Không suy diễn G/M-code từ rule chung; chưa xác nhận thì giữ `chưa xác định`, không triển khai.

## Khi không có rule

Ghi quyết định `baseline`: máy dùng post nền đã chọn và properties/cấu hình đã xác minh, không thêm custom logic. Kỹ thuật viên vẫn phải kiểm tra post với đúng máy, controller, option, input CAM và tình huống vận hành trong phạm vi hỗ trợ. Kết quả được ghi trong mapping máy và checklist; sau khi review/kết chứng phù hợp có thể phát hành một release baseline cho máy. Không dùng trực tiếp file trong `upstream/` làm release chỉ vì chưa có rule.

## Danh sách rule khởi tạo

Các file R001–R010 dưới đây là khung thảo luận. Chúng chưa phải tiêu chuẩn sản xuất và chưa được phép dùng để suy ra lệnh G-code.

| ID | Chủ đề |
| --- | --- |
| R001 | Operation transition |
| R002 | Safe retract |
| R003 | Home position |
| R004 | Tool change |
| R005 | Spindle |
| R006 | Coolant |
| R007 | Header |
| R008 | Footer |
| R009 | Coordinate system |
| R010 | Program end |
