# Hướng dẫn cho trợ lý làm việc với POST-CNC

## Mục tiêu và giới hạn

Tận dụng post Autodesk/Fusion có sẵn; chỉ custom phần khác biệt của công ty và máy. Không xây CAM hoặc post engine mới. Không dùng thay thế chuỗi G-code làm workflow sản xuất.

Đọc README.md, docs/adding-a-machine.md, rules/README.md và hồ sơ máy liên quan trước khi triển khai. Câu “có máy mới” kích hoạt quy trình docs/adding-a-machine.md; không yêu cầu người dùng giải thích lại mục tiêu repo.

## Khi có máy mới

1. Kiểm tra hồ sơ hiện có, dùng dữ liệu đã cung cấp; chỉ hỏi những thông tin còn thiếu.
2. Tạo hồ sơ draft với ID máy vật lý (ví dụ MC-001), hãng/model máy, controller, cấu hình trục và option. Controller không phải model máy.
3. Ghi thông tin chưa rõ là UNKNOWN, không tự đoán M-code, tọa độ home, thứ tự ATC hoặc độ cao an toàn.
4. Chọn post nền gần nhất có nguồn và điều kiện sử dụng rõ ràng. Ưu tiên properties/cấu hình sẵn có trước khi sửa logic.
5. Ghi nguồn, revision, hash, ngày lấy, yêu cầu engine; giữ nguyên nội dung upstream.
6. Tạo posts/<machine-id>/ với README, mapping rule và checklist. Chỉ tạo CPS thực khi đã đọc post nền; không tạo CPS giả hoặc mẫu được mô tả như dùng được.
7. Triển khai từng thay đổi nhỏ, gắn rule và tình huống test. Rule là yêu cầu có điều kiện; không phải mọi rule đều áp dụng cho mọi máy.
8. Kiểm thử với engine Autodesk nếu có. Nếu thiếu engine, input CAM hoặc quyền truy cập thì ghi rõ chưa chạy, không báo pass.
9. Chuẩn bị candidate để kỹ thuật review và xác nhận tại xưởng. Trợ lý không tự xác nhận dry run hoặc gán approved khi chưa có bằng chứng từ người có trách nhiệm.
10. Phát hành đúng phiên bản đã duyệt cùng properties/cấu hình và phạm vi sử dụng. Chỉ thao tác remote GitHub theo yêu cầu người dùng.

## Các giả định bị cấm

- Không coi G28/G53 hoặc lệnh modal lặp là thừa chỉ vì xuất hiện nhiều lần.
- Không giả định upstream luôn về X/Y home giữa operation hoặc phù hợp mọi máy cùng controller.
- Không dùng Z10, Retract Height hay Clearance Height như bảo đảm tránh mọi đồ gá. Phải xét đường chuyển tiếp, hệ tọa độ, dao, hướng trục và setup.
- Không giả định Fusion tự truyền các biến clearanceHeight/retractHeight đúng tên hoặc đủ dữ liệu; kiểm tra API và input thực tế.
- Không khẳng định load() là cơ chế import code phù hợp CPS nếu chưa xác minh. Chưa cần shared library; giữ thay đổi nhỏ trên post nền.
- Không đồng nhất giảm số dòng, giảm thời gian post và giảm thời gian chu kỳ trên máy.
- Không khẳng định không có repo tương tự trên GitHub; khảo sát trước đây không chứng minh điều đó.

## Cập nhật và rollback

Mỗi thay đổi cần tài liệu và kiểm thử phù hợp. Không thay baseline expected chỉ để test pass. Rollback về release custom đã được phê duyệt cho máy, không tự quay về post generic upstream. Giữ lịch sử những release đã dùng cho sản xuất.
