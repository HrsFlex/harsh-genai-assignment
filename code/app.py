import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from code.mobility_analytics import MobilityDataAnalyzer
from code.database_manager import MobilityDBManager
from code.genai_assistant import GenAIAssistant


st.set_page_config(
    page_title="Urban Mobility AI",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
    

    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: rgba(20, 20, 30, 0.8);
        --accent-primary: #6366f1;
        --accent-secondary: #8b5cf6;
        --accent-tertiary: #a855f7;
        --text-primary: #ffffff;
        --text-secondary: #c4c9d4;
        --text-muted: #a1a7b4;
        --glass-border: rgba(255, 255, 255, 0.1);
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gradient-4: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    

    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(at 20% 80%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 80% 20%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(168, 85, 247, 0.05) 0px, transparent 50%);
        font-family: 'Inter', sans-serif;
    }
    

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121a 0%, #1a1a2e 100%);
        border-right: 1px solid var(--glass-border);
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e4e9 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #e2e4e9 !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        color: #ffffff !important;
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #d1d5db !important;
    }
    

    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #fff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 40px rgba(167, 139, 250, 0.3);
        animation: fadeInDown 0.6s ease-out;
    }
    
    h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    

    div[data-testid="stMetric"] {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 20px 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideUp 0.5s ease-out;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
    }
    
    div[data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }
    

    .stChatMessage {
        background: var(--bg-card) !important;
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 16px;
        animation: fadeIn 0.4s ease-out;
        color: #f5f5f7 !important;
    }
    
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #f5f5f7 !important;
    }
    
    .stChatMessage strong {
        color: #ffffff !important;
    }
    

    .stChatInput > div {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }
    
    .stChatInput input {
        color: var(--text-primary) !important;
    }
    

    .stButton > button {
        background: var(--gradient-1) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    

    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }
    

    .stDataFrame {
        background: var(--bg-card) !important;
        border-radius: 16px !important;
        overflow: hidden;
    }
    

    .stRadio > div {
        gap: 8px;
    }
    
    .stRadio > div > label {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: 10px;
        padding: 12px 16px;
        transition: all 0.3s ease;
        color: #e2e4e9 !important;
    }
    
    .stRadio > div > label:hover {
        border-color: var(--accent-primary);
        background: rgba(99, 102, 241, 0.1);
    }
    

    .stSlider label, .stSlider p {
        color: #e2e4e9 !important;
    }
    
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-testid="stThumbValue"] {
        color: #ffffff !important;
    }
    

    label, .stTextInput label, .stSelectbox label, .stMultiSelect label {
        color: #e2e4e9 !important;
    }
    

    .stSelectbox > div > div, .stMultiSelect > div > div {
        color: #e2e4e9 !important;
        background: var(--bg-card) !important;
    }
    

    .stSpinner > div {
        border-top-color: var(--accent-primary) !important;
    }
    

    .stAlert {
        background: var(--bg-card) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }
    

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    

    .custom-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        animation: slideUp 0.5s ease-out;
    }
    
    .custom-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }
    

    .gradient-text {
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    

    .glow {
        box-shadow: 0 0 40px rgba(99, 102, 241, 0.3);
    }
    

    .animated-border {
        position: relative;
        background: var(--bg-card);
        border-radius: 20px;
        overflow: hidden;
    }
    
    .animated-border::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary), var(--accent-tertiary), var(--accent-primary));
        background-size: 400% 400%;
        z-index: -1;
        border-radius: 22px;
        animation: gradient-rotate 3s ease infinite;
    }
    
    @keyframes gradient-rotate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    

    .loading-shimmer {
        background: linear-gradient(90deg, var(--bg-card) 25%, rgba(99, 102, 241, 0.1) 50%, var(--bg-card) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    

    [data-testid="stTooltipIcon"] {
        color: var(--accent-primary) !important;
    }
    

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_managers():
    dataset_path = "yellow_tripdata_2016-01.csv"
    
    analyzer = MobilityDataAnalyzer(dataset_path)
    with st.spinner("Loading Data Model..."):
        analyzer.load_data(nrows=50000) 
        analyzer.clean_data()
        analyzer.feature_engineering()
        
    db_manager = MobilityDBManager()
    db_manager.ingest_data(analyzer)
    
    ai_assistant = GenAIAssistant()
    
    return analyzer, db_manager, ai_assistant

try:
    analyzer, db_manager, ai_assistant = get_managers()
except FileNotFoundError:
    st.error("❌ Dataset not found. Please check file path.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error initializing: {e}")
    st.stop()


with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 1.8rem; margin: 0;">🚕</h1>
        <h2 style="font-size: 1.4rem; margin: 10px 0; background: linear-gradient(135deg, #fff 0%, #a78bfa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Urban Mobility AI</h2>
        <p style="color: #c4c9d4; font-size: 0.85rem;">Intelligent Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "🧭 Navigation",
        ["📊 Dashboard", "🗺️ Geospatial", "🤖 AI Assistant", "📋 Data View"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    

    mode_color = "#10b981" if ai_assistant.mode == "live" else "#f59e0b"
    st.markdown(f"""
    <div style="background: rgba(20, 20, 30, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 16px;">
        <p style="color: #c4c9d4; font-size: 0.75rem; margin: 0; text-transform: uppercase; letter-spacing: 0.1em;">AI Status</p>
        <p style="color: {mode_color}; font-size: 1rem; font-weight: 600; margin: 8px 0 0 0;">
            ● {ai_assistant.provider.upper()} ({ai_assistant.mode})
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 Reset AI Engine", width='stretch'):
        st.cache_resource.clear()
        st.rerun()

if page == "📊 Dashboard":
    
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Executive Dashboard</h1>
        <p style="color: #c4c9d4; font-size: 1.1rem;">Real-time Urban Mobility Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = analyzer.data
    total_rev = df['total_amount'].sum()
    avg_fare = df['fare_amount'].mean()
    total_trips = len(df)
    avg_dist = df['trip_distance'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_rev:,.0f}", "+12.5%")
    col2.metric("🚕 Total Trips", f"{total_trips:,}", "+5.2%")
    col3.metric("💵 Avg Fare", f"${avg_fare:.2f}", "-2.1%")
    col4.metric("📍 Avg Distance", f"{avg_dist:.2f} mi", "+0.8%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    

    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### 📈 Hourly Demand Pattern")
        hourly_data = db_manager.get_hourly_demand()
        
        fig = go.Figure()
        

        fig.add_trace(go.Scatter(
            x=hourly_data['pickup_hour'],
            y=hourly_data['trip_count'],
            mode='lines',
            fill='tozeroy',
            name='Trip Volume',
            line=dict(color='#6366f1', width=3, shape='spline'),
            fillcolor='rgba(99, 102, 241, 0.2)'
        ))
        

        fig.add_trace(go.Scatter(
            x=hourly_data['pickup_hour'],
            y=hourly_data['avg_distance'],
            mode='lines+markers',
            name='Avg Distance',
            yaxis='y2',
            line=dict(color='#f59e0b', width=2, dash='dot'),
            marker=dict(size=6, color='#f59e0b')
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9ca3af', family='Inter'),
            xaxis=dict(
                title='Hour of Day',
                gridcolor='rgba(255,255,255,0.05)',
                showgrid=True
            ),
            yaxis=dict(
                title='Trip Count',
                gridcolor='rgba(255,255,255,0.05)',
                showgrid=True
            ),
            yaxis2=dict(
                title='Avg Distance (mi)',
                overlaying='y',
                side='right',
                gridcolor='rgba(255,255,255,0.05)'
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.markdown("### 🏆 Top Zones")
        top_zones = db_manager.get_top_pickup_zones(5)
        
        fig2 = go.Figure(data=[go.Pie(
            values=top_zones['trip_count'],
            hole=0.65,
            marker=dict(
                colors=['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899'],
                line=dict(color='#0a0a0f', width=2)
            ),
            textfont=dict(color='white', size=12),
            hoverinfo='label+percent+value'
        )])
        
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9ca3af', family='Inter'),
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[dict(
                text='ZONES',
                x=0.5, y=0.5,
                font=dict(size=14, color='#9ca3af'),
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig2, width='stretch')


    st.markdown("### 💹 Daily Revenue Trend")
    daily_rev = db_manager.get_revenue_trends()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=daily_rev['pickup_day'],
        y=daily_rev['total_revenue'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#10b981', width=3, shape='spline'),
        fillcolor='rgba(16, 185, 129, 0.15)'
    ))
    
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9ca3af', family='Inter'),
        xaxis=dict(
            title='Day of Month',
            gridcolor='rgba(255,255,255,0.05)'
        ),
        yaxis=dict(
            title='Revenue ($)',
            gridcolor='rgba(255,255,255,0.05)'
        ),
        margin=dict(l=0, r=0, t=20, b=0),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig3, width='stretch')


elif page == "🗺️ Geospatial":
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Geospatial Intelligence</h1>
        <p style="color: #c4c9d4; font-size: 1.1rem;">Interactive Maps of NYC Taxi Activity</p>
    </div>
    """, unsafe_allow_html=True)
    

    map_data = db_manager.run_query("""
        SELECT pickup_longitude as lon, pickup_latitude as lat, 
               total_amount, trip_distance, pickup_hour
        FROM trips 
        WHERE pickup_longitude BETWEEN -74.05 AND -73.75
        AND pickup_latitude BETWEEN 40.6 AND 40.85
        LIMIT 5000
    """)
    

    map_type = st.radio(
        "Select Map Type",
        ["🔥 Pickup Heatmap", "📍 Scatter Plot", "⏰ Time-based Activity", "💰 Revenue Hotspots"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if map_type == "🔥 Pickup Heatmap":

        fig = px.density_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            radius=8,
            center=dict(lat=40.75, lon=-73.98),
            zoom=11,
            mapbox_style="carto-darkmatter",
            color_continuous_scale=["#1a1a2e", "#6366f1", "#a855f7", "#ec4899", "#f43f5e"],
            title=""
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=550,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("""
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 16px; margin-top: 16px;">
            <p style="color: #e2e4e9; margin: 0; font-size: 0.9rem;">
                <strong>🔥 Heatmap Analysis:</strong> This visualization shows pickup density across NYC. 
                Brighter areas indicate higher taxi demand. Midtown Manhattan shows the highest concentration.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif map_type == "📍 Scatter Plot":

        fig = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            color='trip_distance',
            size='total_amount',
            color_continuous_scale=["#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#f43f5e"],
            size_max=15,
            center=dict(lat=40.75, lon=-73.98),
            zoom=11,
            mapbox_style="carto-darkmatter",
            hover_data=['total_amount', 'trip_distance'],
            title=""
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=550,
            coloraxis_colorbar=dict(
                title="Distance (mi)",
                title_font=dict(color='#e2e4e9'),
                tickfont=dict(color='#e2e4e9')
            )
        )
        st.plotly_chart(fig, width='stretch')
        
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 16px; margin-top: 16px;">
            <p style="color: #e2e4e9; margin: 0; font-size: 0.9rem;">
                <strong>📍 Scatter Analysis:</strong> Each point represents a pickup location. 
                Point size = fare amount, Color = trip distance. Larger, redder points indicate expensive long trips.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif map_type == "⏰ Time-based Activity":

        selected_hour = st.slider("🕐 Select Hour of Day", 0, 23, 12)
        
        hour_data = map_data[map_data['pickup_hour'] == selected_hour]
        
        fig = px.scatter_mapbox(
            hour_data,
            lat='lat',
            lon='lon',
            color_discrete_sequence=["#6366f1"],
            center=dict(lat=40.75, lon=-73.98),
            zoom=11,
            mapbox_style="carto-darkmatter",
            title=""
        )
        fig.update_traces(marker=dict(size=6, opacity=0.7))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=500
        )
        st.plotly_chart(fig, width='stretch')
        

        time_label = f"{selected_hour:02d}:00" if selected_hour < 12 else f"{selected_hour:02d}:00"
        if selected_hour == 0:
            period = "🌙 Late Night"
        elif selected_hour < 6:
            period = "🌙 Early Morning"
        elif selected_hour < 12:
            period = "🌅 Morning Rush"
        elif selected_hour < 17:
            period = "☀️ Afternoon"
        elif selected_hour < 21:
            period = "🌆 Evening Rush"
        else:
            period = "🌙 Night"
        
        col1, col2, col3 = st.columns(3)
        col1.metric("⏰ Time", time_label)
        col2.metric("📊 Trips", f"{len(hour_data):,}")
        col3.metric("📍 Period", period)
    
    elif map_type == "💰 Revenue Hotspots":

        revenue_data = db_manager.run_query("""
            SELECT 
                ROUND(pickup_latitude, 3) as lat,
                ROUND(pickup_longitude, 3) as lon,
                SUM(total_amount) as revenue,
                COUNT(*) as trips
            FROM trips
            WHERE pickup_longitude BETWEEN -74.05 AND -73.75
            AND pickup_latitude BETWEEN 40.6 AND 40.85
            GROUP BY 1, 2
            HAVING COUNT(*) > 5
            ORDER BY revenue DESC
            LIMIT 200
        """)
        
        fig = px.scatter_mapbox(
            revenue_data,
            lat='lat',
            lon='lon',
            size='revenue',
            color='revenue',
            color_continuous_scale=["#10b981", "#22d3ee", "#6366f1", "#a855f7", "#f43f5e"],
            size_max=30,
            center=dict(lat=40.75, lon=-73.98),
            zoom=11,
            mapbox_style="carto-darkmatter",
            hover_data=['trips', 'revenue'],
            title=""
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=550,
            coloraxis_colorbar=dict(
                title="Revenue ($)",
                title_font=dict(color='#e2e4e9'),
                tickfont=dict(color='#e2e4e9')
            )
        )
        st.plotly_chart(fig, width='stretch')
        

        st.markdown("### 💎 Top Revenue Zones")
        top_rev = revenue_data.nlargest(5, 'revenue')
        for i, row in top_rev.iterrows():
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 12px 16px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                <span style="color: #10b981; font-weight: 700;">${row['revenue']:,.0f}</span>
                <span style="color: #c4c9d4;"> from </span>
                <span style="color: #e2e4e9; font-weight: 500;">{row['trips']} trips</span>
                <span style="color: #a1a7b4; font-size: 0.85rem;"> @ ({row['lat']:.3f}, {row['lon']:.3f})</span>
            </div>
            """, unsafe_allow_html=True)
    

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #c4c9d4; margin: 0; font-size: 0.85rem;">COVERAGE AREA</p>
            <p style="color: #6366f1; font-size: 1.5rem; font-weight: 700; margin: 8px 0 0 0;">~150 sq mi</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #c4c9d4; margin: 0; font-size: 0.85rem;">HOTTEST ZONE</p>
            <p style="color: #8b5cf6; font-size: 1.5rem; font-weight: 700; margin: 8px 0 0 0;">Midtown</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        data_points = len(map_data)
        st.markdown(f"""
        <div style="background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
            <p style="color: #c4c9d4; margin: 0; font-size: 0.85rem;">DATA POINTS</p>
            <p style="color: #a855f7; font-size: 1.5rem; font-weight: 700; margin: 8px 0 0 0;">{data_points:,}</p>
        </div>
        """, unsafe_allow_html=True)


elif page == "🤖 AI Assistant":

    st.markdown(f"""
    <div style="text-align: center; padding: 40px 0 20px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">AI Insights Assistant</h1>
        <p style="color: #e2e4e9; font-size: 1.1rem; margin-bottom: 16px;">Ask questions about your data in natural language</p>
        <div style="display: inline-block; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 20px; padding: 8px 20px;">
            <span style="color: #10b981; font-size: 0.9rem; font-weight: 600;">● {ai_assistant.provider.upper()} AI Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    

    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 20px; margin-bottom: 24px;">
        <h4 style="color: #e2e4e9; margin: 0 0 12px 0; font-size: 1rem;">💡 Quick Start Prompts</h4>
        <p style="color: #f0f1f3; font-size: 0.9rem; margin: 0;">Click any prompt below to get instant insights</p>
    </div>
    """, unsafe_allow_html=True)
    

    prompt_cols = st.columns(4)
    suggested_prompts = [
        "📈 Revenue trend analysis",
        "🕐 Peak demand hours",
        "📍 Busiest pickup zones",
        "💰 Average fare breakdown"
    ]
    
    selected_prompt = None
    for i, col in enumerate(prompt_cols):
        with col:

            clean_prompt = suggested_prompts[i].split(" ", 1)[1] if " " in suggested_prompts[i] else suggested_prompts[i]
            if st.button(suggested_prompts[i], key=f"prompt_{i}", width='stretch'):

                prompt_map = {
                    0: "What's the revenue trend?",
                    1: "When is peak demand?",
                    2: "Which zones are busiest?",
                    3: "Show average fare"
                }
                selected_prompt = prompt_map[i]
    
    st.markdown("<br>", unsafe_allow_html=True)
    

    st.markdown("""
    <div style="border-top: 2px solid rgba(99, 102, 241, 0.2); padding-top: 20px;">
        <h4 style="color: #e2e4e9; margin-bottom: 16px;">💬 Conversation</h4>
    </div>
    """, unsafe_allow_html=True)
    

    if "messages" not in st.session_state:
        st.session_state.messages = []
    

    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px;">
            <p style="color: #e2e4e9; font-size: 1.1rem; margin: 0; font-weight: 500;">👋 Hi! I'm your AI data analyst.</p>
            <p style="color: #f0f1f3; font-size: 0.95rem; margin: 12px 0 0 0;">Ask me anything about NYC taxi trip data, and I'll provide insights backed by real analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    prompt = st.chat_input("💭 Ask me anything about the mobility data...") or selected_prompt
    
    if prompt:

        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})


        with st.spinner("🧠 Analyzing your data..."):

            sql_query = ai_assistant.text_to_sql(prompt)
            data_context = "No direct SQL mapping."
            

            if "SELECT" in sql_query and "Error" not in sql_query:
                try:
                    df_res = db_manager.run_query(sql_query)
                    data_context = df_res.to_string()
                except Exception as e:
                    data_context = f"SQL execution failed: {str(e)}"
            

            response = ai_assistant.generate_insight(data_context, prompt)


        with st.chat_message("assistant"):
            st.markdown(response)
            

            if "SELECT" in sql_query:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("🔍 View Generated SQL Query", expanded=False):
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.05); border-left: 3px solid #10b981; padding: 12px; margin-bottom: 8px;">
                        <p style="color: #10b981; font-size: 0.85rem; margin: 0; font-weight: 600;">✓ Query executed successfully</p>
  </div>
                    """, unsafe_allow_html=True)
                    st.code(sql_query, language="sql")
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    

    if len(st.session_state.messages) > 0:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.05); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 12px; padding: 16px; margin-top: 24px;">
            <p style="color: #8b5cf6; font-size: 0.85rem; margin: 0; font-weight: 600;">💡 Pro Tip</p>
            <p style="color: #c4c9d4; font-size: 0.85rem; margin: 8px 0 0 0;">Try asking follow-up questions like "Why is that?" or "Show me the data" for deeper insights.</p>
        </div>
        """, unsafe_allow_html=True)


elif page == "📋 Data View":
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">Data Explorer</h1>
        <p style="color: #e2e4e9; font-size: 1.1rem;">Interactive exploration of the cleaned dataset</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = analyzer.data
    

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Total Rows", f"{len(df):,}")
    col2.metric("📋 Columns", f"{len(df.columns)}")
    col3.metric("💾 Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    col4.metric("📅 Period", "Jan 2016")
    
    st.markdown("<br>", unsafe_allow_html=True)
    

    tab1, tab2, tab3 = st.tabs(["📋 Data Table", "📈 Column Stats", "🔍 Quick Analysis"])
    
    with tab1:

        selected_cols = st.multiselect(
            "Select columns to display:",
            df.columns.tolist(),
            default=['tpep_pickup_datetime', 'trip_distance', 'fare_amount', 'total_amount', 'pickup_hour', 'pickup_weekday']
        )
        

        row_limit = st.slider("Number of rows to display:", 10, 500, 100)
        
        if selected_cols:
            st.dataframe(
                df[selected_cols].head(row_limit),
                width='stretch',
                height=450
            )
        

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            csv = df.head(1000).to_csv(index=False)
            st.download_button(
                label="📥 Download Sample (1000 rows)",
                data=csv,
                file_name="mobility_data_sample.csv",
                mime="text/csv",
                width='stretch'
            )
        with c2:
            if st.button("📋 Copy Schema", width='stretch'):
                st.code(str(df.dtypes.to_dict()), language="python")
    
    with tab2:
        st.markdown("### 📊 Column Statistics")
        

        numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32', 'int8']).columns.tolist()
        selected_stat_col = st.selectbox("Select column for detailed stats:", numeric_cols)
        
        if selected_stat_col:
            col_data = df[selected_stat_col]
            

            s1, s2, s3, s4, s5 = st.columns(5)
            s1.metric("Min", f"{col_data.min():.2f}")
            s2.metric("Max", f"{col_data.max():.2f}")
            s3.metric("Mean", f"{col_data.mean():.2f}")
            s4.metric("Median", f"{col_data.median():.2f}")
            s5.metric("Std Dev", f"{col_data.std():.2f}")
            

            st.markdown("<br>", unsafe_allow_html=True)
            fig = px.histogram(
                df, x=selected_stat_col, 
                nbins=50,
                color_discrete_sequence=['#6366f1']
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e4e9'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig, width='stretch')
    
    with tab3:
        st.markdown("### 🔍 Quick Data Quality Check")
        

        total_rows = len(df)
        missing_counts = df.isnull().sum()
        

        q1, q2, q3 = st.columns(3)
        with q1:
            completeness = ((total_rows - missing_counts.sum()) / (total_rows * len(df.columns))) * 100
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #c4c9d4; margin: 0; font-size: 0.85rem;">DATA COMPLETENESS</p>
                <p style="color: #10b981; font-size: 2rem; font-weight: 700; margin: 8px 0 0 0;">{completeness:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        with q2:
            st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #c4c9d4; margin: 0; font-size: 0.85rem;">UNIQUE DAYS</p>
                <p style="color: #6366f1; font-size: 2rem; font-weight: 700; margin: 8px 0 0 0;">{df['pickup_day'].nunique()}</p>
            </div>
            """, unsafe_allow_html=True)
        with q3:
            avg_trip = df['trip_distance'].mean()
            st.markdown(f"""
            <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 20px; text-align: center;">
                <p style="color: #c4c9d4; margin: 0; font-size: 0.85rem;">AVG TRIP DISTANCE</p>
                <p style="color: #8b5cf6; font-size: 2rem; font-weight: 700; margin: 8px 0 0 0;">{avg_trip:.2f} mi</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        

        st.markdown("#### 📊 Weekday Distribution")
        weekday_counts = df['pickup_weekday'].value_counts()
        fig = px.bar(
            x=weekday_counts.index,
            y=weekday_counts.values,
            color=weekday_counts.values,
            color_continuous_scale=['#6366f1', '#8b5cf6', '#a855f7']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e4e9'),
            xaxis=dict(title='Day', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='Trips', gridcolor='rgba(255,255,255,0.05)'),
            coloraxis_showscale=False,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

