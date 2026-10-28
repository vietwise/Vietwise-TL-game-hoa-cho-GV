# Đặc tả game — Trợ lý game hóa cho giáo viên

Phiên bản đặc tả: **1.0** (27/10/2026, thêm kiểu tương tác và bộ nhận diện) · Áp dụng cho `schema/game-spec.schema.json` phiên bản `"1.0"`.

Tài liệu này dành cho ba nhóm người: **người viết skill/nội dung** (Claude và người soạn), **người vẽ ảnh**, và **đội Edubit**. Khi tài liệu này và schema khác nhau, schema là bản chuẩn cho dữ liệu, còn tài liệu này là bản chuẩn cho hành vi và hình ảnh.

---

## 1. Nguyên tắc chung (áp dụng cho mọi loại game)

1. **Không thi đua, không chấm điểm.** Không có điểm số, đội, bảng xếp hạng, thắng thua hay âm thanh "đúng/sai".
2. **Cả lớp chơi cùng lúc trên một màn hình chiếu.** Học sinh không cần thiết bị riêng. Giáo viên điều khiển bằng bàn phím hoặc chuột.
3. **Bốn trụ cột nội dung:** tình huống thực tế, một quyết định cần chọn, một phẩm chất đi kèm, và một kết nối với bài học. Game 1 kết nối bằng sự tò mò, Game 2 bằng chứng cứ.
4. **Claude chỉ viết nội dung (JSON).** Ảnh, trình chơi và khung dữ liệu nằm cố định trong repo, nên Claude bản miễn phí vẫn ra được game ổn định.
5. **Tách nội dung học sinh và nội dung giáo viên.** Mọi trường bắt đầu bằng `gv_` chỉ hiện ở chế độ giáo viên.

## 2. Luồng sử dụng 3 bước

| Bước | Giáo viên | Hệ thống |
| --- | --- | --- |
| 1. Yêu cầu tạo game | Gõ một câu: loại game, môn, lớp, bài, sĩ số, thời lượng | Skill hỏi lại một lần nếu thiếu thông tin quan trọng |
| 2. Nhận kết quả | Đọc thẻ hướng dẫn, sao chép khối JSON, nhờ sửa nếu cần | Claude xuất thẻ hướng dẫn và một khối JSON hợp lệ theo schema |
| 3. Nhận game trên Edubit | Phương án A: không làm gì. Phương án B: dán JSON vào Edubit | Edubit kiểm tra JSON theo schema, dựng game bằng trình chơi và trả link |

---

## 3. Game loại 1 — Game mở tiết (`"loai": "mo-tiet"`)

**Mục tiêu:** trong 10 phút đầu tiết, khơi sự tò mò cho bài **chưa học**. Kết thúc bằng một câu hỏi treo mà bài học hôm đó sẽ trả lời.

| # | Bước | Phút | Màn hình hiển thị | Trường JSON | Giáo viên | Học sinh |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Kể | 1 | Ảnh nền, nhân vật, lời kể, dữ kiện dạng nhãn | `boi_canh`, `nhan_vat`, `loi_ke`, `du_kien` | Đọc to lời kể | Nghe |
| 2 | Chọn | 2 | 2–3 thẻ úp, bấm vào thì lật ra lựa chọn | `lua_chon[].ma`, `lua_chon[].noi_dung`, `cach_chon` | Lật và đọc từng thẻ | Chọn cùng lúc, im lặng |
| 3 | Nói lý do | 3 | Danh sách câu hỏi gợi mở | `cau_hoi_goi_mo` (mặc định 3 câu chung) | Mời 1–2 em mỗi lựa chọn, không phán đúng sai | Nói, nghe, được đổi ý |
| 4 | Bước ngoặt | 2 | Chi tiết mới bị làm mờ, bấm vào thì hiện; các thẻ đã lật | `buoc_ngoat` | Bấm để hiện, hỏi "Em có chọn lại không?" | Chọn lại |
| 5 | Câu hỏi của hôm nay | 2 | Khung viền đứt nét có câu hỏi treo, bên dưới là câu hỏi về phẩm chất | `cau_hoi_treo`, `loi_chot` | Ghi lên góc bảng, rồi vào bài | Ghi vào vở |

- Nút cuối là **"Vào bài"**, bấm vào thì trình chơi đóng.
- `quay_lai_cuoi_tiet` chỉ hiện ở chế độ giáo viên, để giáo viên dùng trong 2 phút cuối tiết.
- Không bao giờ hiện đáp án đúng. Các con số đã tính sẵn nằm trong `gv_ghi_chu`.

## 4. Game loại 2 — Game ôn bài (`"loai": "on-bai"`)

**Mục tiêu:** học sinh dùng kiến thức **đã học** để bảo vệ một lựa chọn bằng chứng cứ, phản biện lẫn nhau, rồi tự đề xuất một lựa chọn tốt hơn. Quyết định vẫn để mở, nhưng kiến thức sai thì phải được sửa ở bước chốt.

