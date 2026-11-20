# 🏸 SmashPay — Chia Tiền Cầu Lông (Botkeep Ready)

Ứng dụng web chia tiền sau buổi đánh cầu lông (Python FastAPI + SQLite), tối ưu gọn nhẹ để chạy trên **1 server slot miễn phí** của [Botkeep](https://botkeep.cloud/).

## Tính năng chính

- **Danh sách thành viên cố định:** Lưu sẵn tên và thông tin ngân hàng (mã ngân hàng NAPAS, số tài khoản, tên chủ tài khoản) để tự động sinh mã VietQR.
- **Chia đều có loại trừ (Tiền sân, Tiền cầu):** Mặc định chọn toàn bộ người tham gia buổi đánh, cho phép bỏ tích nhanh người về sớm hoặc không tham gia.
- **Phí gửi xe 5.000đ linh hoạt 2 chế độ:**
  1. *1 người trả hộ riêng:* Tự nhân `5.000đ × số người có gửi xe` cho người trả hộ.
  2. *Gộp chung vào hóa đơn sân:* Tự tách `5.000đ × số người có gửi xe` ra khỏi hóa đơn sân trước khi chia đều tiền sân, không bị tính trùng.
- **Bánh & Cà phê theo nhiều dòng món:** Mặc định nhập theo **Đơn giá / người** (ví dụ: 2 người ăn bánh 50k → mỗi người 50k, người ứng trả tự cộng 100k), kèm nút gạt sang **Chia đều tổng** cho các đĩa/hộp ăn chung.
- **Cân đối công nợ tối ưu & tick Đã chuyển khoản:** Tự tính số dư ròng từng người, gom thành ít lượt chuyển khoản nhất, lưu trạng thái đã trả vào SQLite (`data/badminton.db`).
- **VietQR SVG tự động & Copy tin nhắn Zalo:** Dùng [VietQR Quick Link](https://www.vietqr.io/qr-dong) định dạng `.svg` điền sẵn số tiền và nội dung chuyển khoản; sao chép nhanh tin nhắn tổng kết gửi nhóm Zalo/Messenger.

## Cách chạy trên máy cá nhân

```bash
pip install -r requirements.txt
python main.py
```

Sau đó mở trình duyệt tại `http://localhost:8000`.

## Cách triển khai lên Botkeep

1. Đăng nhập bảng điều khiển [Botkeep](https://botkeep.cloud/), tạo mới 1 ứng dụng **Python** (hoặc chọn mẫu **FastAPI**).
2. Tải trực tiếp file `.zip` dự án lên (hoặc đẩy mã nguồn lên GitHub rồi kết nối qua tab GitHub theo [Botkeep Docs](https://botkeep.cloud/docs)).
3. Thiết lập lệnh khởi chạy (**Startup Command**):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
   *(Hoặc dùng `python main.py` — file `main.py` đã tự đọc biến môi trường `PORT`.)*
4. Khởi động server. Cơ sở dữ liệu SQLite sẽ tự động được tạo và lưu bền vững tại `data/badminton.db` trong dung lượng ổ cứng của server.
5. **Sao lưu dữ liệu:** Nên tải bản sao lưu định kỳ file `data/badminton.db` hoặc dùng tính năng Backup trong bảng điều khiển Botkeep.
