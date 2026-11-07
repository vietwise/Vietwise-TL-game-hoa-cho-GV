# Vietwise – Trợ lý game hóa cho giáo viên

Kho tài nguyên chung cho bộ skill game hóa dành cho giáo viên. Claude chỉ viết **nội dung game** (một file JSON). Ảnh, trình chơi và khung nội dung nằm sẵn ở đây, nên giáo viên dùng Claude bản miễn phí vẫn ra được game chạy tốt.

Hiện có hai loại game, cả hai **không thi đua, không chấm điểm**:

| Loại | `loai` | Mục tiêu | Các bước trên màn hình |
| --- | --- | --- | --- |
| Game 1 – Mở tiết | `mo-tiet` | Khơi tò mò cho bài sắp học (10 phút) | Kể → Chọn → Nói lý do → Bước ngoặt → Câu hỏi của hôm nay |
| Game 2 – Ôn bài | `on-bai` | Vận dụng kiến thức đã học, có chứng cứ, phản biện, sáng tạo (15 phút) | Kể → Chọn → Chứng cứ → Phản biện → Sáng tạo → Chốt kiến thức |
| Game 3 – Sách là Thầy | `sach-la-thay` | Phải đọc và hiểu một cuốn sách mới chơi được; chứng cứ lấy từ sách (20 phút) | Chìa khoá sách → Kể → Chọn → Sách nói gì → Phản biện → Viết tiếp → Chốt bài học |

## Cấu trúc

```
assets/
  manifest.json   danh sách ảnh: id, tệp, mô tả, lứa tuổi, chủ đề
  sprites/        nhân vật, con vật, đồ vật
  cards/          lưng thẻ
  backgrounds/    ảnh nền theo bối cảnh
player/
  index.html      trình chơi chung cho cả hai loại game
schema/
  game-spec.schema.json   khung JSON mà Claude phải viết đúng
examples/         game mẫu cho từng loại
```

## Thêm hoặc thay ảnh

1. Đặt tệp vào đúng thư mục (`sprites/`, `cards/`, `backgrounds/`). Nên dùng PNG nền trong hoặc SVG, tên tệp không dấu, không khoảng trắng.
2. Thêm một dòng vào `assets/manifest.json`. `mo_ta` viết bằng lời thường, vì Claude chọn ảnh dựa vào mô tả này mà không nhìn thấy ảnh.
3. Muốn thay ảnh tạm bằng ảnh thật thì **giữ nguyên `id`**, chỉ đổi `tep` và bỏ `"tam": true`. Như vậy các game cũ vẫn chạy.
4. Không đổi hoặc xoá `id` đã dùng. Nếu cần bỏ một ảnh, hãy thêm ảnh mới với `id` mới.

Các ảnh hiện có đều là **ảnh tạm** (có chữ "ẢNH TẠM").

## Mở một game

- **Dán JSON**: mở `player/index.html`, dán khối JSON từ Claude rồi bấm **Mở game**.
- **Theo đường dẫn**: `player/index.html?spec=<đường dẫn tới file JSON>`. Ví dụ: `?spec=../examples/on-bai-khoahoc4-nuoc.json`.
- **Ảnh ở nơi khác**: thêm `&assets=<đường dẫn thư mục assets/>`.

Phím tắt: ← → chuyển bước · Cách: bật/dừng đồng hồ · G: chế độ giáo viên (hiện cái giá của từng lựa chọn, gợi ý lựa chọn D, đáp số; đừng chiếu phần này) · F: toàn màn hình.

Trình chơi phải chạy qua web (GitHub Pages, Edubit hoặc `python3 -m http.server`). Nếu mở thẳng file trên máy, trình duyệt sẽ chặn đọc `manifest.json` và game sẽ hiện không có ảnh.

## Đưa lên mạng

- **Trình chơi**: bật GitHub Pages cho repo này (Settings → Pages → nhánh `main`). Khi đó trình chơi có ở `https://vietwise.github.io/Vietwise-TL-game-hoa-cho-GV/player/`. Edubit cũng có thể tự chứa trình chơi.
- **Ảnh**: có thể tải qua jsDelivr và ghim theo phiên bản để game cũ không đổi khi repo cập nhật, ví dụ `https://cdn.jsdelivr.net/gh/vietwise/vietwise-tl-game-hoa-cho-gv@v1.0/assets/`. Không dùng jsDelivr cho `player/index.html`, vì jsDelivr trả HTML dưới dạng văn bản thường.

## Khung JSON

Xem `schema/game-spec.schema.json`. Tóm tắt:

- Bắt buộc với cả hai loại: `phien_ban` ("1.0"), `loai`, `tieu_de`, `mon`, `lop`, `bai`, `pham_chat`, `loi_ke`, `lua_chon` (2–3 lựa chọn A/B/C).
- `mo-tiet` cần thêm `buoc_ngoat` và `cau_hoi_treo`.
- `on-bai` cần thêm `kien_thuc` và `so_do_chot`.
- `sach-la-thay` cần thêm `sach`, `chia_khoa`, `kien_thuc` và `so_do_chot`.
- Mọi loại có thể thêm `tuong_tac` (7 kiểu tương tác), `ba_nhip`, `chau_ngoc`, `du_an_that`. Chi tiết ở [docs/game-spec.md](docs/game-spec.md).
- Ảnh khai báo bằng `id` trong manifest: `boi_canh`, `nhan_vat[].sprite`.
- Trường bắt đầu bằng `gv_` chỉ hiện ở chế độ giáo viên.
