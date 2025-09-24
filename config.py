"""
Cấu hình chung cho ứng dụng
"""

# Danh sách sàn giao dịch cần theo dõi
EXCHANGES = [
    'binance',
    'kucoin',
    'gate'
]

# Cấu hình theo dõi
MONITORING_CONFIG = {
    # Tần suất cập nhật dữ liệu (giây)
    'update_interval': 300,  # 5 phút
    
    # Ngưỡng phát hiện xu hướng
    'price_change_threshold': 1.0,  # 1% thay đổi giá
    'volume_change_threshold': 10.0,  # 10% thay đổi volume
    
    # Số lượng coin top để theo dõi
    'top_coins_limit': 100,
    
    # Thời gian để tính xu hướng (giờ)
    'trend_timeframe': 24
}

# Cấu hình thông báo
NOTIFICATION_CONFIG = {
    'telegram_enabled': True,
    'notification_cooldown': 3600,  # 1 giờ giữa các thông báo cho cùng một coin
    'min_notifications_interval': 300  # Thời gian tối thiểu giữa các thông báo (giây)

}
