# Quản lý Game-học: Sổ Thầy Cô

App riêng của Vietwise để xem Thầy Cô nào đăng ký và dùng app **Trợ lý Game-học** đến đâu. Miễn phí, không có phần thu phí.

- App quản lý: https://vietwise.github.io/Vietwise-TL-game-hoa-cho-GV/quan-ly/ (mở bằng Chrome hoặc Edge, cài thành app trên máy tính).
- Dữ liệu nằm trong một Google Sheet của tài khoản Vietwise, nhận phiếu qua `apps-script.gs`. Trang app quản lý công khai nhưng không có dữ liệu: muốn xem danh sách phải có mã quản lý.

## Luồng dữ liệu
1. Thầy Cô mở Trợ lý Game-học. Thẻ **Hướng dẫn** có phiếu **Thầy Cô đăng ký** (họ tên, trường, tỉnh, cấp, môn, Zalo hoặc email, ô đồng ý). Thẻ **Giao việc** có dải nhắc đăng ký, Thầy Cô ẩn được.
2. Mỗi lần mở app (tối đa 30 phút một lần) app gửi số liệu ẩn danh: mã máy ngẫu nhiên, số game đã lưu, phiên bản Skill đã tải, loại máy. Thầy Cô tắt được bằng ô "Cho phép gửi các con số này".
3. App quản lý đọc hai trang `DangKy` và `SuDung`, ghép theo mã máy. Trạng thái và ghi chú chị sửa trong app được ghi lại vào Sheet.

## Cài một lần
1. Làm theo phần chú thích đầu tệp `apps-script.gs` (tạo Sheet, dán mã, đặt `MA_QUAN_LY`, triển khai ứng dụng web).
2. Thêm vào `phien-ban.json` ở gốc repo: `"so_thay_co": "<URL ứng dụng web, đuôi /exec>"`. Chưa có dòng này thì app Thầy Cô không hiện phiếu và không gửi gì.
3. Mở app quản lý, thẻ **Cài đặt**, dán URL và mã quản lý.

## Kiểm thử đã chạy
Playwright, khổ 390 px và 1280 px, Apps Script chạy giả lập trong node: đăng ký, báo sử dụng, chặn công thức bảng tính, sai mã quản lý bị từ chối, sửa trạng thái và ghi chú, xuất CSV, khi chưa có URL thì không hiện gì.
