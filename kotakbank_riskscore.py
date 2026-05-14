import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(
    page_title="NSE Risk Score Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .stApp { background-color: #08090d; color: #e0e0e0; }
    .main .block-container { padding-top: 2rem; max-width: 1280px; margin: 0 auto; }
    h1, h2, h3 { font-family: 'DM Sans', sans-serif; }
    .data, table, code { font-family: 'JetBrains Mono', monospace; }
    .glass-card {
        background: rgba(255,255,255,0.06);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .badge {
        padding: 8px 20px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 1.2rem;
    }
    .disclaimer { font-size: 0.85rem; color: #666; text-align: center; padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR ======================
st.sidebar.header("NSE Risk Report")
symbol_input = st.sidebar.text_input("NSE Symbol", value="RELIANCE", help="Without .NS").upper()
stock_symbol = f"{symbol_input}.NS"
fetch_button = st.sidebar.button("🔄 Fetch Live Data", type="primary")

# ====================== DATA FETCH ======================
@st.cache_data(ttl=300)  # 5 minutes cache
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="3mo")
        return info, hist
    except:
        return None, None

if fetch_button or "info" not in st.session_state:
    info, hist = get_stock_data(stock_symbol)
    st.session_state.info = info
    st.session_state.hist = hist

info = st.session_state.get("info")
hist = st.session_state.get("hist")

# Live Values
if info:
    current_price = info.get('currentPrice') or info.get('regularMarketPreviousClose') or 1428.75
    prev_close = info.get('regularMarketPreviousClose') or current_price
    change = round(current_price - prev_close, 2)
    change_pct = round((change / prev_close) * 100, 2) if prev_close else 0
    volume = f"{info.get('volume', 0):,}"
    market_cap = f"₹{info.get('marketCap', 0)/1e7:.2f}L Cr" if info.get('marketCap') else "N/A"
    stock_name = info.get('longName', f"{symbol_input} Ltd.")
else:
    current_price = change = change_pct = 0
    volume = market_cap = "N/A"
    stock_name = f"{symbol_input} Ltd."

# Risk Score (You can enhance this later)
overall_risk_score = 62

# ====================== HEADER ======================
st.markdown(f"""
<div style="text-align:center; margin-bottom:2rem;">
    <h1 style="background: linear-gradient(90deg, #00ffaa, #00ccff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        NSE: {symbol_input} • {stock_name}
    </h1>
    <div style="font-size:2.8rem; font-family:'JetBrains Mono',monospace; font-weight:700;">
        ₹{current_price:,.2f}
    </div>
    <div style="color:{'#00ffaa' if change >= 0 else '#ff4444'}; font-size:1.3rem;">
        {'+' if change >= 0 else ''}₹{change} ({'+' if change_pct >= 0 else ''}{change_pct}%)
    </div>
</div>
""", unsafe_allow_html=True)

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["📊 Risk Overview", "🌌 Sentiment Overlay", "📈 Technical Deep Dive"])

with tab1:
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Overall Risk Score")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_risk_score,
            gauge={'axis': {'range': [0,100]},
                   'bar': {'color': "#00ffaa"}},
            title={'text': "RISK SCORE"}
        ))
        fig.update_layout(height=320, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Trade Plan")
        st.markdown('<span class="badge" style="background:#ffaa0020;color:#ffaa00;border:2px solid #ffaa00;">HOLD</span>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Entry", "1415 – 1435")
            st.metric("Stop Loss", "1388")
        with c2:
            st.metric("Target 1", "1480")
            st.metric("Target 2", "1525")
        st.markdown('</div>', unsafe_allow_html=True)

    # Fundamental Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Fundamental Moat & Valuation")
    colf1, colf2 = st.columns(2)
    with colf1:
        st.metric("PE Ratio", f"{info.get('trailingPE', 24.8):.1f}" if info else "24.8")
        st.metric("Market Cap", market_cap)
    with colf2:
        st.success("DCF Fair Value: ₹1,380 – ₹1,620")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.warning("⚠️ These are supplementary non-traditional tools. Use only as confluence.")
    st.info("Astrological (SBC) + Gann analysis goes here...")

with tab3:
    st.subheader("Price Chart")
    if hist is not None and not hist.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'], high=hist['High'],
            low=hist['Low'], close=hist['Close'],
            increasing_line_color='#00ffaa', decreasing_line_color='#ff4444'
        )])
        fig.update_layout(height=550, xaxis_rangeslider_visible=False, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Click 'Fetch Live Data' to load chart")

st.markdown('<div class="disclaimer">Not financial advice. For educational purposes only.</div>', unsafe_allow_html=True)
