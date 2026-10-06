# R001 – Operation transition

Status: proposed

## Mục tiêu

Quy định chuyển từ operation này sang operation khác để tránh chuyển động không cần thiết trong điều kiện đã được xác minh an toàn.

## Yêu cầu đang thảo luận

- Không tự động về X/Y machine home giữa các operation nếu không có lý do kỹ thuật hoặc thay đổi setup.
- Retract trước khi chạy ngang phải đạt mức an toàn do setup/job xác định.
- Không suy ra rằng bỏ home luôn an toàn. Đồ gá, phôi, dao, trục quay, hướng tiếp cận và clearance phải được kiểm tra.

## Phạm vi

Áp dụng cho các operation cùng setup và cùng hệ tọa độ khi post và máy hỗ trợ hành vi này. Tool change, đổi WCS, đổi orientation, probing hoặc điều kiện machine state có thể yêu cầu transition khác.

## Triển khai

Chưa có mapping theo máy. Ghi mapping trong `posts/<machine-id>/README.md` sau khi đọc post upstream và kiểm thử.

## Kiểm thử

Cần fixture có ít nhất hai operation ở hai vị trí khác nhau, đồ gá đại diện, tool change và trường hợp đổi WCS nếu máy hỗ trợ.
