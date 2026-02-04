"""
Ethiopia Financial Inclusion Forecasting Dashboard
Streamlit application for exploring data and forecasts
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Forecast",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3B82F6;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .positive {
        color: #10B981;
    }
    .negative {
        color: #EF4444;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #93C5FD;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">📈 Ethiopia Financial Inclusion Forecasting Dashboard</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
    <strong>About this dashboard:</strong> This interactive tool provides forecasts for Ethiopia's financial inclusion 
    indicators (2025-2027) based on historical data, event impacts, and scenario analysis. 
    Use the sidebar to navigate between sections.
</div>
""", unsafe_allow_html=True)

# Function to get correct file paths
def get_file_path(filename):
    """Get correct path whether running from dashboard or project root"""
    # Try multiple possible locations
    possible_paths = [
        filename,  # Direct path
        os.path.join('..', filename),  # From dashboard folder
        os.path.join('../data', filename.split('/')[-1]),  # From project root
        os.path.join('data', filename.split('/')[-1]),  # Relative to dashboard
        os.path.join('.', filename.split('/')[-1])  # Current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If file doesn't exist, return original path
    return filename

# Load data with better error handling
@st.cache_data
def load_data():
    """Load forecast data and processed datasets"""
    data = {}
    
    # List of required files and their types
    files_to_load = {
        'account_forecast': 'data/processed/account_ownership_forecast_2025_2027.csv',
        'p2p_forecast': 'data/processed/p2p_transaction_forecast_2025_2027.csv',
        'scenarios': 'data/processed/account_ownership_scenarios.csv',
        'enriched': 'data/processed/ethiopia_fi_enriched.csv',
        'impact_matrix': 'data/processed/event_indicator_association_matrix.csv',
        'historical': 'data/raw/ethiopia_fi_unified_data.csv'
    }
    
    for key, filename in files_to_load.items():
        try:
            filepath = get_file_path(filename)
            if os.path.exists(filepath):
                data[key] = pd.read_csv(filepath)
                st.success(f"✓ Loaded {filename.split('/')[-1]}")
            else:
                st.warning(f"⚠ File not found: {filename}")
                data[key] = pd.DataFrame()
        except Exception as e:
            st.error(f"✗ Error loading {filename}: {str(e)[:100]}")
            data[key] = pd.DataFrame()
    
    # If no data loaded, create demo data
    if all(df.empty for df in data.values()):
        st.info("📊 Using demo data for demonstration purposes")
        data = create_demo_data()
    
    return data

def create_demo_data():
    """Create demo data if real data files are missing"""
    data = {}
    
    # Demo account forecast
    data['account_forecast'] = pd.DataFrame({
        'year': [2025, 2026, 2027],
        'forecast': [54.2, 56.8, 59.4],
        'trend_only': [53.5, 55.9, 58.3],
        'event_impact': [0.7, 0.9, 1.1],
        'events_applied': ['5G Launch, EthioPay', 'None', 'None']
    })
    
    # Demo P2P forecast
    data['p2p_forecast'] = pd.DataFrame({
        'year': [2025, 2026, 2027],
        'forecast': [157.1e6, 188.5e6, 226.2e6],
        'trend_only': [150.0e6, 180.0e6, 216.0e6],
        'event_impact': [7.1e6, 8.5e6, 10.2e6],
        'events_applied': ['Tax Exemption', 'None', 'None']
    })
    
    # Demo scenarios
    data['scenarios'] = pd.DataFrame({
        'year': [2025, 2026, 2027],
        'indicator': ['ACC_OWNERSHIP', 'ACC_OWNERSHIP', 'ACC_OWNERSHIP'],
        'optimistic': [57.3, 60.1, 62.9],
        'baseline': [54.2, 56.8, 59.4],
        'pessimistic': [51.1, 53.5, 55.9]
    })
    
    # Demo historical data
    data['historical'] = pd.DataFrame({
        'record_id': ['REC_0001', 'REC_0002', 'REC_0003', 'EVT_0001', 'EVT_0002'],
        'record_type': ['observation', 'observation', 'observation', 'event', 'event'],
        'indicator': ['Account Ownership', 'Account Ownership', 'Mobile Money Accounts', 'Telebirr Launch', 'M-Pesa Launch'],
        'indicator_code': ['ACC_OWNERSHIP', 'ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'EVT_TELEBIRR', 'EVT_MPESA'],
        'observation_date': ['2014-12-31', '2017-12-31', '2021-12-31', '2021-05-17', '2023-08-01'],
        'value_numeric': [22.0, 35.0, 4.7, None, None],
        'gender': ['all', 'all', 'all', 'all', 'all'],
        'location': ['national', 'national', 'national', 'national', 'national'],
        'source_name': ['Global Findex', 'Global Findex', 'Global Findex', 'Ethio Telecom', 'Safaricom'],
        'notes': ['Baseline year', 'Growth from 2014', 'Mobile money introduction', 'First major mobile money service', 'Second mobile money entrant']
    })
    
    # Demo enriched data
    data['enriched'] = data['historical'].copy()
    
    # Demo impact matrix
    data['impact_matrix'] = pd.DataFrame({
        'event_date': ['2021-05-17', '2023-08-01'],
        'category': ['product_launch', 'market_entry'],
        'ACC_OWNERSHIP': ['increase 0.5pp', 'increase 0.3pp'],
        'ACC_MM_ACCOUNT': ['increase 2.0pp', 'increase 1.5pp'],
        'USG_P2P_COUNT': ['increase 25%', 'increase 15%']
    }, index=['EVT_TELEBIRR', 'EVT_MPESA'])
    
    return data

# Load all data
with st.spinner('Loading data...'):
    data = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select Section",
    ["📊 Overview", "📈 Trends & Forecasts", "🎯 Inclusion Projections", 
     "⚡ Event Impacts", "📋 Data Explorer", "ℹ️ About"]
)

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

# Year filter
years = list(range(2011, 2028))
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=min(years),
    max_value=max(years),
    value=(2014, 2027)
)

