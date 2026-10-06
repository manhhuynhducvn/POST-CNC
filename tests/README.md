# Kiểm thử

Chưa có input thực tế hoặc post engine được cấu hình; chưa có test sinh G-code nào được chạy.

- fixtures: job CAM và/hoặc input trung gian Autodesk tương thích engine. File .f3d không tự chạy trực tiếp bằng post.exe; cần Fusion tạo toolpath/input phù hợp.
- expected: output đã review cho đúng post, engine và properties. Output upstream chỉ là đối chiếu, không tự là chuẩn đúng.
- review: bằng chứng review và kiểm chứng tại xưởng.

Ma trận tối thiểu theo phạm vi máy: nhiều operation cùng dao, đổi dao, đổi WCS, đầu/cuối chương trình, spindle/coolant, cycles, mm/inch nếu hỗ trợ, rotary/probing nếu có. Bổ sung ca tái hiện từng lỗi.

So sánh output và kiểm tra hành vi: thứ tự chuyển động, tọa độ/modal state, bù dao, không bỏ lệnh cần thiết. Chỉ cập nhật expected sau review thay đổi. Diff không chứng minh không va chạm.

Đo thời gian post riêng với chu kỳ máy. Benchmark chỉ thêm khi có nhu cầu; không là bằng chứng G-code đúng.
