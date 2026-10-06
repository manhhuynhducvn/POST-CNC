# Rxxx – <chủ đề>

Status: proposed

## Quan sát thực tế

- Máy, post/properties, loại job và setup: UNKNOWN
- Lệnh hoặc chuyển động lặp lại; ví dụ G-code trước/sau: UNKNOWN
- Nguồn gốc: CAM, property post, logic post, hay yêu cầu máy: UNKNOWN
- Rủi ro khi bỏ/đổi lệnh: UNKNOWN

## Mục tiêu

Nêu vấn đề cần giải quyết và thước đo (thời gian chỉnh tay, thời gian chạy máy, độ tin cậy, v.v.). Không coi giảm dòng G-code là mục tiêu độc lập.

## Điều kiện áp dụng

Ghi rõ setup, cùng/khác dao, WCS, định hướng trục, đồ gá, trạng thái máy và ngoại lệ. Phân biệt yêu cầu CAM theo job với hành vi dùng chung của post.

## Hành vi bắt buộc và hành vi cấm

Chỉ chốt sau khi đã đối chiếu manual, upstream/properties và người phụ trách xưởng.

## Triển khai từng máy

Link `posts/<machine-id>/README.md`; có thể không áp dụng hoặc cần triển khai khác nhau.

## Kiểm thử và phê duyệt

- Tình huống đối chứng/ngoại lệ, toolpath/input, engine/properties: UNKNOWN
- G-code review, dry run/kiểm chứng tại xưởng: chưa có
- Người/ngày duyệt: chưa có
