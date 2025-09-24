"""
Module xử lý và chuẩn bị dữ liệu cho việc hiển thị
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class DataVisualizer:
    def __init__(self):
        self.latest_data = None
        self.trend_history = []
        self.max_history_size = 100  # Số lượng xu hướng tối đa để lưu trữ
        
    def prepare_market_data(self, market_data: Dict) -> pd.DataFrame:
        """Chuyển đổi dữ liệu thị trường thành DataFrame"""
        data = []
        for symbol, info in market_data.items():
            data.append({
                'symbol': symbol,
                'price': info['avg_price'],
                'volume': info['total_volume'],
                'exchanges': ', '.join(info['exchanges'])
            })
        
        df = pd.DataFrame(data)
        df['symbol'] = df['symbol'].apply(lambda x: x.replace('/USDT', ''))
        self.latest_data = df
        return df
    
    def prepare_trend_data(self, trends: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Chuẩn bị dữ liệu xu hướng cho việc hiển thị"""
        # Thêm xu hướng mới vào lịch sử
        for trend in trends:
            trend['timestamp'] = pd.Timestamp.now()
            self.trend_history.append(trend)
        
        # Giới hạn kích thước lịch sử
        self.trend_history = self.trend_history[-self.max_history_size:]
        
        # Tạo DataFrame cho xu hướng hiện tại
        current_trends = pd.DataFrame(trends)
        if not current_trends.empty:
            current_trends['symbol'] = current_trends['symbol'].apply(lambda x: x.replace('/USDT', ''))
        
        # Tạo DataFrame cho lịch sử xu hướng
        history_df = pd.DataFrame(self.trend_history)
        if not history_df.empty:
            history_df['symbol'] = history_df['symbol'].apply(lambda x: x.replace('/USDT', ''))
        
        return current_trends, history_df
    
    def get_top_movers(self, n: int = 10) -> pd.DataFrame:
        """Lấy top n coin có biến động lớn nhất"""
        if self.latest_data is None or self.latest_data.empty:
            return pd.DataFrame()
            
        return self.latest_data.nlargest(n, 'volume')
    
    def get_trend_statistics(self) -> Dict:
        """Tính toán thống kê từ dữ liệu xu hướng"""
        if not self.trend_history:
            return {
                'total_alerts': 0,
                'avg_price_change': 0,
                'avg_volume_change': 0,
                'most_active_coins': []
            }
        
        history_df = pd.DataFrame(self.trend_history)
        
        stats = {
            'total_alerts': len(history_df),
            'avg_price_change': history_df['price_change'].mean(),
            'avg_volume_change': history_df['volume_change'].mean(),
            'most_active_coins': history_df['symbol'].value_counts().head(5).to_dict()
        }
        
        return stats