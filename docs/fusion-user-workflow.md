# Sử dụng post trong Fusion

1. Xác định ID máy sẽ chạy và lấy release approved tương ứng; không lấy source draft trong posts.
2. Import/chọn CPS qua Post Library của Fusion (local hoặc thư viện công ty đang sử dụng). Tên menu có thể khác theo phiên bản Fusion. Nếu gói có dependency/cấu hình, cài đủ theo release.
3. Lập trình CAM cho từng sản phẩm: phôi, đồ gá, dao, WCS, toolpath, chiều cao và đường chuyển tiếp phù hợp.
4. Trong NC Program/Post Process, chọn đúng post và properties được phát hành cho máy; xuất G-code.
5. Kiểm tra output và mô phỏng phù hợp. Mô phỏng toolpath không mặc nhiên kiểm chứng mọi chuyển động do post bổ sung.
6. Thiết lập máy thực tế khớp CAM; kiểm chứng chương trình mới/đã thay đổi theo quy trình xưởng trước sản xuất.

Nếu cần sửa G-code, báo lại người giữ post với file CAM/input, properties, post version, output gốc và thay đổi mong muốn. Phân biệt lỗi CAM, cấu hình, post và yêu cầu riêng của job trước khi sửa post dùng chung.

Custom post giảm thao tác sửa tay lặp lại; không loại bỏ trách nhiệm kiểm tra từng chương trình.
