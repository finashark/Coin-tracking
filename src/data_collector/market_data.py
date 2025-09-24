"""
Module thu thập dữ liệu thị trường từ các sàn giao dịch
"""
import ccxt
import pandas as pd
from typing import Dict, List
from config import EXCHANGES, MONITORING_CONFIG

class MarketDataCollector:
    def __init__(self):
        self.exchanges = {}
        self._initialize_exchanges()
        
    def _initialize_exchanges(self):
        """Khởi tạo kết nối với các sàn giao dịch"""
        for exchange_id in EXCHANGES:
            try:
                exchange_class = getattr(ccxt, exchange_id)
                self.exchanges[exchange_id] = exchange_class({
                    'enableRateLimit': True
                })
            except Exception as e:
                print(f"Error initializing exchange {exchange_id}: {str(e)}")
    
    def collect_data(self) -> Dict:
        """Thu thập dữ liệu từ tất cả các sàn"""
        all_data = {}
        
        for exchange_id, exchange in self.exchanges.items():
            try:
                # Lấy thông tin thị trường
                markets = exchange.load_markets()
                tickers = exchange.fetch_tickers()
                
                # Lọc và xử lý dữ liệu
                for symbol, ticker in tickers.items():
                    if self._is_valid_market(symbol, markets):
                        if symbol not in all_data:
                            all_data[symbol] = {
                                'price': [],
                                'volume': [],
                                'exchanges': []
                            }
                        
                        all_data[symbol]['price'].append(ticker['last'])
                        all_data[symbol]['volume'].append(ticker['quoteVolume'])
                        all_data[symbol]['exchanges'].append(exchange_id)
                        
            except Exception as e:
                print(f"Error collecting data from {exchange_id}: {str(e)}")
        
        # Tính trung bình giá và volume cho mỗi coin
        for symbol in all_data:
            all_data[symbol]['avg_price'] = sum(all_data[symbol]['price']) / len(all_data[symbol]['price'])
            all_data[symbol]['total_volume'] = sum(all_data[symbol]['volume'])
        
        return all_data
    
    def _is_valid_market(self, symbol: str, markets: Dict) -> bool:
        """Kiểm tra xem một cặp giao dịch có hợp lệ không"""
        try:
            # Chỉ lấy các cặp với USDT
            return symbol.endswith('/USDT') and markets[symbol]['active']
        except:
            return False