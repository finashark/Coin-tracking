# Cryptocurrency Market Tracker

Ứng dụng theo dõi và phân tích thị trường tiền số, tự động phát hiện và thông báo về các Altcoin tiềm năng.

## Tính năng

- Thu thập dữ liệu thời gian thực từ nhiều sàn giao dịch
- Phân tích xu hướng giá và độ quan tâm của thị trường
- Tự động phát hiện các Altcoin có tiềm năng
- Gửi thông báo qua Telegram

## Cài đặt

1. Clone repository này
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
3. Tạo file `.env` với các thông tin cấu hình:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

## Cấu hình

- Chỉnh sửa `config.py` để cấu hình:
  - Danh sách sàn giao dịch cần theo dõi
  - Ngưỡng cảnh báo
  - Tần suất cập nhật

## Sử dụng

Chạy ứng dụng:
```bash
python src/main.py
```

## Cấu trúc dự án

```
.
├── src/
│   ├── data_collector/    # Thu thập dữ liệu từ các sàn
│   ├── analyzer/          # Phân tích xu hướng
│   ├── notifier/          # Gửi thông báo
│   └── main.py           # Entry point
├── config.py             # Cấu hình
├── requirements.txt      # Thư viện cần thiết
└── README.md
```