| # | Bước | Phút | Màn hình hiển thị | Trường JSON | Giáo viên | Học sinh |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Kể | 1 | Như Game 1 | `boi_canh`, `nhan_vat`, `loi_ke`, `du_kien` | Đọc, chỉ vào dữ kiện | Nghe, ghi dữ kiện |
| 2 | Chọn | 2 | Thẻ úp, lật ra lựa chọn | `lua_chon`, `cach_chon` | Lật và đọc thẻ | Chọn cá nhân |
| 3 | Chứng cứ | 4 | Khung 3 ô Chọn – Chứng cứ – Lập luận, câu hỏi gợi mở, danh sách lựa chọn dạng gọn | `cau_hoi_goi_mo`, `lua_chon` | Phát thẻ lập luận, đi quanh lớp | Làm theo cặp, mở vở hoặc SGK |
| 4 | Phản biện | 4 | Câu mẫu phản biện riêng của game, cộng 2 câu chung | `cau_mau_phan_bien` | Mời 2–3 cặp, chỉ hỏi thêm | Chất vấn lập luận, không chất vấn người |
| 5 | Sáng tạo | 2 | Các thẻ A–C đã lật và thẻ D "Lựa chọn của lớp mình" | `gv_goi_y_lua_chon_d` (chỉ giáo viên) | Hỏi "Có lựa chọn D nào tốt hơn không?" | Đề xuất, giải thích bằng kiến thức |
| 6 | Chốt kiến thức | 2 | Sơ đồ kiến thức → dùng vào đâu, kèm câu hỏi phẩm chất | `so_do_chot`, `loi_chot`, `gv_hieu_lam` (chỉ giáo viên) | Sửa mọi chứng cứ sai về kiến thức | Ghi sơ đồ vào vở |

- Nút cuối là **"Kết thúc"**.
- Mỗi lựa chọn nên có `gv_kien_thuc`, ghi kiến thức nào bảo vệ hoặc bác bỏ lựa chọn đó.
- Ít nhất một lựa chọn phải dựa trên một hiểu lầm phổ biến, và hiểu lầm đó được ghi trong `gv_hieu_lam`.

## 4A. Game loại 3 — Sách là Thầy (`"loai": "sach-la-thay"`)

**Mục tiêu:** học sinh **phải đọc một cuốn sách** (hoặc một phần sách) trước buổi chơi thì mới chơi được, và **phải hiểu sách** thì mới bảo vệ được lựa chọn. Sách trở thành "người thầy": chứng cứ lấy từ chi tiết trong sách, rồi đem bài học của sách vào một tình huống thật của học sinh. Không thi đua, không chấm điểm, kể cả phần kiểm tra đã đọc.

**Hai lớp hiểu:** (1) *hiểu chuyện*: nhân vật làm gì, vì sao, hệ quả ra sao; (2) *hiểu bài học*: đem điều sách dạy vào đời mình. Phần Chìa khoá sách lo lớp (1), các bước sau lo lớp (2).

| # | Bước | Phút | Màn hình hiển thị | Trường JSON | Giáo viên | Học sinh |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Chìa khoá sách | 3 | Tên sách và 3–5 câu chỉ người đã đọc mới trả lời được. Chạm câu nào thì hiện "Mở sách: chương/đoạn" | `sach`, `chia_khoa` | Hỏi từng câu, mời nhiều em nhớ lại. Chưa ai nhớ thì cả lớp mở sách đọc đoạn đó | Nhớ lại, kể bằng lời mình |
| 2 | Kể | 1 | Tình huống thật của học sinh, giống tình huống trong sách | `loi_ke`, `du_kien`, `boi_canh`, `nhan_vat` | Đọc | Nghe |
| 3 | Chọn | 2 | Thẻ úp A/B/C | `lua_chon`, `cach_chon` | Lật thẻ | Chọn cá nhân |
| 4 | Sách nói gì | 4 | Khung Chọn – Chi tiết trong sách – Lập luận | `cau_hoi_goi_mo` | Đi quanh lớp, hỏi "ở đoạn nào?" | Theo cặp, mở sách tìm chi tiết |
| 5 | Phản biện | 4 | Câu mẫu phản biện | `cau_mau_phan_bien` | Mời 2–3 cặp | Chất vấn lập luận bằng chi tiết sách |
| 6 | Viết tiếp | 3 | Lời mời "Nếu em là tác giả…" và thẻ D | `viet_tiep`, `gv_goi_y_lua_chon_d` | Mời ý sáng tạo | Đề xuất kết thúc khác hoặc lựa chọn D |
| 7 | Chốt bài học | 3 | Sơ đồ chi tiết sách → dùng vào đời, câu phẩm chất, việc thật tuần này, soi gương | `so_do_chot`, `loi_chot`, `du_an_that` | Sửa chỗ hiểu sai về sách | Ghi sơ đồ, nhận việc thật |

