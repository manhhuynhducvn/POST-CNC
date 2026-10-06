# Cách quản lý repository

## Vai trò

Người giữ post quản lý source, rule, kiểm thử và release. Lập trình viên CAM cung cấp setup/toolpath và sử dụng release đúng máy. Người vận hành và kỹ thuật xưởng xác nhận hành vi trên máy thực tế.

## Phát triển

upstream là bản gốc giữ nguyên. posts là source đang phát triển, có thể chưa được duyệt. rules mô tả yêu cầu có điều kiện; sửa tài liệu rule không tự sửa các CPS. machines ghi dữ liệu thực tế và nguồn xác nhận. tests giữ input và bằng chứng kiểm tra. releases chỉ dẫn tới các gói đã được duyệt.

Không bắt buộc mỗi máy vật lý có code khác nhau: các máy tương đương có thể dùng cùng post đã kiểm chứng, nhưng phải có mapping hồ sơ/cấu hình/phạm vi rõ ràng. Nếu không có yêu cầu sửa post, chọn nhánh `baseline`: mapping ghi không custom logic, properties máy được kiểm chứng, giữ upstream nguyên trạng. Vẫn cần input CAM, output review và kiểm chứng tại xưởng trước khi duyệt release cho máy; không coi tên controller là bằng chứng phù hợp.

## Nhận update Autodesk

Giữ revision cũ, tải revision mới vào vị trí riêng. So sánh upstream cũ–mới và phần custom so với upstream cũ. Tích hợp có chủ đích vào nhánh phát triển, chạy lại các tình huống bị ảnh hưởng, review và xác nhận trước khi phát hành. Không ghi đè release đang sử dụng.

## Phát hành và rollback

Gói phát hành cần ID máy, version post, upstream revision/hash, properties, phạm vi hỗ trợ, giới hạn, checklist và người/ngày xác nhận. Ghi version post trong header nếu controller cho phép.

Rollback về release đã duyệt trước đó cho đúng máy (custom hoặc baseline). Nếu đây là release đầu tiên, ghi rõ chưa có bản rollback đã duyệt; bản upstream generic không mặc nhiên là phương án rollback an toàn.

## Đo cải tiến

Đo riêng thời gian xuất post, thời gian chỉnh tay và thời gian chu kỳ máy. Giảm số dòng G-code không chứng minh chu kỳ nhanh hơn. So sánh cùng job/setup và ghi điều kiện đo.
