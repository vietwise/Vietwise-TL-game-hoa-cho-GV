# Khung game (đọc trước khi tạo JSON)

## Nguyên tắc chung
1. Không thi đua, không điểm số, không đội, không xếp hạng, không "đúng/sai" bằng âm thanh. Học sinh được tò mò, được chọn, được lập luận bằng chứng cứ.
2. Cả lớp chơi cùng lúc trên một màn hình chiếu. Học sinh không cần thiết bị riêng. Thầy Cô điều khiển.
3. Bốn trụ cột: một tình huống thật, một quyết định cần chọn, một phẩm chất đi kèm, một kết nối với bài học.
4. Tách nội dung học sinh và nội dung Thầy Cô: trường bắt đầu bằng `gv_` chỉ hiện ở chế độ Thầy Cô. Đáp số, lời giải, hiểu lầm hay gặp luôn để trong `gv_`.
5. Không bịa số liệu, trích dẫn, số trang. Chỉ dùng kiến thức có trong nội dung bài Thầy Cô gửi hoặc kiến thức phổ thông chắc chắn.
6. Dẫn truyện từ thử thách đời thật mà kiến thức giúp giải, rồi mở ra sự hiếu kỳ về kiến thức hữu ích; không dẫn bằng cảnh làm bài tập trong lớp.
7. Gọi giáo viên là "Thầy Cô". Game chơi ngay trong artifact.

## Ba loại game
| Loại | `loai` | Phút | Mục tiêu | Các bước trong trình chơi |
| --- | --- | --- | --- | --- |
| Game mở tiết | `mo-tiet` | 10 | Khơi tò mò cho bài CHƯA học, kết bằng câu hỏi treo | Kể, Chọn, Nói lý do, Bước ngoặt, Câu hỏi của hôm nay |
| Game ôn bài | `on-bai` | 15 | Dùng kiến thức ĐÃ học để bảo vệ lựa chọn bằng chứng cứ, phản biện, sáng tạo | Kể, Chọn, Chứng cứ, Phản biện, Sáng tạo, Chốt |
| Sách là Thầy | `sach-la-thay` | 20 | Học sinh phải đọc sách mới chơi được; chứng cứ lấy từ sách | Chìa khóa sách, Kể, Chọn, Sách nói gì, Phản biện, Viết tiếp, Chốt |

Mở tiết không bao giờ hiện đáp án đúng. Ôn bài: ít nhất một lựa chọn dựa trên hiểu lầm phổ biến, ghi trong `gv_hieu_lam`. Sách là Thầy: chỉ dùng chi tiết sách khi Thầy Cô cung cấp hoặc sách rất phổ biến và Claude chắc chắn; không chắc thì ghi vị trí theo chương hoặc đoạn và dặn Thầy Cô đối chiếu.

## Trường JSON
Bắt buộc mọi loại: `phien_ban` ("1.0"), `loai`, `tieu_de`, `mon`, `lop` (chuỗi), `nhom_lop` (A đến E), `nhom_mon`, `bai`, `pham_chat`, `loi_ke`, `lua_chon`. Bài ngoại ngữ thêm `ngoai_ngu`. Xem `nhom-lop.md`, `nhom-mon.md`, `doc-ngoai-ngu.md`, `quy-tac-vietwise.md`.
Nên có: `thoi_luong_phut`, `kien_thuc` (mảng), `nhan_vat` ([{"ten"}]), `du_kien` (mảng nhãn ngắn), `cach_chon`, `cau_hoi_goi_mo` (mảng), `loi_chot`, `du_an_that`, `gv_ghi_chu`, `chau_ngoc` (hieu-ky, thich-nghi, ben-chi, an-lac).