- Tổng mặc định **20 phút**. Hợp với tiết Đọc mở rộng, tiết Ngữ văn, sinh hoạt lớp, hoặc câu lạc bộ đọc sách.
- **Thật thà về nội dung sách:** Claude chỉ dùng chi tiết khi chắc chắn (sách rất phổ biến, ghi `nguon_noi_dung: "claude-biet-ro"`) hoặc khi giáo viên dán đoạn/tóm tắt (`"gv-cung-cap"`). Không bịa chi tiết, không bịa số trang: nếu không chắc thì ghi vị trí theo chương hoặc đoạn, và ghi chú giáo viên đối chiếu. Trích dẫn tối đa một hai câu ngắn, không chép dài nội dung sách.
- **Đã đọc chưa?** Không dùng điểm để ép đọc. Game tự đòi đọc vì chứng cứ phải lấy từ sách. Em chưa đọc vẫn ngồi cùng cặp và được mở sách trong lớp.
- Giao sách trước ít nhất một tuần, chia phần đọc vừa sức (tiểu học: 1 truyện ngắn hoặc 1–2 chương; THCS: 2–4 chương).

## 5. Thời lượng

Nhịp mặc định: Game 1 tổng **10 phút**, Game 2 tổng **15 phút**, Game 3 tổng **20 phút**. Nếu có `ba_nhip`, thêm bước Lặng 30 giây ở đầu, nằm trong tổng thời lượng. Khi có `thoi_luong_phut`, trình chơi chia lại thời gian theo tỉ lệ, làm tròn đến 0,5 phút, mỗi bước tối thiểu 0,5 phút. Đồng hồ chỉ đếm ngược và nhấp nháy khi hết giờ, không có âm thanh và không tự sang bước.

---

## 6. Đặc tả dữ liệu (JSON)

Bản chuẩn nằm ở `schema/game-spec.schema.json`. Cột "Ai thấy" cho biết trường đó hiện cho học sinh (HS) trên màn chiếu hay chỉ hiện ở chế độ giáo viên (GV).

| Trường | Kiểu | Bắt buộc | Giới hạn | Ai thấy | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| `phien_ban` | chuỗi | cả hai | `"1.0"` | — | Tăng khi khung đổi kiểu không tương thích |
| `loai` | chuỗi | mọi loại | `mo-tiet` \| `on-bai` \| `sach-la-thay` | HS | |
| `tieu_de` | chuỗi | cả hai | ≤ 60 ký tự | HS | Tên ngắn, gợi tò mò |
| `mon`, `lop`, `bai` | chuỗi | cả hai | | HS | Hiện ở đầu màn hình |
| `thoi_luong_phut` | số nguyên | không | 5–45 | HS | |
| `kien_thuc` | mảng chuỗi | Game 2 | ≤ 4 | GV | Game 1: yêu cầu cần đạt sẽ mở. Game 2: ý được ôn |
| `pham_chat` | chuỗi | cả hai | 1 phẩm chất | GV | yêu nước, nhân ái, chăm chỉ, trung thực, trách nhiệm, hoặc giá trị gần |
| `boi_canh` | id ảnh | không | `nhom = background` | HS | |
| `nhan_vat[]` | `{ten, sprite?}` | không | ≤ 3 | HS | `sprite` là id có `nhom = sprite` |
| `loi_ke` | chuỗi | cả hai | Game 1 ≤ 120 chữ, Game 2 ≤ 150 chữ | HS | |
| `du_kien` | mảng chuỗi | không | ≤ 6, mỗi mục ngắn | HS | Số liệu, điều kiện cần nhìn thấy |
| `lua_chon[]` | `{ma, noi_dung, gv_cai_gia?, gv_kien_thuc?}` | cả hai | 2–3, `ma` là A/B/C, `noi_dung` ≤ 140 ký tự | HS (trừ `gv_`) | |
| `cach_chon` | chuỗi | không | | HS | Ví dụ: "giơ thẻ màu" |
| `cau_hoi_goi_mo` | mảng chuỗi | không | ≤ 4 | HS | |
| `buoc_ngoat` | chuỗi | Game 1 | | HS | Game 2 dùng trong bản mở rộng, chỉ hiện ở chế độ giáo viên |
| `cau_hoi_treo` | chuỗi | Game 1 | 1 câu | HS | Bài hôm đó phải trả lời được |
| `cau_mau_phan_bien` | mảng chuỗi | không | ≤ 4 | HS | Game 2 |
| `so_do_chot[]` | `{kien_thuc, dung_vao}` | Game 2 | ≤ 5 | HS | |
| `loi_chot` | chuỗi | không | 1 câu hỏi | HS | Gọi tên phẩm chất, không kết luận |
| `quay_lai_cuoi_tiet` | chuỗi | không | | GV | Game 1 |
| `gv_goi_y_lua_chon_d` | chuỗi | không | | GV | Game 2 |
| `gv_hieu_lam` | mảng chuỗi | không | | GV | Game 2 |
| `gv_ghi_chu` | chuỗi | không | | GV | Ví dụ: đáp số đã tính sẵn |
| `sach` | `{ten, tac_gia, phan_doc, nguon_noi_dung?}` | Game 3 | | HS | `nguon_noi_dung`: `gv-cung-cap` \| `claude-biet-ro` |
| `chia_khoa[]` | `{cau_hoi, trang, gv_goi_y?}` | Game 3 | 3–5 | HS (trừ `gv_`) | Chỉ người đã đọc mới trả lời được |
| `viet_tiep` | chuỗi | không | ≤ 200 ký tự | HS | Game 3 |
| `chau_ngoc` | chuỗi | không | `hieu-ky` \| `thich-nghi` \| `ben-chi` \| `an-lac` | GV | Viên ngọc game nuôi ngầm (mục 14) |
| `ba_nhip` | `{biet_on, tu_thoai?}` | không | | HS | 30 giây: ba nhịp thở, một câu biết ơn, một câu tự nói |
| `du_an_that` | chuỗi | không | ≤ 240 ký tự | HS | Game 2, 3: việc thật 10–15 phút ngoài giờ |
| `tuong_tac[]` | xem mục 12 | không | ≤ 2 | HS | |

