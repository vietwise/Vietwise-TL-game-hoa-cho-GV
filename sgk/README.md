# Danh mục sách giáo khoa 2026

Thư mục này **chỉ chứa danh mục**: tên sách, bộ sách, lớp, môn và đường link về trang của NXB Giáo dục Việt Nam. Repo công khai nên **không đưa file sách** vào đây. File sách do Viện Giáo dục và Quản trị Nhân lực (IEHRM) tải về để nghiên cứu được lưu ở nơi riêng tư.

Mỗi dòng trong `danh-muc.json`:

| Trường | Ý nghĩa |
| --- | --- |
| `id` | Mã ổn định, chữ thường không dấu, ví dụ `toan-5-kntt-tap-1` |
| `ten` | Tên sách đúng như bìa |
| `bo_sach` | Kết nối tri thức với cuộc sống, Chân trời sáng tạo, Cánh Diều… |
| `lop` | `1`–`12`, hoặc `mam-non` |
| `mon` | Môn học |
| `tap` | Số tập, nếu có |
| `link` | Trang của sách trên taphuan.nxbgd.vn hoặc hanhtrangso.nxbgd.vn |

Skill game dùng danh mục này để gọi đúng tên sách và bài. Khi soạn game cho một bài cụ thể, giáo viên vẫn chụp hoặc dán trang SGK cho Claude.