| Trường | Kiểu | Ghi chú |
| --- | --- | --- |
| `lua_chon` | mảng 2 đến 4: `{ma, noi_dung, gv_cai_gia}` hoặc `{ma, noi_dung, gv_kien_thuc}` | `ma` là A, B, C. Mỗi lựa chọn có lý do hợp lý |
| `buoc_ngoat`, `cau_hoi_treo`, `quay_lai_cuoi_tiet` | chuỗi | Chỉ `mo-tiet`. `quay_lai_cuoi_tiet` là của Thầy Cô |
| `cau_mau_phan_bien` | mảng chuỗi | `on-bai`, `sach-la-thay` |
| `so_do_chot` | mảng `{kien_thuc, dung_vao}` | Kiến thức đã dùng, dùng vào lựa chọn nào |
| `gv_goi_y_lua_chon_d`, `gv_hieu_lam` | chuỗi, mảng | Chỉ Thầy Cô thấy |
| `sach` | `{ten, tac_gia, phan_doc, nguon_noi_dung}` | `sach-la-thay`. `nguon_noi_dung`: "gv-cung-cap" hoặc "claude-biet-ro" |
| `chia_khoa` | mảng 3 đến 5 `{cau_hoi, trang, gv_goi_y}` | Câu chỉ người đã đọc mới trả lời được; không chấm |
| `hinh_minh_hoa` | chuỗi SVG ≤ 3000 ký tự | Hình minh họa cảnh của lời kể, hiện ở bước Kể |
| `viet_tiep` | chuỗi | Lời mời "Nếu em là tác giả..." |
| `level` | mảng 1 đến 4 `{so, ten, nhiem_vu, goi_y[], gv_danh_cho, gv_dap_an}` | Chỉ khi Thầy Cô chọn level. `so` 1 đến 4; `ten` mặc định Làm quen, Vững bước, Vận dụng, Sáng tạo. Xem `nhom-lop.md` mục Bốn level. Trình chơi thêm bước "Chọn level" (mở tiết: sau Nói lý do; ôn bài: sau Chứng cứ; Sách là Thầy: sau Sách nói gì) |
| `noi_dung_phu` | `{chu_de, ten_buoc, loi_moi, cau_hoi[], gv_y_do}` | Chỉ khi Thầy Cô ghi nội dung phụ. `ten_buoc` là tên bước học sinh thấy (mặc định "Ngẫm thêm"), đặt trước bước cuối. `cau_hoi` 2 đến 3 câu mở, không đáp án. `gv_y_do`: ý Thầy Cô và lưu ý tôn trọng |

Không dùng `tuong_tac`, `boi_canh`, `sprite` (trình chơi nhẹ bỏ qua). Xem ví dụ trong `vi-du/` và bắt chước đúng cấu trúc. Game có 4 level và nội dung phụ: `vi-du/on-bai-khtn9-lipid-carbohydrate-protein-4-level.json`.

## Nội dung phụ của Thầy Cô
Thầy Cô có thể ghi thêm một chủ đề ngoài kiến thức (ví dụ "ý chí tự do, quyền chọn về học, ăn thuận tự nhiên"; "lương tâm khi dùng kiến thức"). Cách lồng:
1. Lời kể có sẵn một khoảnh khắc nhân vật được tự chọn ("Không ai bắt Minh phải ăn gì"), không biến thành bài giảng.
2. Bước `noi_dung_phu`: một lời mời ngắn và 2 đến 3 câu hỏi mở về lựa chọn của chính học sinh, cách dùng kiến thức có lương tâm. Không có đáp án đúng, không chấm.
3. Câu chốt (`loi_chot`) nối kiến thức với quyền tự chọn.
4. `gv_y_do`: nhắc tôn trọng mọi lựa chọn, không phán xét hoàn cảnh gia đình, học sinh được viết riêng không cần chia sẻ.
Không viết điều chưa chắc đúng về sức khỏe, tôn giáo, tâm linh; đặt dưới dạng câu hỏi để học sinh tự nghĩ.

## Phẩm chất ngầm (không phát huy hiệu, không chấm)
Phẩm chất CT GDPT 2018: yêu nước, nhân ái, chăm chỉ, trung thực, trách nhiệm. Bốn viên ngọc Vietwise nuôi ngầm: Hiếu kỳ, Thích nghi, Bền chí, An lạc. Chọn một phẩm chất bám tình huống, viết bằng lời học sinh hiểu.