Quy tắc khác:

- Không được có trường ngoài danh sách trên (`additionalProperties: false`). Trình chơi và Edubit từ chối JSON có trường lạ.
- Mọi id ảnh phải có trong `assets/manifest.json`. Nếu id không tồn tại, trình chơi vẫn chạy nhưng bỏ ảnh đó và báo ở chế độ giáo viên.
- Văn bản là tiếng Việt có dấu, dạng Unicode NFC, không chứa HTML hay Markdown. Trình chơi hiển thị nguyên văn.
- Trường tuỳ chọn `tuong_tac` (tối đa 2 mục) thêm kiểu tương tác, xem mục 12.
- Ví dụ đầy đủ: `examples/mo-tiet-toan5-ti-so-phan-tram.json` (chia nguồn lực, đoán chữ), `examples/mo-tiet-khoahoc5-tiet-kiem-dien.json` (xếp ưu tiên, con đường) và `examples/on-bai-khoahoc4-nuoc.json` (xếp nhóm, pha ý).

---

## 7. Đặc tả tài nguyên ảnh

### 7.1 Nhóm ảnh và kích thước

| Nhóm (`nhom`) | Thư mục | Định dạng | Kích thước khuyến nghị | Cách trình chơi dùng |
| --- | --- | --- | --- | --- |
| `background` | `assets/backgrounds/` | JPG/WebP hoặc SVG | 1920 × 1080 (16:9), ≤ 400 KB | Phủ kín khung kể chuyện. Nửa phải bị phủ tối và che bởi ô lời kể, nên chi tiết quan trọng đặt ở **nửa trái** |
| `sprite` | `assets/sprites/` | WebP hoặc PNG nền trong, hoặc SVG | Cao 900–1200 px, chân chạm mép dưới, cắt sát, ≤ 300 KB | Đứng ở góc trái dưới, cao khoảng 42% màn hình, tên nhân vật ghi dưới chân |
| `card` | `assets/cards/` | PNG/WebP hoặc SVG | 1200 × 900 (4:3), ≤ 200 KB | Mặt sau của thẻ lựa chọn, căn giữa và phủ kín. Họa tiết chính nằm trong **vùng an toàn 70% ở giữa**, vì mép có thể bị cắt khi thẻ đổi kích thước |

Mặt trước thẻ do trình chơi tự vẽ bằng màu thương hiệu (mục 13), gồm A Cam, B Xanh Vườn, C Blue và D Vàng, nên không cần vẽ.

### 7.2 Phong cách

- Dễ nhìn từ cuối lớp: nét rõ, tương phản cao, ít chi tiết nhỏ, không có chữ trong ảnh (trừ ảnh tạm).
- Nhân vật là người Việt, nhiều độ tuổi, giới tính và vùng miền. Trang phục đời thường hoặc đồng phục học sinh. Không nhân vật nào gắn với khuyết điểm hay hoàn cảnh khó khăn.
- Bối cảnh là nơi học sinh Việt Nam quen thuộc, ví dụ lớp học, sân trường, chợ, cửa hàng, nhà, bếp, đường phố, công viên, ruộng, suối, bờ biển.
- Lưng thẻ dùng một bộ thống nhất cho mọi game. Có thể có biến thể theo cấp học, mỗi biến thể một id.

### 7.3 Đặt tên và manifest

