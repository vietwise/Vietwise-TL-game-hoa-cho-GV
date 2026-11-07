# Nhóm môn: cùng khung, đổi "chứng cứ" và "thử thách đời thật"

Mọi nhóm môn dùng cùng ba loại game và cùng khung. Khác nhau ở: thử thách đời thật mở đầu lấy từ đâu, "chứng cứ" là gì, hiểu lầm hay gặp là gì, và phản biện/sáng tạo đòi hỏi gì. Điền `nhom_mon` trong JSON.

| `nhom_mon` | Môn | Thử thách đời thật hay dùng | "Chứng cứ" của học sinh | Hiểu lầm hay gặp (đưa vào `gv_hieu_lam`) |
|---|---|---|---|---|
| `toan` | Toán, Tin học (phần tính toán) | Mua sắm, pha trộn, đo đạc, chia tiền, lịch trình | Phép tính và cách tính, đơn vị | Quên đổi đơn vị, nhầm tỉ lệ và hiệu, tin số "tròn" |
| `khoa-hoc` | Khoa học tự nhiên, Vật lý, Hóa, Sinh, Khoa học 4 đến 5, Công nghệ | Nấu ăn, y tế gia đình, đồ điện, môi trường, an toàn | Số liệu, thí nghiệm, nguyên lý đã học | Nhầm khái niệm gần nhau, đơn vị, "tự nhiên thì an toàn" |
| `ngu-van` | Tiếng Việt, Ngữ văn, Sách là Thầy | Một lời nhắn, một quyết định của nhân vật, một cuộc tranh luận trong gia đình | Câu chữ trong văn bản hoặc sách (trích đúng, đúng chỗ) | Kể lại chung chung, bình luận không có chữ nào trong văn bản làm gốc |
| `xa-hoi` | Lịch sử, Địa lí, Đạo đức, Giáo dục công dân, Kinh tế pháp luật, Hoạt động trải nghiệm | Chuyến đi, di tích quê em, một quy định nơi ở, một việc thiện | Tư liệu, bản đồ, số liệu, quy định trong bài | Áp suy nghĩ hôm nay vào thời xưa, khái quát từ một ví dụ |
| `ngoai-ngu` | Tiếng Anh, Hàn, Nhật, Trung, Pháp, Đức, Nga... | Đọc một biển báo, nhãn sản phẩm, tin nhắn, thực đơn, thông báo thật | Câu hoặc từ ngoại ngữ trong văn bản đọc (xem `doc-ngoai-ngu.md`) | Dịch từng từ, đoán nghĩa theo tiếng Việt, bỏ qua ngữ cảnh |
| `nghe-thuat-the-chat` | Âm nhạc, Mĩ thuật, Thể dục | Một buổi biểu diễn, một cuộc thi trường, chuẩn bị chạy bền, thiết kế áp phích | Điều học sinh nghe, thấy, thử được ngay trong lớp | Cho rằng chỉ có một cách "đúng" để sáng tạo |
| `tin-hoc` | Tin học, Công nghệ số | Tin nhắn lạ, mật khẩu, chia sẻ ảnh, dùng AI | Việc học sinh làm được và cách kiểm tra | Tin ngay thông báo trúng thưởng, dùng một mật khẩu cho mọi nơi |

Môn khác thì chọn nhóm gần nhất và nói trong `gv_ghi_chu`.

## Cách dùng theo loại game
- **Mở tiết:** thử thách đời thật + một quyết định + "bước ngoặt" làm lộ khoảng trống kiến thức, kết bằng câu hỏi treo mà bài hôm nay sẽ trả lời. Không hiện đáp án.
- **Ôn bài:** mỗi lựa chọn ứng với một cách hiểu; ít nhất một lựa chọn dựa trên hiểu lầm phổ biến của nhóm môn (cột cuối). Chứng cứ theo cột "Chứng cứ". Lựa chọn D (sáng tạo) của môn nào thì sáng tạo kiểu môn đó: ví dụ Toán đổi điều kiện bài toán, Văn viết tiếp, Xã hội đề xuất quy định, Ngoại ngữ viết lại thông báo.
- **Sách là Thầy:** mạnh nhất với `ngu-van` và `xa-hoi`, dùng được cho mọi môn có sách đọc thêm (khoa học thường thức, sách ngoại ngữ đọc hiểu). Chìa khóa sách phải là câu chỉ người đã đọc mới trả lời được.

## Quy tắc riêng từng nhóm
- **Toán, khoa học:** số liệu đã tính sẵn để trong `gv_`. Đơn vị đi kèm mọi con số. Chỉ dùng thông tin đời thật chắc chắn đúng, đúng trình độ lớp; không chắc thì bỏ và ghi cho Thầy Cô. Mô phỏng hoặc hình minh họa phải nói rõ đó là hình minh họa. Nội dung y tế, hóa chất, điện: tình huống không được khuyến khích hành động nguy hiểm; có dòng an toàn trong `gv_ghi_chu`.
- **Ngữ văn:** trích văn bản chỉ trong phạm vi ảnh trang Thầy Cô gửi. Không bịa trích dẫn, số trang. Không chấm cảm thụ đúng sai.
- **Xã hội:** sự kiện lịch sử, số liệu địa lí chỉ lấy từ trang sách hoặc điều rất chắc chắn. Chủ đề nhạy cảm (tôn giáo, chính trị, dân tộc): chỉ dùng điều phổ quát và tôn trọng; không áp niềm tin tôn giáo nào.
- **Nghệ thuật, thể chất:** không chê kỹ năng; không chọn lựa chọn đòi hỏi thể lực cụ thể mà học sinh có thể không làm được. Nhân vật, tác phẩm của người khác: không sao chép; dựng nhân vật mới.
- **Tin học:** không chứa liên kết hoặc ứng dụng thật gây hại; tình huống lừa đảo mô tả chung, không dùng tên thương hiệu thật.
