"""
MONARCH CASTLE TECHNOLOGIES
Unified Intelligence Dashboard
==============================
A command center interface displaying all intelligence feeds.

Usage:
    streamlit run dashboard.py

Opens in browser at: http://localhost:8501
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Monarch Castle Intelligence",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DARK MODE STYLING (Black & Gold Theme)
# ============================================================================

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213e 0%, #0f0f23 100%);
        border-right: 2px solid #d4af37;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #d4af37 !important;
        font-family: 'Georgia', serif;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #d4af37;
        border-radius: 10px;
        padding: 15px;
    }
    
    [data-testid="stMetricValue"] {
        color: #d4af37 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a2e;
        border: 1px solid #d4af37;
        color: #d4af37;
        border-radius: 5px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #d4af37 !important;
        color: #0a0a0a !important;
    }
    
    /* Alert boxes */
    .high-alert {
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .low-alert {
        background: linear-gradient(135deg, #006400 0%, #228B22 100%);
        border: 2px solid #00FF00;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(90deg, #0a0a0a 0%, #16213e 50%, #0a0a0a 100%);
        border-top: 2px solid #d4af37;
        padding: 10px;
        text-align: center;
        color: #d4af37;
        font-family: 'Courier New', monospace;
        z-index: 1000;
    }
    
    .status-online {
        color: #00FF00;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("# 🏰 MONARCH CASTLE")
    st.markdown("### TECHNOLOGIES")
    st.markdown("---")
    st.markdown("*\"The Palantir of Türkiye\"*")
    st.markdown("")
    st.markdown("**Intelligence Divisions:**")
    st.markdown("- 📊 MCFI - Financial Intel")
    st.markdown("- 🍕 MCEI - Enjoy Intel")
    st.markdown("- 🌍 MCDI - Defense Intel")
    st.markdown("---")
    st.markdown(f"**Last Update:**")
    st.markdown(f"`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

# ============================================================================
# HEADER
# ============================================================================

st.markdown("# 🏰 MONARCH CASTLE INTELLIGENCE DASHBOARD")
st.markdown("---")

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_inflation_data():
    """Load inflation data from CSV."""
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "MVP 1 - Inflation Intelligence Agency (IIA)",
        "inflation_data.csv"
    )
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        return df
    return None

def load_defense_data():
    """Load defense signals from CSV."""
    csv_path = os.path.join(
        os.path.dirname(__file__),
        "Pizza Stores Around Pentagon Tracker",
        "defense_signals.csv"
    )
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df
    return None

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Turkey Inflation Monitor", 
    "🍕 Global Threat Level",
    "📈 System Overview"
])

# ---------------------------------------------------------------------------
# TAB 1: INFLATION MONITOR
# ---------------------------------------------------------------------------

with tab1:
    st.markdown("## 🇹🇷 Turkey Inflation Intelligence")
    st.markdown("*Real-time price tracking from Turkish supermarkets*")
    
    inflation_df = load_inflation_data()
    
    if inflation_df is not None and len(inflation_df) > 0:
        # Calculate inflation metrics
        products = inflation_df.groupby('Product_Name')
        
        col1, col2, col3 = st.columns(3)
        
        # Calculate total basket change
        first_date_totals = inflation_df[
            inflation_df['Date'] == inflation_df['Date'].min()
        ].groupby('Product_Name')['Price'].first().sum()
        
        last_date_totals = inflation_df[
            inflation_df['Date'] == inflation_df['Date'].max()
        ].groupby('Product_Name')['Price'].last().sum()
        
        if first_date_totals > 0:
            inflation_rate = ((last_date_totals - first_date_totals) / first_date_totals) * 100
        else:
            inflation_rate = 0
        
        with col1:
            st.metric(
                label="MONARCH INFLATION INDEX",
                value=f"{inflation_rate:+.2f}%",
                delta=f"vs. first reading"
            )
        
        with col2:
            st.metric(
                label="Current Basket Total",
                value=f"₺{last_date_totals:.2f}",
                delta=f"₺{last_date_totals - first_date_totals:+.2f}"
            )
        
        with col3:
            st.metric(
                label="Products Tracked",
                value=len(inflation_df['Product_Name'].unique())
            )
        
        st.markdown("---")
        
        # Line chart of prices over time
        fig = px.line(
            inflation_df,
            x='DateTime',
            y='Price',
            color='Product_Name',
            title='Price Trends Over Time',
            template='plotly_dark'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#d4af37',
            title_font_color='#d4af37',
            legend_title_font_color='#d4af37',
            xaxis=dict(gridcolor='#333333'),
            yaxis=dict(gridcolor='#333333', title='Price (TL)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        with st.expander("📋 View Raw Data"):
            st.dataframe(
                inflation_df.sort_values('DateTime', ascending=False),
                use_container_width=True
            )
    
    else:
        st.warning("⚠️ No inflation data available yet.")
        st.markdown("""
        **To collect data, run:**
        ```bash
        cd "MVP 1 - Inflation Intelligence Agency (IIA)"
        python inflation_tracker.py
        ```
        """)
        
        # Demo data for visualization
        st.markdown("---")
        st.markdown("### 📉 Demo Visualization (Sample Data)")
        
        demo_data = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=10, freq='D'),
            'Product': ['Milk'] * 10,
            'Price': [45.90, 46.50, 47.20, 47.90, 48.50, 49.00, 49.90, 50.50, 51.20, 52.00]
        })
        
        fig = px.line(
            demo_data,
            x='Date',
            y='Price',
            title='Sample: Milk Price Trend (Demo)',
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#d4af37'
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 2: GLOBAL THREAT LEVEL
# ---------------------------------------------------------------------------

with tab2:
    st.markdown("## 🌍 Pentagon Activity Monitor")
    st.markdown("*OSINT tracking of late-night activity near intelligence hubs*")
    
    defense_df = load_defense_data()
    
    if defense_df is not None and len(defense_df) > 0:
        # Get latest reading
        latest = defense_df.iloc[-1]
        
        # Check overall risk level
        high_risk_count = len(defense_df[defense_df['Risk_Score'] == 'HIGH'])
        latest_risk = latest['Risk_Score']
        
        # Display alert banner
        if latest_risk == 'HIGH':
            st.markdown("""
            <div class="high-alert">
                <h1>🚨 DEFCON 3</h1>
                <h2>LATE NIGHT MUNCHIES DETECTED</h2>
                <p>Unusual activity detected at Pentagon-area food outlets</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="low-alert">
                <h1>✅ ALL CLEAR</h1>
                <h2>NORMAL OPERATIONS</h2>
                <p>No unusual activity detected</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Current Status",
                value=latest_risk
            )
        
        with col2:
            st.metric(
                label="Last Check",
                value=latest['Timestamp'][:19] if len(str(latest['Timestamp'])) > 19 else str(latest['Timestamp'])
            )
        
        with col3:
            st.metric(
                label="Historical High Alerts",
                value=high_risk_count
            )
        
        st.markdown("---")
        
        # Store-by-store breakdown
        st.markdown("### 📍 Location Status")
        
        latest_timestamp = defense_df['Timestamp'].max()
        latest_readings = defense_df[defense_df['Timestamp'] == latest_timestamp]
        
        for _, row in latest_readings.iterrows():
            risk_color = "🔴" if row['Risk_Score'] == 'HIGH' else "🟡" if row['Risk_Score'] == 'ELEVATED' else "🟢"
            st.markdown(f"**{risk_color} {row['Store_Name']}**")
            st.markdown(f"   Status: {row['Busyness_Status']} | Risk: {row['Risk_Score']}")
        
        # History table
        with st.expander("📋 View Signal History"):
            st.dataframe(
                defense_df.sort_values('Timestamp', ascending=False),
                use_container_width=True
            )
    
    else:
        st.warning("⚠️ No defense signals available yet.")
        st.markdown("""
        **To collect data, run:**
        ```bash
        cd "Pizza Stores Around Pentagon Tracker"
        python pentagon_pizza.py
        ```
        """)
        
        # Display demo banner
        st.markdown("---")
        st.markdown("### Demo Status Display")
        st.markdown("""
        <div class="low-alert">
            <h1>✅ ALL CLEAR</h1>
            <h2>NORMAL OPERATIONS</h2>
            <p>System awaiting first data collection</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TAB 3: SYSTEM OVERVIEW
# ---------------------------------------------------------------------------

with tab3:
    st.markdown("## 📈 System Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Active Modules")
        
        modules = [
            ("Inflation Intelligence Agency", "IIA", inflation_df is not None),
            ("Pentagon Pizza Tracker", "MCEI", defense_df is not None),
            ("Border Threat Index", "BNTI", False),
            ("Sahel Region Watch", "SRTI", False),
            ("Oil Price Oracle", "OPI", False),
            ("NATO Burden Tracker", "NATO", False),
            ("Cloudy&Shiny Index", "CSI", False),
            ("Baltic Dry Predictor", "BDI", False),
        ]
        
        for name, code, active in modules:
            status = "🟢 ONLINE" if active else "⚪ STANDBY"
            st.markdown(f"**{code}** - {name}: {status}")
    
    with col2:
        st.markdown("### 📊 Data Summary")
        
        inflation_count = len(inflation_df) if inflation_df is not None else 0
        defense_count = len(defense_df) if defense_df is not None else 0
        
        st.metric("Inflation Records", inflation_count)
        st.metric("Defense Signals", defense_count)
        st.metric("Total Data Points", inflation_count + defense_count)
    
    st.markdown("---")
    st.markdown("### 🛠️ Quick Commands")
    st.code("""
# Run Inflation Tracker
python "MVP 1 - Inflation Intelligence Agency (IIA)/inflation_tracker.py"

# Run Pentagon Pizza Tracker
python "Pizza Stores Around Pentagon Tracker/pentagon_pizza.py"

# Launch Dashboard
streamlit run dashboard.py
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class="footer">
    <span class="status-online">●</span> System Status: ONLINE | 
    <strong>MONARCH CASTLE TECHNOLOGIES</strong> | 
    <em>"The chart doesn't lie."</em>
</div>
""", unsafe_allow_html=True)

# Add spacing for footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
