# Đóng gói Trợ lý Game-hóa cho Thầy Cô

Dựng lại toàn bộ gói giao cho Thầy Cô chỉ bằng một lệnh, từ đúng nội dung trong repo này.

```
python3 tools/dong-goi/dong_goi.py            # ra dist/Tro-ly-Game-hoa-Vietwise.zip
python3 tools/dong-goi/dong_goi.py /đường/dẫn/ra.zip
python3 tools/dong-goi/dung_giao_viec.py      # chỉ dựng web/giao-viec.html
```

Gói bung ra theo thứ tự: 1 Đọc trước và phiếu giao việc (`mau/doc-truoc.html`), 2 giao việc mở trong Claude (dựng từ `mau/giao-viec.tpl.html`, `sprite/`, trình chơi và ví dụ của Skill), 3 ba game mẫu (dựng bằng `skill/game-hoc-vietwise/scripts/dung_trang.py`), 4 `game-hoc-vietwise.zip` để tải lên Claude.

## Thu sẵn giọng đọc cho 3 game mẫu
Chỉ game mẫu mới thu sẵn được (game Thầy Cô tạo mới có chữ mới). Cần mạng tới `speech.platform.bing.com`, `pip install edge-tts` và ffmpeg:

```
python3 tools/dong-goi/thu_giong.py          # thu HoaiMy (Việt) và giọng từng thứ tiếng, ra tools/dong-goi/giong/*.json
python3 tools/dong-goi/dong_goi.py           # tự dùng bản có giọng nếu có thư mục giong/
```
`--gia` tạo âm thử bằng ffmpeg để kiểm tra đường ống; KHÔNG commit kết quả của `--gia`. Cách chia đoạn và khóa băm trong script phải khớp hàm `rng/chia/tach/hk` của `trinh-choi.html` (đã kiểm: 8/8 đoạn khớp). Trình chơi dùng âm thu sẵn nếu có, đoạn nào thiếu thì dùng giọng trên máy, thiếu cả hai thì báo.

## Khi sửa Skill, làm theo thứ tự
1. Sửa trong `skill/game-hoc-vietwise/` (SKILL.md, references, assets/trinh-choi.html, ví dụ trong references/vi-du).
2. Chạy `dung_trang.py` cho mọi ví dụ trong `references/vi-du/`; tất cả phải dựng được.
3. Nếu đổi 3 game mẫu, sửa danh sách `games` trong `dong_goi.py` và các thẻ "Chơi thử" trong `mau/doc-truoc.html`.
4. Chạy `dong_goi.py`, giải nén ra thư mục sạch, mở từng tệp ở khổ 390 px: không cuộn ngang, không lỗi, khối logo không bị khóa.
5. Cập nhật `dist/` và commit.

## Điều không được đổi
- Khối ghi nguồn Vietwise (BRAND, FOOT) trong `trinh-choi.html`: đổi chữ là hỏng mã băm và trình chơi tự khóa; script dựng từ chối chạy. CSS ngoài khối khóa được sửa tự do (đã làm cho điện thoại).
- Logo chỉ ở đầu trang, dòng tri ân chỉ ở cuối trang.
- Không có bước đăng lên Vietwise.edu.vn; dùng từ "giao việc" và "trả kết quả".

## Chưa kiểm chứng
Tài khoản Claude miễn phí có tải Skill lên được không; giọng đọc thật trên thiết bị thật; nút "Giao việc cho Trợ lý" khi chạy trong Claude thật.
