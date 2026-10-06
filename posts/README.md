# Source post custom

Thư mục này thay cho tên custom trong đề xuất ban đầu. Source ở đây không mặc nhiên được phép dùng sản xuất; người dùng lấy release approved.

Tạo `posts/<machine-id>/` với README mapping rule và RELEASE-CHECKLIST.md. Nếu máy chỉ dùng hành vi của post nền, ghi trạng thái `baseline` và upstream/revision/hash; không bắt buộc tạo một CPS copy khác biệt. Nếu cần chỉnh sửa, CPS custom phải dựa trên upstream thực tế và được lưu trong thư mục máy.

Baseline vẫn cần test, review và release approved theo đúng máy; upstream generic không tự trở thành release an toàn chỉ vì chưa có custom rule. Bắt đầu với chỉnh sửa nhỏ trong từng CPS. Chỉ thêm thư viện dùng chung hoặc bước build khi có nhu cầu và đã xác minh cơ chế hỗ trợ của Autodesk engine.
