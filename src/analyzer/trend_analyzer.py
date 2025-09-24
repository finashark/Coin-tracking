"""
Module phân tích xu hướng thị trường
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from config import MONITORING_CONFIG

class TrendAnalyzer:
    def __init__(self):
        self.price_history = {}
        self.volume_history = {}
        
    def analyze(self, market_data: Dict) -> List[Dict]:
        """Phân tích xu hướng từ dữ liệu thị trường"""
        trends = []
        
        for symbol, data in market_data.items():
            # Cập nhật lịch sử
            if symbol not in self.price_history:
                self.price_history[symbol] = []
                self.volume_history[symbol] = []
            
            self.price_history[symbol].append(data['avg_price'])
            self.volume_history[symbol].append(data['total_volume'])
            
            # Giữ lịch sử trong khoảng thời gian cấu hình
            max_history = int(MONITORING_CONFIG['trend_timeframe'] * 3600 / MONITORING_CONFIG['update_interval'])
            self.price_history[symbol] = self.price_history[symbol][-max_history:]
            self.volume_history[symbol] = self.volume_history[symbol][-max_history:]
            
            # Phân tích xu hướng nếu có đủ dữ liệu
            if len(self.price_history[symbol]) >= 2:
                trend = self._analyze_single_coin(symbol, data)
                if trend:
                    trends.append(trend)
        
        return self._filter_top_trends(trends)
    
    def _analyze_single_coin(self, symbol: str, current_data: Dict) -> Dict:
        """Phân tích xu hướng cho một coin"""
        try:
            price_change = self._calculate_change(self.price_history[symbol])
            volume_change = self._calculate_change(self.volume_history[symbol])
            
            # Kiểm tra ngưỡng đáng chú ý
            if (abs(price_change) >= MONITORING_CONFIG['price_change_threshold'] and
                volume_change >= MONITORING_CONFIG['volume_change_threshold']):
                
                return {
                    'symbol': symbol,
                    'price': current_data['avg_price'],
                    'price_change': price_change,
                    'volume_change': volume_change,
                    'exchanges': current_data['exchanges']
                }
                
        except Exception as e:
            print(f"Error analyzing {symbol}: {str(e)}")
            
        return None
    
    def _calculate_change(self, values: List[float]) -> float:
        """Tính phần trăm thay đổi"""
        if len(values) < 2:
            return 0
        return ((values[-1] - values[0]) / values[0]) * 100
    
    def _filter_top_trends(self, trends: List[Dict]) -> List[Dict]:
        """Lọc ra những xu hướng đáng chú ý nhất"""
        if not trends:
            return []
            
        # Sắp xếp theo mức độ thay đổi volume và giá
        sorted_trends = sorted(trends, 
                             key=lambda x: (abs(x['volume_change']) * abs(x['price_change'])),
                             reverse=True)
        
        return sorted_trends[:10]  # Trả về 10 xu hướng top