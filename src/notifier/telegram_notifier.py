"""
Module gửi thông báo qua Telegram
"""
import os
import time
from typing import List, Dict
from telegram.ext import Updater
from config import NOTIFICATION_CONFIG

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.last_notifications = {}
        
        if not self.bot_token or not self.chat_id:
            raise ValueError("Telegram bot token and chat ID are required")
        
        self.updater = Updater(self.bot_token, use_context=True)
    
    def send_alerts(self, trends: List[Dict]):
        """Gửi cảnh báo về các xu hướng đáng chú ý"""
        current_time = time.time()
        
        for trend in trends:
            symbol = trend['symbol']
            
            # Kiểm tra thời gian chờ giữa các thông báo
            if symbol in self.last_notifications:
                time_since_last = current_time - self.last_notifications[symbol]
                if time_since_last < NOTIFICATION_CONFIG['notification_cooldown']:
                    continue
            
            # Tạo thông báo
            message = self._format_alert_message(trend)
            
            try:
                # Gửi thông báo
                self.updater.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
                
                # Cập nhật thời gian thông báo
                self.last_notifications[symbol] = current_time
                
                # Đợi giữa các thông báo
                time.sleep(NOTIFICATION_CONFIG['min_notifications_interval'])
                
            except Exception as e:
                print(f"Error sending notification for {symbol}: {str(e)}")
    
    def _format_alert_message(self, trend: Dict) -> str:
        """Format thông báo cảnh báo"""
        return f"""🚨 *Altcoin Alert* 🚨

*{trend['symbol']}* đang có động thái đáng chú ý!

💰 Giá: ${trend['price']:.4f}
📈 Thay đổi giá: {trend['price_change']:.2f}%
📊 Thay đổi volume: {trend['volume_change']:.2f}%
🏦 Các sàn: {', '.join(trend['exchanges'])}

#crypto #alert #{trend['symbol'].split('/')[0]}"""