# Scenario filter
scenario_options = ["Baseline", "Optimistic", "Pessimistic"]
selected_scenario = st.sidebar.selectbox(
    "Select Scenario",
    scenario_options,
    index=0
)

# ==================== SECTION 1: OVERVIEW ====================
if section == "📊 Overview":
    st.markdown('<h2 class="sub-header">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not data['historical'].empty:
            current_account = data['historical'][
                (data['historical']['indicator_code'] == 'ACC_OWNERSHIP') &
                (data['historical']['record_type'] == 'observation') &
                (data['historical']['gender'] == 'all')
            ]
            if not current_account.empty:
                latest_acc = current_account.iloc[-1]['value_numeric']
                if len(current_account) > 1:
                    delta = latest_acc - current_account.iloc[-2]['value_numeric']
                else:
                    delta = None
                st.metric(
                    label="Current Account Ownership",
                    value=f"{latest_acc:.1f}%" if pd.notna(latest_acc) else "N/A",
                    delta=f"{delta:.1f}%" if delta is not None else None
                )
            else:
                st.metric("Current Account Ownership", "N/A")
        else:
            st.metric("Current Account Ownership", "N/A")
    
    with col2:
        target_2025 = 70  # NFIS-II target
        if 'latest_acc' in locals() and pd.notna(latest_acc):
            gap = target_2025 - latest_acc
            st.metric(
                label="Gap to 2025 Target",
                value=f"{gap:.1f}pp",
                delta_color="inverse"
            )
        else:
            st.metric("Gap to 2025 Target", "N/A")
    
    with col3:
        if not data['historical'].empty:
            p2p_data = data['historical'][
                (data['historical']['indicator_code'] == 'USG_P2P_COUNT') &
                (data['historical']['record_type'] == 'observation')
            ]
            if not p2p_data.empty:
                latest_p2p = p2p_data.iloc[-1]['value_numeric'] / 1e6
                if len(p2p_data) > 1:
                    prev_p2p = p2p_data.iloc[-2]['value_numeric'] / 1e6
                    delta_pct = ((latest_p2p / prev_p2p) - 1) * 100
                else:
                    delta_pct = None
                st.metric(
                    label="P2P Transactions (Latest)",
                    value=f"{latest_p2p:.1f}M" if pd.notna(latest_p2p) else "N/A",
                    delta=f"{delta_pct:.0f}%" if delta_pct is not None else None
                )
            else:
                st.metric("P2P Transactions (Latest)", "N/A")
        else:
            st.metric("P2P Transactions (Latest)", "N/A")
    
    with col4:
        if not data['historical'].empty:
            events_count = len(data['historical'][data['historical']['record_type'] == 'event'])
            st.metric(
                label="Cataloged Events",
                value=events_count,
                delta=f"+{len(data['impact_matrix'])} with impacts" if not data['impact_matrix'].empty else None
            )
        else:
            st.metric("Cataloged Events", "0")
    
    st.markdown("---")
    
    # P2P vs ATM crossover indicator
    st.markdown('<h3 class="sub-header">🎯 Key Milestone: Digital Transformation</h3>', unsafe_allow_html=True)
    
    if not data['historical'].empty:
        crossover_data = data['historical'][
            (data['historical']['indicator'].str.contains('P2P/ATM', na=False)) |
            (data['historical']['indicator_code'] == 'EVT_CROSSOVER')
        ]
        
        if not crossover_data.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div class="info-box">
                    <strong>Historic Milestone Achieved:</strong> In 2024, P2P digital transactions 
                    surpassed ATM cash withdrawals for the first time in Ethiopia's history. 
                    This marks a significant shift toward digital payments.
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric(
                    label="P2P/ATM Ratio (2024)",
                    value=">1.0",
                    delta="Digital > Cash",
                    delta_color="normal"
                )
    
    # Recent events timeline
    st.markdown('<h3 class="sub-header">📅 Recent Key Events</h3>', unsafe_allow_html=True)
    
    if not data['historical'].empty:
        recent_events = data['historical'][
            (data['historical']['record_type'] == 'event') &
            (data['historical']['observation_date'].notna())
        ].copy()
        
        if not recent_events.empty:
            recent_events['date'] = pd.to_datetime(recent_events['observation_date'], errors='coerce')
            recent_events = recent_events.sort_values('date', ascending=False).head(5)
            
            for _, event in recent_events.iterrows():
                # Safely get notes (handle NaN values)
                notes = event.get('notes', '')
                if pd.isna(notes):
                    notes = 'No description available'
                else:
                    notes = str(notes)[:100] + '...' if len(str(notes)) > 100 else str(notes)
                
                event_date = event['date'].strftime('%b %Y') if pd.notna(event['date']) else 'Date N/A'
                event_name = event.get('indicator', 'Unnamed Event')
                
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{event_date}: {event_name}</strong><br>
                    <small>{notes}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No events data available")

# ==================== SECTION 2: TRENDS & FORECASTS ====================
elif section == "📈 Trends & Forecasts":
    st.markdown('<h2 class="sub-header">📈 Trends & Forecasts Analysis</h2>', unsafe_allow_html=True)
    
    # Tab layout
    tab1, tab2, tab3 = st.tabs(["Account Ownership", "P2P Transactions", "Growth Analysis"])
    
    with tab1:
        st.markdown("#### Account Ownership Trend & Forecast")
        
        # Prepare data
        if not data['historical'].empty:
            historical_acc = data['historical'][
                (data['historical']['indicator_code'] == 'ACC_OWNERSHIP') &
                (data['historical']['record_type'] == 'observation') &
                (data['historical']['gender'] == 'all')
            ].copy()
        else:
            historical_acc = pd.DataFrame()
        
        if not historical_acc.empty and not data['account_forecast'].empty:
            historical_acc['date'] = pd.to_datetime(historical_acc['observation_date'], errors='coerce')
            historical_acc['year'] = historical_acc['date'].dt.year
            historical_acc = historical_acc.dropna(subset=['year', 'value_numeric'])
            
            # Combine historical and forecast
            forecast_acc = data['account_forecast'].copy()
            
            # Create visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical_acc['year'],
                y=historical_acc['value_numeric'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#3B82F6', width=3),
                marker=dict(size=10)
            ))
            
            # Forecast data
            fig.add_trace(go.Scatter(
                x=forecast_acc['year'],
                y=forecast_acc['forecast'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#10B981', width=3, dash='dash'),
                marker=dict(size=10, symbol='diamond')
            ))
            
            # Add target line
            fig.add_hline(
                y=70,
                line_dash="dot",
                line_color="red",
                annotation_text="2025 Target (70%)",
                annotation_position="bottom right"
            )
            
            # Add scenario bands if available
            if not data['scenarios'].empty:
                years_scen = data['scenarios']['year']
                optimistic = data['scenarios']['optimistic']
                pessimistic = data['scenarios']['pessimistic']
                
                fig.add_trace(go.Scatter(
                    x=list(years_scen) + list(years_scen[::-1]),
                    y=list(optimistic) + list(pessimistic[::-1]),
                    fill='toself',
                    fillcolor='rgba(59, 130, 246, 0.2)',
                    line=dict(color='rgba(255, 255, 255, 0)'),
                    name='Scenario Range',
                    showlegend=True
                ))
            
            fig.update_layout(
                title="Account Ownership: Historical Trend & Forecast (2025-2027)",
                xaxis_title="Year",
                yaxis_title="Account Ownership (%)",
                hovermode="x unified",
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast table
            st.markdown("#### Detailed Forecast Table")
            display_df = forecast_acc[['year', 'forecast']].copy()
            if 'events_applied' in forecast_acc.columns:
                display_df['Key Events'] = forecast_acc['events_applied']
            display_df.columns = ['Year', 'Forecast (%)', 'Key Events'] if 'Key Events' in display_df.columns else ['Year', 'Forecast (%)']
            st.dataframe(display_df, use_container_width=True)
        else:
            st.warning("Insufficient data to display account ownership trends")
    
    with tab2:
        st.markdown("#### P2P Transaction Trend & Forecast")
        
        # Prepare data
        if not data['historical'].empty:
            historical_p2p = data['historical'][
                (data['historical']['indicator_code'] == 'USG_P2P_COUNT') &
                (data['historical']['record_type'] == 'observation')
            ].copy()
        else:
            historical_p2p = pd.DataFrame()
        
        if not historical_p2p.empty and not data['p2p_forecast'].empty:
            historical_p2p['date'] = pd.to_datetime(historical_p2p['observation_date'], errors='coerce')
            historical_p2p['year'] = historical_p2p['date'].dt.year
            historical_p2p = historical_p2p.dropna(subset=['year', 'value_numeric'])
            historical_p2p['value_millions'] = historical_p2p['value_numeric'] / 1e6
            
            forecast_p2p = data['p2p_forecast'].copy()
            forecast_p2p['value_millions'] = forecast_p2p['forecast'] / 1e6
            
            # Create visualization
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical_p2p['year'],
                y=historical_p2p['value_millions'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#8B5CF6', width=3),
                marker=dict(size=10)
            ))
            
            # Forecast data
            fig.add_trace(go.Scatter(
                x=forecast_p2p['year'],
                y=forecast_p2p['value_millions'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#F59E0B', width=3, dash='dash'),
                marker=dict(size=10, symbol='diamond')
            ))
            
            fig.update_layout(
                title="P2P Transactions: Historical Trend & Forecast (2025-2027)",
                xaxis_title="Year",
                yaxis_title="Transactions (Millions)",
                hovermode="x unified",
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth metrics
            if len(forecast_p2p) >= 3 and len(historical_p2p) > 0:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    growth_2025 = ((forecast_p2p.iloc[0]['value_millions'] / historical_p2p.iloc[-1]['value_millions']) - 1) * 100
                    st.metric("2025 Growth", f"{growth_2025:.0f}%")
                
                with col2:
                    growth_2026 = ((forecast_p2p.iloc[1]['value_millions'] / forecast_p2p.iloc[0]['value_millions']) - 1) * 100
                    st.metric("2026 Growth", f"{growth_2026:.0f}%")
                
                with col3:
                    cumulative = ((forecast_p2p.iloc[2]['value_millions'] / historical_p2p.iloc[-1]['value_millions']) - 1) * 100
                    st.metric("3-Year Growth", f"{cumulative:.0f}%")
        else:
            st.warning("Insufficient data to display P2P transaction trends")
    
    with tab3:
        st.markdown("#### Growth Rate Analysis")
        
        # Calculate growth rates
        growth_data = []
        
        # Account ownership growth
        if not data['historical'].empty:
            acc_series = data['historical'][
                (data['historical']['indicator_code'] == 'ACC_OWNERSHIP') &
                (data['historical']['gender'] == 'all') &
                (data['historical']['record_type'] == 'observation')
            ].sort_values('observation_date')
        else:
            acc_series = pd.DataFrame()
        
        if len(acc_series) > 1:
            for i in range(1, len(acc_series)):
                year1 = pd.to_datetime(acc_series.iloc[i-1]['observation_date']).year
                year2 = pd.to_datetime(acc_series.iloc[i]['observation_date']).year
                growth = acc_series.iloc[i]['value_numeric'] - acc_series.iloc[i-1]['value_numeric']
                growth_data.append({
                    'Period': f'{year1}-{year2}',
                    'Indicator': 'Account Ownership',
                    'Growth_pp': growth,
                    'Annual_pp': growth / (year2 - year1)
                })
        
        # Add forecast growth
        if not data['account_forecast'].empty:
            last_historical = acc_series.iloc[-1]['value_numeric'] if not acc_series.empty else 0
            for i, row in data['account_forecast'].iterrows():
                if i == 0:
                    growth = row['forecast'] - last_historical
                else:
                    growth = row['forecast'] - data['account_forecast'].iloc[i-1]['forecast']
                
                growth_data.append({
                    'Period': f'Forecast {row["year"]}',
                    'Indicator': 'Account Ownership',
                    'Growth_pp': growth,
                    'Annual_pp': growth
                })
        
        if growth_data:
            growth_df = pd.DataFrame(growth_data)
            
            # Create bar chart
            fig = px.bar(
                growth_df,
                x='Period',
                y='Growth_pp',
                color='Growth_pp',
                color_continuous_scale=['red', 'yellow', 'green'],
                title='Account Ownership Growth by Period (Percentage Points)',
                labels={'Growth_pp': 'Growth (pp)', 'Period': 'Time Period'}
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth insights
            avg_growth = growth_df['Growth_pp'].mean()
            max_growth = growth_df['Growth_pp'].max()
            min_growth = growth_df['Growth_pp'].min()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Growth", f"{avg_growth:.1f}pp")
            col2.metric("Maximum Growth", f"{max_growth:.1f}pp")
            col3.metric("Minimum Growth", f"{min_growth:.1f}pp")
        else:
            st.info("Insufficient data for growth analysis")

# ==================== SECTION 3: INCLUSION PROJECTIONS ====================
elif section == "🎯 Inclusion Projections":
    st.markdown('<h2 class="sub-header">🎯 Financial Inclusion Projections</h2>', unsafe_allow_html=True)
    
    # Scenario selector
    scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
    
    with scenario_col1:
        st.markdown("#### Target Progress")
        current_acc = 49  # 2024 value (default)
        if not data['historical'].empty:
            acc_data = data['historical'][
                (data['historical']['indicator_code'] == 'ACC_OWNERSHIP') &
                (data['historical']['record_type'] == 'observation')
            ]
            if not acc_data.empty:
                current_acc = acc_data.iloc[-1]['value_numeric']
        
        target_2025 = 70
        
        progress = (current_acc / target_2025) * 100
        st.progress(int(progress) / 100)
        st.metric("Progress to 2025 Target", f"{progress:.1f}%", f"{target_2025 - current_acc:.1f}pp remaining")
    
    with scenario_col2:
        st.markdown("#### Scenario Projections")
        scenario = st.selectbox(
            "Select Forecast Scenario",
            ["Baseline", "Optimistic", "Pessimistic"],
            key="scenario_select"
        )
    
    with scenario_col3:
        st.markdown("#### Forecast Horizon")
        horizon = st.slider("Years to Forecast", 1, 5, 3, key="horizon_slider")
    
    # Projection visualization
    st.markdown("#### Inclusion Projection Timeline")
    
    # Create projection data based on selected scenario
    if not data['account_forecast'].empty and not data['scenarios'].empty:
        baseline = data['account_forecast']['forecast'].values
        
        if scenario == "Optimistic":
            projections = data['scenarios']['optimistic'].values
        elif scenario == "Pessimistic":
            projections = data['scenarios']['pessimistic'].values
        else:
            projections = baseline
        
        years = data['account_forecast']['year'].values
        
        # Create projection chart
        fig = go.Figure()
        
        # Historical data
        if not data['historical'].empty:
            historical_acc = data['historical'][
                (data['historical']['indicator_code'] == 'ACC_OWNERSHIP') &
                (data['historical']['record_type'] == 'observation') &
                (data['historical']['gender'] == 'all')
            ].copy()
            
            if not historical_acc.empty:
                historical_acc['date'] = pd.to_datetime(historical_acc['observation_date'], errors='coerce')
                historical_acc['year'] = historical_acc['date'].dt.year
                historical_acc = historical_acc.dropna(subset=['year', 'value_numeric'])
                
                fig.add_trace(go.Scatter(
                    x=historical_acc['year'],
                    y=historical_acc['value_numeric'],
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='#6B7280', width=2)
                ))
        
        # Projections
        fig.add_trace(go.Scatter(
            x=years,
            y=projections,
            mode='lines+markers',
            name=f'{scenario} Scenario',
            line=dict(color='#3B82F6', width=3)
        ))
        
        # Target line
        fig.add_hline(
            y=70,
            line_dash="dot",
            line_color="red",
            annotation_text="NFIS-II 2025 Target",
            annotation_position="bottom right"
        )
        
        # 50% inclusion milestone
        fig.add_hline(
            y=50,
            line_dash="dot",
            line_color="orange",
            annotation_text="Half of Adults",
            annotation_position="bottom right"
        )
        
        fig.update_layout(
            title=f"Financial Inclusion Projection: {scenario} Scenario",
            xaxis_title="Year",
            yaxis_title="Account Ownership (%)",
            hovermode="x unified",
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Projection table
        st.markdown("#### Detailed Projections")
        proj_df = pd.DataFrame({
            'Year': years,
            f'{scenario}_Projection': projections,
            'Gap_to_Target': 70 - projections,
        })
        
        st.dataframe(proj_df, use_container_width=True)
        
        # Key milestones
        st.markdown("#### Key Milestones")
        
        milestones = []
        for year, proj in zip(years, projections):
            if proj >= 50 and 50 not in [m[1] for m in milestones]:
                milestones.append((year, 50, "Half of adults with accounts"))
            if proj >= 60 and 60 not in [m[1] for m in milestones]:
                milestones.append((year, 60, "Majority inclusion milestone"))
            if proj >= 70 and 70 not in [m[1] for m in milestones]:
                milestones.append((year, 70, "NFIS-II target achieved"))
        
        if milestones:
            for milestone in milestones:
                st.info(f"**{milestone[0]}**: Reach {milestone[1]}% ({milestone[2]})")
        else:
            st.info("No major milestones reached in forecast period")
    else:
        st.warning("Insufficient data for inclusion projections")

# ==================== SECTION 4: EVENT IMPACTS ====================
elif section == "⚡ Event Impacts":
    st.markdown('<h2 class="sub-header">⚡ Event Impact Analysis</h2>', unsafe_allow_html=True)
    
    # Event impact matrix
    st.markdown("#### Event-Impact Association Matrix")
    
    if not data['impact_matrix'].empty:
        # Filter matrix for display
        display_matrix = data['impact_matrix'].copy()
        
        # Select key indicators
        key_indicators = ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_P2P_COUNT', 'USG_P2P_VALUE']
        available_indicators = [ind for ind in key_indicators if ind in display_matrix.columns]
        
        if available_indicators:
            # Add event date and category for context
            if 'event_date' in display_matrix.columns:
                display_matrix = display_matrix[['event_date', 'category'] + available_indicators]
            else:
                display_matrix = display_matrix[available_indicators]
            
            st.dataframe(display_matrix, use_container_width=True)
        else:
            st.info("No impact matrix data available")
    else:
        st.info("No impact matrix data available")
    
    # Event timeline visualization
    st.markdown("#### Event Timeline")
    
    if not data['historical'].empty:
        events = data['historical'][data['historical']['record_type'] == 'event'].copy()
        if not events.empty:
            events['date'] = pd.to_datetime(events['observation_date'], errors='coerce')
            events = events.dropna(subset=['date'])
            events = events.sort_values('date')
            
            # Create timeline
            fig = go.Figure()
            
            for _, event in events.iterrows():
                fig.add_trace(go.Scatter(
                    x=[event['date']],
                    y=[1],  # Placeholder y-value
                    mode='markers+text',
                    name=event.get('indicator', 'Event'),
                    marker=dict(size=15),
                    text=[event.get('indicator', 'Event')[:20]],
                    textposition="top center",
                    hovertext=event.get('notes', 'No description'),
                    hoverinfo="text"
                ))
            
            fig.update_layout(
                title="Key Events Timeline",
                xaxis_title="Date",
                showlegend=False,
                height=300,
                yaxis=dict(showticklabels=False, range=[0.5, 1.5]),
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No events data available")
    else:
        st.info("No historical data available")

# ==================== SECTION 5: DATA EXPLORER ====================
elif section == "📋 Data Explorer":
    st.markdown('<h2 class="sub-header">📋 Data Explorer</h2>', unsafe_allow_html=True)
    
    # Data selection
    dataset_options = ["Historical Observations", "Forecasts", "Events", "All Data"]
    if not data['enriched'].empty:
        dataset_options.append("Enriched Data")
    
    dataset = st.selectbox("Select Dataset", dataset_options)
    
    # Prepare data based on selection
    if dataset == "Historical Observations":
        display_data = data['historical'][data['historical']['record_type'] == 'observation'].copy()
    elif dataset == "Forecasts":
        if not data['account_forecast'].empty and not data['p2p_forecast'].empty:
            display_data = pd.concat([
                data['account_forecast'].assign(type='Account Forecast'),
                data['p2p_forecast'].assign(type='P2P Forecast')
            ], ignore_index=True)
        else:
            display_data = pd.DataFrame()
    elif dataset == "Events":
        display_data = data['historical'][data['historical']['record_type'] == 'event'].copy()
    elif dataset == "Enriched Data":
        display_data = data['enriched'].copy()
    else:
        display_data = data['historical'].copy()
    
    if not display_data.empty:
        # Display data
        st.markdown(f"#### {dataset} ({len(display_data)} records)")
        st.dataframe(display_data, use_container_width=True)
        
        # Download option
        csv = display_data.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"ethiopia_fi_{dataset.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
        
        # Data summary
        st.markdown("#### Data Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(display_data))
        
        with col2:
            if 'observation_date' in display_data.columns:
                display_data['year'] = pd.to_datetime(display_data['observation_date'], errors='coerce').dt.year
                years_range = f"{int(display_data['year'].min())}-{int(display_data['year'].max())}"
                st.metric("Year Range", years_range)
            else:
                st.metric("Year Range", "N/A")
        
        with col3:
            if 'indicator' in display_data.columns:
                unique_indicators = display_data['indicator'].nunique()
                st.metric("Unique Indicators", unique_indicators)
            else:
                st.metric("Unique Indicators", "N/A")
    else:
        st.warning("No data available for selected dataset")

# ==================== SECTION 6: ABOUT ====================
else:  # About section
    st.markdown('<h2 class="sub-header">ℹ️ About This Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Project Overview
        
        This dashboard is part of the **Ethiopia Financial Inclusion Forecasting** project,
        developed for Selam Analytics to track Ethiopia's digital financial transformation.
        
        ### Key Objectives:
        1. **Forecast** Account Ownership and Digital Payment Usage for 2025-2027
        2. **Analyze** the impact of events (product launches, policies, infrastructure)
        3. **Provide** actionable insights for stakeholders
        4. **Monitor** progress toward NFIS-II targets
        
        ### Data Sources:
        - Global Findex Database (World Bank)
        - National Bank of Ethiopia reports
        - Mobile money operator reports (Telebirr, M-Pesa)
        - Infrastructure data (GSMA, ITU)
        - Policy announcements and market developments
        
        ### Methodology:
        - Time series analysis with event impacts
        - Comparable country evidence
        - Scenario-based forecasting
        - Regression modeling with intervention variables
        """)
    
    with col2:
        st.markdown("""
        ### Technical Details
        
        **Version:** 1.0.0
        
        **Last Updated:** February 2026
        
        **Built With:**
        - Python 3.9
        - Streamlit (Dashboard)
        - Plotly (Visualizations)
        - Pandas (Data Analysis)
        - Scikit-learn (Modeling)
        
        **Data Status:**
        """)
        
        # Data status indicators
        data_status = {
            "Historical Data": not data['historical'].empty,
            "Forecast Data": not data['account_forecast'].empty,
            "Event Impacts": not data['impact_matrix'].empty,
            "Scenarios": not data['scenarios'].empty
        }
        
        for name, status in data_status.items():
            if status:
                st.success(f"✓ {name}")
            else:
                st.warning(f"⚠ {name}")
        
        st.markdown("---")
        st.info("**Note:** Demo data is used when real data files are not found.")

    st.markdown("---")
    st.caption("""
    Developed for the Ethiopia Financial Inclusion Forecasting Challenge | 
    Selam Analytics | Data Science Team | February 2026
    """)

# Footer
st.markdown("---")
st.caption("📊 Ethiopia Financial Inclusion Dashboard v1.0 | Data last updated: February 2026")