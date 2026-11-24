/** @OnlyCurrentDoc */
/**
 * Sổ Thầy Cô — nhận phiếu đăng ký và số liệu sử dụng từ app "Trợ lý Game-học",
 * trả danh sách cho app quản lý "Quản lý Game-học" của Vietwise.
 *
 * Cách cài (một lần, bằng tài khoản Google của Vietwise):
 * 1. Tạo một Google Sheet mới, đặt tên "Sổ Thầy Cô Game-học".
 * 2. Tiện ích mở rộng > Apps Script. Xoá mã có sẵn, dán toàn bộ tệp này, bấm Lưu.
 * 3. Cài đặt dự án (bánh răng) > Thuộc tính tập lệnh > Thêm: tên MA_QUAN_LY,
 *    giá trị là một mật khẩu dài chỉ chị biết (ít nhất 12 ký tự).
 * 4. Triển khai > Tùy chọn triển khai mới > Loại: Ứng dụng web.
 *    Thực thi với tư cách: Tôi. Người có quyền truy cập: Bất kỳ ai. Bấm Triển khai, cấp quyền.
 * 5. Chép "URL ứng dụng web" (đuôi /exec) dán vào app quản lý, mục Cài đặt.
 * Dòng @OnlyCurrentDoc ở đầu tệp giới hạn quyền chỉ trong Sheet này (Google không chặn
 * như khi xin quyền mọi bảng tính). Đừng xoá dòng đó.
 * Sửa mã sau này: Triển khai > Quản lý bản triển khai > bút chì > Phiên bản mới (giữ nguyên URL).
 */

var TAB_DK = 'DangKy';
var TAB_SD = 'SuDung';
var COT_DK = ['ma_may', 'ngay_dang_ky', 'ho_ten', 'truong', 'tinh', 'mon', 'cap', 'lien_he', 'dong_y', 'cap_nhat', 'trang_thai', 'ghi_chu'];
var COT_SD = ['ma_may', 'lan_dau', 'lan_cuoi', 'so_lan_mo', 'so_ngay_dung', 'so_game_luu', 'phien_ban', 'thiet_bi', 'ngay_cuoi_dem'];

function bang_(ten, cot) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(ten);
  if (!sh) { sh = ss.insertSheet(ten); sh.appendRow(cot); sh.setFrozenRows(1); }
  return sh;
}

function cat_(v, n) { return String(v == null ? '' : v).replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, n || 120); }
// Chặn công thức bảng tính lọt vào ô (ô bắt đầu bằng = + - @)
function an_(v, n) { var s = cat_(v, n); return /^[=+\-@]/.test(s) ? "'" + s : s; }
function maMayHopLe_(m) { return /^[A-Za-z0-9_-]{8,40}$/.test(String(m || '')); }

function tim_(sh, ma) {
  var n = sh.getLastRow();
  if (n < 2) return 0;
  var ds = sh.getRange(2, 1, n - 1, 1).getValues();
  for (var i = 0; i < ds.length; i++) if (String(ds[i][0]) === ma) return i + 2;
  return 0;
}

function ra_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function dungMa_(ma) {
  var dung = PropertiesService.getScriptProperties().getProperty('MA_QUAN_LY');
  return !!dung && dung.length >= 12 && String(ma || '') === dung;
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return ra_({ ok: false, loi: 'bận' });
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var hom = Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'yyyy-MM-dd HH:mm');
    if (d.viec === 'dang_ky') {
      if (!maMayHopLe_(d.ma_may) || !cat_(d.ho_ten) || d.dong_y !== true) return ra_({ ok: false, loi: 'thiếu' });
      var sh = bang_(TAB_DK, COT_DK), r = tim_(sh, d.ma_may);
      var hang = [an_(d.ho_ten, 80), an_(d.truong, 120), an_(d.tinh, 40), an_(d.mon, 60), an_(d.cap, 30), an_(d.lien_he, 80), 'có', hom];
      if (r) sh.getRange(r, 3, 1, hang.length).setValues([hang]);
      else sh.appendRow([d.ma_may, hom].concat(hang).concat(['Mới', '']));
      return ra_({ ok: true });
    }
    if (d.viec === 'su_dung') {
      if (!maMayHopLe_(d.ma_may)) return ra_({ ok: false });
      var s2 = bang_(TAB_SD, COT_SD), r2 = tim_(s2, d.ma_may);
      var homNay = hom.slice(0, 10);
      var game = Math.max(0, Math.min(10000, parseInt(d.so_game_luu, 10) || 0));
      if (r2) {
        var v = s2.getRange(r2, 1, 1, COT_SD.length).getValues()[0];
        var ngayMoi = String(v[8]) !== homNay;
        s2.getRange(r2, 3, 1, 7).setValues([[hom, (+v[3] || 0) + 1, (+v[4] || 0) + (ngayMoi ? 1 : 0), game, an_(d.phien_ban, 12), an_(d.thiet_bi, 20), homNay]]);
      } else {
        s2.appendRow([d.ma_may, hom, hom, 1, 1, game, an_(d.phien_ban, 12), an_(d.thiet_bi, 20), homNay]);
      }
      return ra_({ ok: true });
    }
    if (d.viec === 'ghi_chu') {
      if (!dungMa_(d.ma)) return ra_({ ok: false, loi: 'sai mã quản lý' });
      var s3 = bang_(TAB_DK, COT_DK), r3 = tim_(s3, String(d.ma_may || ''));
      if (!r3) return ra_({ ok: false, loi: 'không thấy' });
      s3.getRange(r3, 11, 1, 2).setValues([[an_(d.trang_thai, 30), an_(d.ghi_chu, 500)]]);
      return ra_({ ok: true });
    }
    return ra_({ ok: false, loi: 'việc lạ' });
  } catch (err) {
    return ra_({ ok: false, loi: 'lỗi' });
  } finally { lock.releaseLock(); }
}

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.viec !== 'danh_sach') return ra_({ ok: true, ten: 'Sổ Thầy Cô Game-học' });
  if (!dungMa_(p.ma)) return ra_({ ok: false, loi: 'sai mã quản lý' });
  function doc(ten, cot) {
    var sh = bang_(ten, cot), n = sh.getLastRow();
    if (n < 2) return [];
    return sh.getRange(2, 1, n - 1, cot.length).getDisplayValues().map(function (h) {
      var o = {}; cot.forEach(function (c, i) { o[c] = h[i]; }); return o;
    });
  }
  return ra_({ ok: true, dang_ky: doc(TAB_DK, COT_DK), su_dung: doc(TAB_SD, COT_SD), luc: new Date().toISOString() });
}