- Tên tệp và `id` chỉ dùng chữ thường không dấu, số và dấu gạch ngang, ví dụ `hs-nu-thcs`, `nen-cho-que`.
- **`id` không bao giờ đổi hoặc xoá** sau khi đã có game dùng nó. Muốn thay hình thì đổi `tep` và giữ nguyên `id`.
- Mỗi ảnh có một dòng trong `assets/manifest.json`:

| Trường | Ý nghĩa |
| --- | --- |
| `id` | Mã ổn định để JSON game trỏ tới |
| `nhom` | `background` \| `sprite` \| `card` |
| `tep` | Đường dẫn tương đối từ `assets/` |
| `mo_ta` | Mô tả bằng lời thường. Claude chọn ảnh dựa vào mô tả này, nên ghi rõ ai/cái gì, tư thế, cảm xúc |
| `lua_tuoi` | Một hoặc nhiều giá trị: `mam-non`, `tieu-hoc`, `thcs`, `thpt`, `tat-ca` |
| `chu_de` | Thẻ chủ đề, ví dụ `truong-hoc`, `mua-ban`, `thien-nhien`, `gia-dinh` |
| `tam` | `true` nếu là ảnh tạm, sẽ được thay |

### 7.3A Bộ linh vật Bé Não (`assets/sprites/nao/`)

16 sprite Bé Não do Vietwise cung cấp (27/10/2026), WebP nền trong, cao 900 px. Dùng làm nhân vật dẫn chuyện hoặc nhân vật đi kèm phẩm chất. Không dùng như huy hiệu phát cho học sinh.

| id | Huy chương | Gợi ý dùng |
| --- | --- | --- |
| `nao-vay-tay` | không có | Dẫn chuyện, chào lớp |
| `nao-hieu-ky`, `nao-thich-nghi`, `nao-ben-chi`, `nao-an-lac` | Bốn viên ngọc | Khớp với `chau_ngoc` của game |
| `nao-iq`, `nao-eq`, `nao-sq`, `nao-pq` | Bốn trí thông minh | Game chạm logic, cảm xúc, tâm linh, thể chất |
| `nao-toan-do`, `nao-phan-do`, `nao-phan-hoi` | Ba luật tác tạo | Bước làm chung cả lớp, làm cặp, phản biện |
| `nao-guong-than` | Gương thần | Bước soi gương cuối buổi |
| `nao-dua-than`, `nao-quat-than`, `nao-tham-than` | Đồ phép | Sáng tạo, viết tiếp, con đường |

### 7.4 Bộ ảnh tối thiểu cho ngày ra mắt 20.11

| Nhóm | Số lượng | Nội dung |
| --- | --- | --- |
| `card` | 1 | Lưng thẻ chung |
| `sprite` | 8 | Nam và nữ cho mỗi cấp mầm non, tiểu học, THCS, THPT |
| `sprite` | 4 | Giáo viên nam, giáo viên nữ, phụ huynh, người bán hàng |
| `background` | 6 | Lớp học, sân trường, chợ hoặc cửa hàng, nhà hoặc bếp, đường phố, thiên nhiên (suối, công viên) |

---

## 8. Trình chơi (`player/index.html`)

