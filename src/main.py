"""
Entry point của ứng dụng
"""
import os
import time
import schedule
from dotenv import load_dotenv

# Load các biến môi trường
load_dotenv()

# Import các modules
from data_collector.market_data import MarketDataCollector
from analyzer.trend_analyzer import TrendAnalyzer
from notifier.telegram_notifier import TelegramNotifier
from config import MONITORING_CONFIG

def main():
    # Khởi tạo các components
    data_collector = MarketDataCollector()
    analyzer = TrendAnalyzer()
    notifier = TelegramNotifier()
    
    def update_and_analyze():
        try:
            # Thu thập dữ liệu
            market_data = data_collector.collect_data()
            
            # Phân tích xu hướng
            trends = analyzer.analyze(market_data)
            
            # Gửi thông báo nếu phát hiện xu hướng đáng chú ý
            if trends:
                notifier.send_alerts(trends)
                
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
    
    # Lên lịch chạy định kỳ
    schedule.every(MONITORING_CONFIG['update_interval']).seconds.do(update_and_analyze)
    
    # Chạy lần đầu
    update_and_analyze()
    
    # Loop chính
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()