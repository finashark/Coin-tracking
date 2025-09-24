"""
Streamlit app để hiển thị dữ liệu theo dõi thị trường tiền số
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from datetime import datetime, timedelta
import time

# Import các modules từ dự án
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_collector.market_data import MarketDataCollector
from src.analyzer.trend_analyzer import TrendAnalyzer
from src.visualization.data_processor import DataVisualizer
from config import MONITORING_CONFIG

# Thiết lập trang
st.set_page_config(
    page_title="Crypto Market Monitor",
    page_icon="📊",
    layout="wide"
)

# Khởi tạo các components
data_collector = MarketDataCollector()
analyzer = TrendAnalyzer()
visualizer = DataVisualizer()

# Tiêu đề
st.title("🚀 Crypto Market Monitor")
st.markdown("---")

# Tạo columns cho layout
col1, col2 = st.columns([2, 1])

# Hàm cập nhật dữ liệu
def update_data():
    with st.spinner("Đang cập nhật dữ liệu..."):
        # Thu thập và phân tích dữ liệu
        market_data = data_collector.collect_data()
        trends = analyzer.analyze(market_data)
        
        # Chuẩn bị dữ liệu cho visualization
        market_df = visualizer.prepare_market_data(market_data)
        current_trends, history_trends = visualizer.prepare_trend_data(trends)
        
        return market_df, current_trends, history_trends

# Main dashboard
with col1:
    st.subheader("📈 Xu hướng thị trường")
    
    # Nút refresh
    if st.button("🔄 Cập nhật dữ liệu"):
        try:
            market_df, current_trends, history_trends = update_data()
            
            # Lưu vào session state
            st.session_state['market_data'] = market_df
            st.session_state['current_trends'] = current_trends
            st.session_state['history_trends'] = history_trends
            
            st.success("Đã cập nhật dữ liệu thành công!")
        except Exception as e:
            st.error(f"Lỗi khi cập nhật dữ liệu: {str(e)}")
    
    # Hiển thị xu hướng hiện tại
    if 'current_trends' in st.session_state and not st.session_state['current_trends'].empty:
        trends_df = st.session_state['current_trends']
        
        # Biểu đồ xu hướng
        chart = alt.Chart(trends_df).mark_circle().encode(
            x='price_change',
            y='volume_change',
            size='price',
            color='symbol',
            tooltip=['symbol', 'price', 'price_change', 'volume_change']
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        
        # Bảng chi tiết
        st.dataframe(
            trends_df[['symbol', 'price', 'price_change', 'volume_change', 'exchanges']],
            use_container_width=True
        )
    else:
        st.info("Nhấn nút 'Cập nhật dữ liệu' để xem xu hướng mới nhất")

# Sidebar với thống kê
with col2:
    st.subheader("📊 Thống kê")
    
    if 'market_data' in st.session_state:
        stats = visualizer.get_trend_statistics()
        
        # Hiển thị các metrics
        st.metric(
            label="Tổng số cảnh báo",
            value=stats.get('total_alerts', 0)
        )
        
        st.metric(
            label="Thay đổi giá trung bình",
            value=f"{stats.get('avg_price_change', 0):.2f}%"
        )
        
        st.metric(
            label="Thay đổi volume trung bình",
            value=f"{stats.get('avg_volume_change', 0):.2f}%"
        )
        
        # Top coins được theo dõi nhiều nhất
        st.subheader("🔥 Coins nổi bật")
        most_active_coins = stats.get('most_active_coins', {})
        if most_active_coins:
            for coin, count in most_active_coins.items():
                st.write(f"{coin}: {count} cảnh báo")
        else:
            st.info("Chưa có dữ liệu xu hướng. Hãy đợi vài lần cập nhật.")
    
    # Hiển thị cấu hình hiện tại
    st.subheader("⚙️ Cấu hình")
    st.write("Ngưỡng theo dõi:")
    st.write(f"- Thay đổi giá: {MONITORING_CONFIG['price_change_threshold']}%")
    st.write(f"- Thay đổi volume: {MONITORING_CONFIG['volume_change_threshold']}%")
    st.write(f"- Cập nhật mỗi: {MONITORING_CONFIG['update_interval']} giây")

# Auto refresh
if st.checkbox("Tự động cập nhật"):
    time_placeholder = st.empty()
    error_placeholder = st.empty()
    try:
        while True:
            try:
                market_df, current_trends, history_trends = update_data()
                st.session_state['market_data'] = market_df
                st.session_state['current_trends'] = current_trends
                st.session_state['history_trends'] = history_trends
                
                time_placeholder.text(f"Lần cập nhật cuối: {datetime.now().strftime('%H:%M:%S')}")
                error_placeholder.empty()  # Xóa thông báo lỗi nếu có
            except Exception as e:
                error_placeholder.error(f"Lỗi khi cập nhật: {str(e)}")
            
            time.sleep(MONITORING_CONFIG['update_interval'])
    except Exception as e:
        st.error(f"Lỗi hệ thống: {str(e)}")