- **Nạp game:** dán JSON vào ô nhập (chấp nhận cả khối có rào ```` ```json ````), hoặc dùng tham số `?spec=<url>`. Tham số tuỳ chọn `&assets=<url thư mục assets/>` cho trường hợp ảnh nằm ở nơi khác.
- **Kiểm tra:** khi JSON thiếu trường bắt buộc hoặc sai `loai`, trình chơi báo lỗi bằng tiếng Việt và không mở game.
- **Điều khiển:** ← → chuyển bước, phím cách bật hoặc dừng đồng hồ, G bật chế độ giáo viên, F bật toàn màn hình. Có nút bấm tương ứng cho màn hình cảm ứng.
- **Chữ:** lời kể và câu hỏi tối thiểu 24 px trên màn hình 1366 × 768. Có bố cục riêng cho màn hình hẹp (≥ 360 px).
- **Không phụ thuộc bên ngoài:** một file HTML, không dùng thư viện. Font Quicksand và Nunito đóng gói sẵn trong `assets/fonts/` (giấy phép SIL OFL), không gọi Google Fonts. Ảnh tải qua manifest, và nếu không tải được thì game vẫn chạy không có ảnh, chữ dùng font hệ thống.
- **Chuyển động nhẹ:** khi máy bật chế độ giảm chuyển động (`prefers-reduced-motion`), thẻ lật không có hiệu ứng và đồng hồ không nhấp nháy.
- **Kiểm thử:** chạy qua mọi bước của các game mẫu ở 1440 × 900 và 390 × 844, không tràn ngang, không lỗi console.
- **Không ghi dữ liệu học sinh.** Chỉ lưu JSON game gần nhất trong bộ nhớ của trình duyệt, để tiện mở lại.

## 9. Tích hợp Edubit

| Phương án | Edubit cung cấp | Hợp đồng dữ liệu |
| --- | --- | --- |
| A. Connector (MCP) | Một công cụ `dang_game` | Đầu vào: JSON game. Edubit kiểm tra theo schema 1.0, trả về `{ link, id_game }` hoặc danh sách lỗi bằng tiếng Việt để Claude tự sửa |
| B. Trang dán JSON | Một trang "Tạo game từ Claude" | Ô dán, nút Xem trước (chạy trình chơi) và nút Đăng (trả link) |

**Cách nhúng đã biết của Edubit:** trong builder.edubit.vn chọn Thêm mới → **Nhúng HTML** (có ba tab HTML, CSS, JS). Không dùng khối HTML thường vì nó bỏ thẻ `<script>`. CSS phải gói dưới một id gốc (ví dụ `#game-root`) để không đè giao diện trang. CSS hoặc JS dài có thể đặt ở Cài đặt trang → Custom CSS/JS. Kích thước khối gợi ý: máy tính 1200 × 1800, máy tính bảng 768 × 1800, điện thoại 420 × 2300. Việc cần làm tiếp: tách `player/index.html` thành ba phần HTML, CSS, JS với CSS gói dưới id gốc, để dán thẳng vào khối Nhúng HTML.

Ở cả hai phương án, Edubit chạy trình chơi của repo, hoặc một bản sao giữ đúng hành vi ở mục 3 đến 5 và mục 8. Ảnh nên tải qua đường dẫn ghim theo phiên bản repo, ví dụ thẻ `v1.0`, để game cũ không đổi khi repo cập nhật.

## 10. Phiên bản và thay đổi

- Thêm trường tuỳ chọn hoặc thêm ảnh: không đổi `phien_ban`.
- Đổi tên trường, bỏ trường, hoặc đổi trường tuỳ chọn thành bắt buộc: tăng `phien_ban` (ví dụ `"2.0"`). Trình chơi phải đọc được mọi phiên bản còn hỗ trợ.
- Thêm loại game mới (loại 4 trở đi): thêm giá trị vào `loai`, thêm nhịp bước ở mục 3–4 và trong trình chơi, cùng ít nhất một ví dụ trong `examples/`.

## 11. Kiểm tra chất lượng nội dung (trước khi đăng)

- [ ] Nếu có `tuong_tac`: kiểu tương tác giúp lớp suy nghĩ về quyết định, không biến thành câu đố có một đáp án đúng.

- [ ] Đủ bốn trụ cột: tình huống, quyết định, phẩm chất, và kết nối bài học (tò mò hoặc chứng cứ).
- [ ] Quyết định có sức căng thật: mỗi lựa chọn đều có lý và đều có cái giá.
- [ ] Game 1: câu hỏi treo được bài hôm đó trả lời. Game 2: mỗi lựa chọn chỉ bảo vệ hoặc bác bỏ được bằng kiến thức đã học.
- [ ] Mọi con số đã được tính lại, kiến thức đúng chương trình và đúng thuật ngữ SGK.
- [ ] Không có điểm, đội hay thắng thua. Không có tình huống gây tổn thương. Không dùng tên học sinh thật.
- [ ] JSON hợp lệ theo schema, mọi id ảnh có trong manifest.

---

## 12. Kiểu tương tác (mượn từ 20 trò Hạt Mầm)

Bộ skill tham khảo thư viện 20 trò của dự án "Game giáo dục cho giáo viên" (Hạt Mầm) để có thêm cách cho lớp tương tác, ngoài giơ thẻ A/B/C. Mỗi cơ chế được **đổi mục đích**: từ "tìm đáp án đúng" sang "làm rõ quyết định và cái giá". Trình chơi không chấm, không đếm điểm.

Mỗi game có thể thêm tối đa **2** kiểu qua trường `tuong_tac`. Mỗi kiểu là một bước riêng, chèn vào vị trí cố định. Tổng thời lượng vẫn bằng `thoi_luong_phut`, các bước khác tự co lại.

| `kieu` | Mượn từ trò | Lớp làm gì | Chèn ở đâu | Dùng cho |
| --- | --- | --- | --- | --- |
| `lat-du-kien` | Lật thẻ trí nhớ, Truy tìm hoá thạch | Lật từng manh mối, sau mỗi thẻ hỏi "có ai đổi ý không?" | Sau Kể | Cả hai |
| `xep-uu-tien` | Vườn chữ diệu kỳ, Du hành vũ trụ | Chạm theo thứ tự ưu tiên, so thứ tự giữa các nhóm | Sau Chọn | Cả hai |
| `chia-nguon-luc` | Thành phố xanh, Bếp bánh phân số | Chia một ngân sách (tiền, thời gian) bằng nút + −, thấy cái giá | Sau Chọn | Cả hai, hợp Toán |
| `phan-nhom` | Biệt đội phân loại, Dọc miền đất Việt, Nông trại tí hon | Xếp mục vào 2–3 nhóm, giải thích vì sao | Sau Chọn | Cả hai, hợp Game 2 (xếp chứng cứ) |
| `con-duong` | Đường về nhà | Đi 2–3 chặng, mỗi chặng chọn một ngả và xem hệ quả | Trước Bước ngoặt (Game 1) hoặc Phản biện (Game 2) | Cả hai |
| `doan-hinh` | Đuổi hình bắt chữ, Mật mã kho báu | Từ 2–3 manh mối đoán từ khoá bài hôm nay | Trước Câu hỏi của hôm nay | Chỉ Game 1 |
| `pha-tron` | Phòng pha màu, Kỹ sư xây cầu | Chọn hai mảnh kiến thức, ghép thành ý tưởng mới | Trước Sáng tạo | Chỉ Game 2 |

**Không mượn:** Đua thuyền ngày hội và Ô ăn quan (có đội, có thắng thua). Nhịp điệu vui, Sudoku sắc màu, Phố đèn lồng, Xưởng khối hình (luyện tập có một đáp án đúng, không có quyết định). Giáo viên vẫn có thể dùng các trò này ở Hạt Mầm như hoạt động khởi động riêng.

**Gợi ý chọn kiểu cho Claude:**

- Tình huống có nhiều thông tin: `lat-du-kien`, để lớp thấy quyết định thay đổi khi biết thêm.
- Tình huống có tiền, thời gian, vật liệu có hạn: `chia-nguon-luc`.
- Tình huống có nhiều việc cần làm trước sau: `xep-uu-tien`.
- Game 2 cần phân biệt kiến thức nào bảo vệ lựa chọn nào: `phan-nhom`.
- Quyết định kéo theo hệ quả qua nhiều bước, hoặc phẩm chất thể hiện qua cách hành xử: `con-duong`.
- Bài mới có một từ khoá gọi tên được: `doan-hinh`.
- Game 2 muốn học sinh sáng tạo lựa chọn D: `pha-tron`.
- Không bắt buộc. Game 10 phút chỉ nên có 1 kiểu.

## 13. Nhận diện hình ảnh (bộ màu, font Vườn Game-học Vietwise)

Theo wiki "Bộ Màu Vườn Game-Học Vietwise". Chỉ dùng **6 màu** và trắng. Muốn nhạt hay đậm hơn thì dùng `rgba()` của 6 màu này, không thêm mã màu mới. Màu đen chỉ dùng trong bóng đổ.

| Màu | Mã | Vai trò trong trình chơi |
| --- | --- | --- |
| Blue | `#0018F9` | Giọng chính: tiêu đề, số, kiến thức, bước đang chọn. Chữ thân bài là Blue 72% |
| Cam | `#F96726` | Cảm xúc, lời mời, tên riêng: câu gọi tên phẩm chất, hệ quả trên con đường, thẻ A |
| Vàng | `#F9C12D` | Nút chính (chữ Blue), màu khi rê chuột lên mọi nút, bút dạ quang nửa dòng, thẻ D |
| Xanh Vườn | `#4E9F2E` | Nhãn mục chữ hoa, viền tiêu điểm bàn phím, chế độ giáo viên, thẻ B |
| Đỏ | `#DF0000` | Chỉ báo lỗi, dùng rất ít |
| Kem | `#FFFEF3` | Nền trang, chữ trên nền đậm |

- **Font:** Quicksand 500 cho tiêu đề, nút, nhãn và số. Nunito 400 cho thân bài. Không in đậm nặng, không in nghiêng.
- **Thứ tự màu cho nhóm hoặc chặng:** Cam → Xanh Vườn → Blue → Vàng → Đỏ (Đỏ đứng cuối vì Đỏ còn mang nghĩa lỗi).
- **Bo góc** (theo Hạt Mầm): thẻ 12 px, khung kể chuyện 17 px, nút 8 px.
- **Tương phản:** chữ trên thẻ màu từ 24 px trở lên. Chữ trên Vàng dùng Blue, không dùng trắng.
- **Ảnh vẽ** nên dùng cùng 6 màu này làm màu chủ đạo để khớp với trình chơi.

## 14. Nền Vietwise cài ngầm trong mọi game

Bộ game giáo viên mang triết lý của Vườn Game-học Vietwise (founder Lê Nhất Phương Hồng), nhưng **cài ngầm**: học sinh không nghe giảng về triết lý, các em gặp nó qua cách game vận hành. Nguồn: wiki game-học (Chuẩn Game-Học Tác Tạo, SPARK, Tâm Lý Học Theo Độ Tuổi) và vietwise.edu.vn.

| Nền | Ý chính | Hiện trong game giáo viên ở đâu |
| --- | --- | --- |
| Quặng mỏ châu ngọc | Mỗi học sinh là một mỏ ngọc, giáo dục để lộ ra, không phải để chấm | Không có đáp án đúng cho quyết định. Mọi lý do đều được nghe |
| Giáo dục Tác Tạo, We Are One | Hợp nhất không phải đồng nhất. Học bằng việc thật, đối thoại cởi mở, không chứng minh người khác sai | Bước Phản biện: "hỏi vào lập luận, không hỏi vào người". Việc thật tuần này |
| Ba luật tác tạo | Toàn đồ (không xếp hạng, phần chung lớn lên), Phân đồ (đổi theo người học), Phản hồi (có bài học, ôn lại sau) | Không đội, không điểm. Ba mức gợi ý theo lớp. Câu "quay lại cuối tiết" và ôn ở buổi sau |
| SPARK | S kết nối tâm linh, P dự án có ý nghĩa và cùng vui, A thể hiện bản thân, R quan hệ (bắt đầu từ làm bạn với chính mình), K hiếu kỳ khám phá | S: bước Lặng. P: việc thật. A: lựa chọn D, viết tiếp. R: làm theo cặp, soi gương. K: câu hỏi treo, chìa khoá sách. Mỗi game chạm ít nhất 3 chữ, Game 3 chạm đủ 5 |
| 5P | Mục đích → Nguồn lực → Nguyên tắc → Hiện thực → Nhân bản | Kể (mục đích) → dữ kiện, kiến thức, sách (nguồn lực) → phẩm chất (nguyên tắc) → chọn và làm (hiện thực) → việc thật, kể lại cho người thân (nhân bản) |
| Bốn viên ngọc | Hiếu kỳ, Thích nghi, Bền chí, An lạc | Trường `chau_ngoc`, chỉ giáo viên thấy. Đi cùng 5 phẩm chất CT GDPT 2018 ở `pham_chat` |
| Gương Thần nhí | Tự soi: điều vui, điều khó, đã giúp được ai | Ba câu "Soi gương trước khi về" ở bước chốt (Game 2, 3) |
| Nghi thức ba nhịp | Ba nhịp thở, một câu biết ơn, một câu tự thoại | Trường `ba_nhip`, bước Lặng 30 giây |
| Thật thà, không làm hộ | Không đưa đáp án, gợi ý bằng ý nghĩa | Chìa khoá sách chỉ chỉ chỗ mở sách, không hiện đáp án cho học sinh. Học sinh tự nghĩ trước, rồi mới hỏi AI |

**Khoa học tâm lý được dùng (ghi rõ mức chắc chắn):**

- Khen nỗ lực và cách nghĩ, không khen "thông minh", "giỏi nhất" (Mueller và Dweck, 1998).
- Không phần thưởng vật chất hay báo trước, vì làm giảm hứng thú tự thân (Deci, Koestner và Ryan, 1999). Vì vậy không có điểm, quà, huy hiệu phát tay.
- Tự chủ, năng lực, gắn kết là ba nhu cầu gốc (thuyết tự quyết, Deci và Ryan). Học sinh luôn được chọn và được đổi ý.
- Gợi ý từng bậc trong vùng phát triển gần (Vygotsky). Game 2 nhắm khoảng 85% học sinh tìm được chứng cứ ở lần đầu (Wilson và cộng sự, 2019, bằng chứng từ mô hình, dùng làm điểm xuất phát).
- Trẻ nhạy với tuổi nhắm tới, chê nội dung "cho em bé" (Nielsen Norman Group). Lệch thì lệch nửa bước về phía lớn hơn.
- Niềm vui khi học đi cùng kết quả tốt hơn (Camacho-Morles và cộng sự, 2021). Đây là mối liên hệ, chưa phải quan hệ nhân quả.
- Khoảng 5 khoảnh khắc tích cực cho mỗi khoảnh khắc tiêu cực (Gottman): lời của giáo viên trong game giữ tỉ lệ này.

**Nên và không nên (vạch đỏ):**

| Nên | Không nên |
| --- | --- |
| Cả lớp cùng nghĩ, cùng nghe | Bảng xếp hạng, chia đội thắng thua, đua nhau |
| Sai thì nói "chưa đúng, mình thử lại", kèm gợi ý bằng ý nghĩa | "Sai rồi!", trừ điểm, phê bình trước lớp |
| Đồng hồ chỉ để giáo viên giữ nhịp, im lặng | Đếm ngược hù doạ, âm báo hết giờ |
| Khen "em đã nghĩ rất kỹ", "em dùng chứng cứ rõ" | "Giỏi nhất", "nhanh nhất", "thủ lĩnh" |
| Điều phổ quát: thở, biết ơn, tĩnh lặng, tử tế | Áp một niềm tin tôn giáo cụ thể |
| Nhân vật tự dựng, tên Việt thông dụng | Nhân vật có bản quyền của bên khác, tên học sinh thật |
| Học sinh tự nghĩ trước, rồi mới hỏi AI, và tự kiểm lại | Để AI làm hộ bài |
