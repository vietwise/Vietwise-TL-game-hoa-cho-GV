# Nhóm lớp: game đổi theo độ tuổi (lấy từ "Tâm Lý Học Theo Độ Tuổi" của Vườn Game-học Vietwise)

Hai núm riêng, không lẫn:
- **Nội dung** theo lớp và bài Thầy Cô gửi (ảnh sách).
- **Phong cách** (giọng, lượng chữ, nhân vật, cách thưởng) theo nhóm tuổi dưới đây. Học sinh lớn hơn hoặc nhỏ hơn tuổi của lớp thì Thầy Cô nói trong ghi chú, ưu tiên điều Thầy Cô nói.

Phạm vi gốc của Vườn Game-học là 3 đến 12 tuổi. Nhóm D và E (lớp 8 đến 12) là phần Skill mở rộng cho Thầy Cô; ghi rõ trong `gv_ghi_chu` là "phong cách tham khảo".

Điền `nhom_lop` trong JSON: `A`, `B`, `C`, `D` hoặc `E`.

| Nhóm | Lớp | Thời lượng gợi ý | Lời kể (`loi_ke`) | Số lựa chọn | Giọng |
|---|---|---|---|---|---|
| A | 1 đến 3 | mở tiết 10, ôn bài 15 | 2 đến 3 câu ngắn, mỗi câu một ý, có hình minh họa lớn | 2 (tối đa 3) | Ấm, gọi bằng tên, câu ngắn. Nhân vật dễ thương |
| B | 4 đến 5 | 10 / 15 / 20 | Đoạn 2 đến 3 câu đọc thầm được; chuyện phiêu lưu hoặc khoa học | 3 | Thân thiện, không nựng, không gọi "bé ơi"; hài hước nhẹ; giải thích "vì sao" |
| C | 6 đến 7 | 10 / 15 / 20 | Ngắn, ngang hàng, có tình huống hơi mơ hồ để tranh luận | 3 đến 4 | Ngang hàng, không giảng đạo, cho quyền chọn |
| D | 8 đến 10 | 10 / 15 / 20 | Việc thật, có số liệu; ít cute | 3 đến 4 | Tôn trọng, thẳng, không khen kiểu "ngoan" |
| E | 11 đến 12 | 10 / 15 / 20 | Gắn học tập, nghề, quyết định thật; có thể mơ hồ có chủ ý | 3 đến 4 | Như đồng nghiệp, ít lời |

## Chi tiết theo nhóm

**A (lớp 1 đến 3).** Nghĩ trên vật cụ thể, chưa quen ký hiệu. Dùng đồ vật quen (tiền lẻ, quả, đồ chơi). Chữ ít, trên màn hình chiếu nên Thầy Cô đọc to. Không báo lỗi gắt; gợi ý từng bước. Mục tiêu khoảng 85% học sinh làm được. Thưởng thấy được (ngọc, ngôi sao) gắn với nỗ lực, không với đúng sai. Phản biện: hỏi "em thấy gì?" thay vì "chứng cứ nào?".

**B (lớp 4 đến 5).** Muốn "làm chuyên gia", bắt đầu chê nội dung trẻ con. Giảm cute, nhân vật là đồng đội. Cho xin gợi ý thay vì hiện sẵn. Có thể thêm câu thử thách khó hơn. Tránh câu đố mẹo quá dễ.

**C (lớp 6 đến 7).** Bắt đầu nghĩ theo giả thuyết ("nếu... thì..."), nhưng còn ngại bị so sánh với bạn. Cho nhiều đường giải; lựa chọn D (sáng tạo) khuyến khích. Không so sánh học sinh với nhau; tôn trọng riêng tư khi chia sẻ ý kiến.

**D (lớp 8 đến 10).** Cần việc thật, mục đích rõ, không gian thử vai. Tình huống dùng số liệu thật. Phản hồi thẳng. Không dùng giọng nựng hay khen kiểu "ngoan".

**E (lớp 11 đến 12).** Tình huống nối với học tập và nghề nghiệp. Dự án thật gắn với đời sống. Thầy Cô đóng vai người hướng dẫn.

## Ba mức (Khởi động, Vững vàng, Thử thách)
Một game, cùng nội dung; Thầy Cô chọn mức bằng ghi chú. Chỉ đổi số lựa chọn, gợi ý và số câu hỏi gợi mở. Trong `gv_ghi_chu` ghi sẵn cách nâng hoặc hạ mức:
- Khởi động: ít lựa chọn nhất của nhóm, gợi ý hiện luôn, câu mở ngắn.
- Vững vàng: số lựa chọn chuẩn của nhóm, gợi ý khi học sinh hỏi.
- Thử thách: thêm một lựa chọn gây tranh luận, không gợi ý, thêm câu "nếu đổi điều kiện thì...".

## Tự kiểm sau khi viết (chẩn đoán)
- Quá trẻ con: học sinh lướt qua nhân vật, ngại chơi trước bạn → giảm cute, đổi xưng hô.
- Quá nghiêm túc: ngáp, đoạn chữ dài, ít tương tác → chia nhỏ, thêm lựa chọn, thêm dự án thật.
- Quá dễ: gần như cả lớp chọn giống nhau ngay → thêm tình huống mới, thêm lựa chọn thật sự khó.
- Quá khó: học sinh im lặng, xin gợi ý dồn dập → thêm ví dụ cụ thể, giảm chữ, hạ mức rồi nâng dần.
Ghi một dòng gợi ý chẩn đoán này vào `gv_ghi_chu` để Thầy Cô điều chỉnh trên lớp.
