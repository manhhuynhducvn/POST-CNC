# Thêm máy mới

Khi người dùng nói “có máy mới”, bắt đầu quy trình này. Có thể chuẩn bị hồ sơ trước khi đủ dữ liệu; phần thiếu ghi UNKNOWN và chặn các thay đổi phụ thuộc vào nó.

## Thông tin cần thu thập

- ID máy trong xưởng, hãng và model máy, controller và phiên bản.
- Phay/tiện/mill-turn; số trục, kiểu bố trí và động học trục quay.
- Option đang lắp: ATC, probing, coolant xuyên tâm, TCP, chu trình hỗ trợ, v.v.
- Manual máy và bảng G/M-code của nhà chế tạo; chương trình đã chạy ổn nếu có.
- Post hiện dùng, properties, phiên bản Fusion/engine nếu biết.
- Trình tự đầu chương trình, thay dao, retract/home, kết thúc đã được xác nhận.
- Đơn vị, hệ tọa độ, quy ước bù dao, giới hạn và vị trí máy có liên quan.
- Ví dụ G-code gốc và bản sửa mong muốn, kèm lý do từng thay đổi.
- File CAM hoặc input trung gian, setup/phôi/đồ gá đại diện.
- Người phụ trách CAM và người xác nhận tại xưởng.

Tên controller đơn lẻ không đủ để xác định M-code hay quy trình thay dao.

## Các bước thực hiện

1. Chọn post nền phù hợp, kiểm tra nguồn/điều kiện sử dụng và properties trước khi custom. Nếu có file `.cps` local hoặc URL HTTPS trực tiếp tới CPS, chạy `python tools/import_post.py --path "<đường-dẫn-hoặc-URL>"` từ gốc repo. Không chạy script với post đã sửa tay rồi coi là gốc.
2. Script hỏi base ID, revision thực (không biết ghi UNKNOWN), nguồn, engine, điều kiện sử dụng và ID máy; lưu nguyên trạng ở `upstream/<base-id>/<revision>/` (revision chưa xác minh dùng `unverified-<hash>`), ghi `upstream/MANIFEST.md`. Nhập ID máy để tiếp tục hỏi thông tin thực và tạo `machines/<machine-id>.md`, `posts/<machine-id>/README.md` cùng checklist **draft**. Nếu đã có hồ sơ máy, script không ghi đè; đối chiếu và cập nhật mapping thủ công.
3. Kỹ thuật viên đối chiếu thông tin máy và nguồn post với manual/người xác nhận. Dữ liệu UNKNOWN không được phép suy đoán. Đọc upstream thực và tạo CPS phát triển trong `posts/<machine-id>/` khi đã chốt yêu cầu; script **không** tạo CPS custom.
4. Lập bảng cho từng rule: áp dụng/không áp dụng/chưa rõ, điều kiện và ngoại lệ, properties hoặc phần code thực thi, tình huống test. Rule chung không mặc nhiên áp dụng mọi máy. Nếu chưa có yêu cầu thay đổi, ghi rõ `baseline`: không custom logic, không áp dụng rule custom.
5. Với baseline, kiểm tra post gốc bằng properties/configuration phù hợp với máy, test các tình huống trong phạm vi hỗ trợ, so sánh output và review với kỹ thuật viên. Chỉ khi có bằng chứng phù hợp mới tạo release custom baseline cho máy; không dùng upstream generic trực tiếp làm release máy.
6. Nếu có yêu cầu thay đổi, sửa từng hành vi, so sánh output với upstream và kết quả mong muốn đã review.
7. Ghi engine, input, properties và kết quả test. Thiếu điều kiện thì ghi chưa kiểm thử.
8. Chuẩn bị candidate, review kỹ thuật và kiểm chứng tại xưởng theo quy trình máy.
9. Người có trách nhiệm xác nhận phạm vi approved. Đóng gói release với cấu hình, hướng dẫn và bằng chứng.

## Kết quả cần có

Hồ sơ máy, nguồn upstream, CPS custom, mapping rule, input test, output được review, checklist và trạng thái phát hành. Chưa có xác nhận tại xưởng thì không gọi post là sẵn sàng sản xuất.
