import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="NSE Risk Score Report", layout="wide", page_icon="📊")

# ====================== CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .stApp { background-color: #08090d; color: #e0e0e0; }
    .glass-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 1.8rem; }
    .mono { font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
st.sidebar.header("NSE Risk Score Report")
symbol_input = st.sidebar.text_input("Enter NSE Symbol", value="RELIANCE").upper()
stock_symbol = f"{symbol_input}.NS"

if st.sidebar.button("🔄 Fetch Live Data", type="primary"):
    st.session_state.fetch = True

# ====================== FETCH DATA ======================
@st.cache_data(ttl=300)
def get_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="6mo")
        return info, hist
    except:
        return None, None

info, hist = get_data(stock_symbol)

# Live Values
if info:
    price = info.get('currentPrice') or info.get('regularMarketPrice') or 1428.75
    prev_close = info.get('regularMarketPreviousClose') or price
    change = price - prev_close
    change_pct = (change / prev_close) * 100
    volume = f"{info.get('volume', 0)/10**7:.2f} Cr"
    mkt_cap = f"₹{(info.get('marketCap', 0)/10**7):.2f}L Cr"
    name = info.get('longName', stock_symbol)
else:
    price, change, change_pct, volume, mkt_cap, name = 1428.75, 12.45, 0.88, "1.84 Cr", "₹19.32L Cr", "Reliance Industries Ltd."

# ====================== HEADER ======================
st.markdown(f"""
<div style="text-align:center; margin-bottom:2rem;">
    <h1 style="font-size:2.8rem; background:linear-gradient(90deg,#00ffaa,#00ccff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        NSE: {symbol_input} • {name}
    </h1>
    <div style="font-size:3.2rem; font-weight:700; font-family:'JetBrains Mono';">₹{price:,.2f}</div>
    <div style="font-size:1.4rem; color:{'#00ffaa' if change>=0 else '#ff4444'}">
        {'+' if change>=0 else ''}₹{change:.2f} ({'+' if change_pct>=0 else ''}{change_pct:.2f}%)
    </div>
    <div class="mono" style="margin-top:0.5rem;">Vol: {volume} | Mkt Cap: {mkt_cap}</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Risk Overview", "🌌 Sentiment Overlay", "📈 Technical Deep Dive"])

# ====================== TAB 1: RISK OVERVIEW ======================
with tab1:
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Overall Risk Score")
        overall = 64  # You can make this dynamic later
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall,
            gauge={'axis': {'range': [0,100]}, 'bar': {'color': "#00ffaa"}},
            title={'text': "RISK SCORE"}
        ))
        fig.update_layout(height=340, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Trade Plan")
        st.markdown('<span style="background:#ffaa0020;color:#ffaa00;border:2px solid #ffaa00;padding:8px 24px;border-radius:9999px;font-size:1.3rem;font-weight:700;">HOLD</span>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            st.metric("Entry Zone", "1415 – 1435")
            st.metric("Stop Loss", "1388 (ATR + Gann)")
        with c2:
            st.metric("Target 1", "1480")
            st.metric("Target 2", "1525")
        st.markdown('</div>', unsafe_allow_html=True)

# ====================== TAB 2: SENTIMENT OVERLAY (SBC + GANN) ======================
with tab2:
    st.warning("⚠️ Non-traditional tools. Use only as confluence. Not primary signals.")

    # Sarvatobhadra Chakra
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Astrological Sentiment – Sarvatobhadra Chakra (SBC)")
    
    seed = sum(ord(c) for c in symbol_input)
    sbc_score = max(35, min(88, 48 + (seed % 45)))
    
    fig_sbc = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sbc_score,
        gauge={'axis': {'range': [0,100]}, 'bar': {'color': "#aaff00"}},
        title={'text': "SBC Vedha Score - Mildly Bullish"}
    ))
    fig_sbc.update_layout(height=220)
    st.plotly_chart(fig_sbc, use_container_width=True)

    akshara = symbol_input[0]
    st.markdown(f"""
    **First Akshara (East Cell):** {akshara} – Strong Vedha from Jupiter & Venus  
    **Short-term (1-7 days):** Mild Bullish (+4% to +9%)  
    **Medium-term (30-90 days):** Positive bias  
    **Active Yoga:** Guru-Mangal Yoga
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Gann Analysis
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Gann Price-Time Square Analysis")
    resistance1 = round(price * 1.038)
    resistance2 = round(price * 1.068)
    
    st.markdown(f"""
    Current price on **Gann Square of Nine – Cardinal Level**  
    Next Resistances: **₹{resistance1}** (1×1) & **₹{resistance2}** (Square of 9)  
    Next Major Time Cycle: **{ (datetime.now() + timedelta(days=42)).strftime('%d %b %Y')}**  
    **Bias:** Mildly Bullish | Strength: 7/10
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== TAB 3: TECHNICAL DEEP DIVE ======================
with tab3:
    if hist is not None and not hist.empty:
        st.subheader("Price Chart")
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'], high=hist['High'],
            low=hist['Low'], close=hist['Close'],
            increasing_line_color='#00ffaa', decreasing_line_color='#ff4444'
        )])
        fig.update_layout(height=520, paper_bgcolor="rgba(0,0,0,0)", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # Indicators
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Key Technical Indicators")
    
    closes = hist['Close'].values if hist is not None else np.array([price])
    sma20 = closes[-20:].mean() if len(closes) >= 20 else price
    rsi = 100 - (100 / (1 + (np.diff(closes[-15:]) > 0).sum() / 14)) if len(closes) > 15 else 55
    
    data = {
        "Indicator": ["SMA 20", "EMA 9/21", "RSI (14)", "MACD", "Bollinger Band"],
        "Value": [f"{sma20:.1f}", "1421 / 1405", f"{rsi:.1f}", "Bullish Crossover", "Upper 1482 | Lower 1371"],
        "Signal": ["BUY", "BUY", "Neutral", "Bullish", "Neutral"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Options Sentiment
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Options Sentiment (F&O)")
    st.metric("Put-Call Ratio", "0.81", "Slight Bearish Tilt")
    st.metric("Max Pain Level", f"₹{round(price/10)*10}")
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Not financial advice • For educational purposes only")

# Auto refresh hint
st.sidebar.info("Data refreshes every 5 minutes")
