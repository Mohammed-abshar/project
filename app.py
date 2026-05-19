import streamlit as st
import sys

# Guard to launch Streamlit immediately if run directly as a standard Python script
if not st.runtime.exists():
    import subprocess
    print("Launching Streamlit dashboard from app.py...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])
    sys.exit(0)

# --- The rest of the dashboard application runs only inside the Streamlit context ---
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

# Set page configuration for a premium look
st.set_page_config(
    page_title="Cloud Cost Intelligence",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, premium aesthetics
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #00F0FF;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
        color: #A0AEC0;
    }
    div[data-testid="metric-container"] {
        background-color: #1A202C;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #2D3748;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #171923;
        border-right: 1px solid #2D3748;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("healthcare_cloud_billing.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Could not find 'healthcare_cloud_billing.csv'. Please ensure the dataset is generated.")
    st.stop()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3256/3256013.png", width=80)
    st.title("Filters & Controls")
    
    # Date Range
    min_date = df['Date'].min().date()
    max_date = df['Date'].min().date() if pd.isna(df['Date'].max()) else df['Date'].max().date()
    date_range = st.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    # Selection Filters
    hospitals = st.multiselect("🏥 Hospitals", options=df['Hospital Name'].unique(), default=df['Hospital Name'].unique())
    vendors = st.multiselect("☁️ Cloud Providers", options=df['Vendor Name'].unique(), default=df['Vendor Name'].unique())
    services = st.multiselect("🛠️ Services", options=df['Service Type'].unique(), default=df['Service Type'].unique())

# Filter the data
filtered_df = df[
    (df['Hospital Name'].isin(hospitals)) &
    (df['Vendor Name'].isin(vendors)) &
    (df['Service Type'].isin(services))
]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['Date'].dt.date >= start_date) & (filtered_df['Date'].dt.date <= end_date)]

# --- MAIN DASHBOARD ---
st.title("☁️ Cloud Cost Intelligence Platform")
st.markdown("Advanced analytics, AI predictions, and cost optimization for healthcare cloud infrastructure.")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🤖 AI & Predictive Analytics", "💡 Optimization Recommendations"])

chart_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#A0AEC0'),
    margin=dict(l=20, r=20, t=50, b=20)
)

with tab1:
    # KPI Metrics
    total_cost = filtered_df['Monthly Cost'].sum()
    avg_cpu = filtered_df['CPU Usage %'].mean()
    avg_mem = filtered_df['Memory Usage %'].mean()
    total_storage = filtered_df['Storage Used (GB)'].sum() / 1000  # in TB
    
    # Advanced KPIs
    if not filtered_df.empty:
        total_monthly_cost = filtered_df[filtered_df['Date'].dt.month == filtered_df['Date'].max().month]['Monthly Cost'].sum()
        top_expensive_dept = filtered_df.groupby('Department Name')['Monthly Cost'].sum().idxmax()
        top_expensive_service = filtered_df.groupby('Service Type')['Monthly Cost'].sum().idxmax()
        pending_payments = filtered_df[filtered_df['Payment Status'] == 'Pending']['Monthly Cost'].sum()
    else:
        total_monthly_cost = 0
        top_expensive_dept = "N/A"
        top_expensive_service = "N/A"
        pending_payments = 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cloud Spend (YTD)", f"${total_cost:,.2f}")
    with col2:
        st.metric("Total Storage (TB)", f"{total_storage:,.2f} TB")
    with col3:
        st.metric("Avg CPU Usage", f"{avg_cpu:.1f}%")
    with col4:
        st.metric("Avg Memory Usage", f"{avg_mem:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Recent Month Cost", f"${total_monthly_cost:,.2f}")
    with col6:
        st.metric("Pending Payments", f"${pending_payments:,.2f}")
    with col7:
        st.metric("Top Dept", top_expensive_dept)
    with col8:
        st.metric("Top Service", top_expensive_service)

    st.markdown("<br>", unsafe_allow_html=True)

    # Monthly Trend
    monthly_trend = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Monthly Cost'].sum().reset_index()
    monthly_trend['Date'] = monthly_trend['Date'].dt.to_timestamp()
    
    fig_trend = px.line(
        monthly_trend, x='Date', y='Monthly Cost', markers=True,
        title="Monthly Cloud Cost Trend", line_shape='spline'
    )
    fig_trend.update_traces(line_color='#00ff99', line_width=3, marker=dict(size=8, color='white'))
    fig_trend.update_layout(**chart_layout)
    fig_trend.update_xaxes(showgrid=False)
    fig_trend.update_yaxes(showgrid=True, gridcolor='#2D3748')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")

    # Cost by Vendor (Donut Chart)
    vendor_cost = filtered_df.groupby('Vendor Name')['Monthly Cost'].sum().reset_index()
    fig_vendor = px.pie(
        vendor_cost, values='Monthly Cost', names='Vendor Name',
        title="Cloud Provider Market Share",
        hole=0.5,
        color_discrete_sequence=['#ff9900', '#0078d4', '#ea4335']
    )
    fig_vendor.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0E1117', width=2)))
    fig_vendor.update_layout(**chart_layout, showlegend=False)
    st.plotly_chart(fig_vendor, use_container_width=True)

    st.markdown("---")

    # Cost by Service Type (Donut Chart)
    service_cost = filtered_df.groupby('Service Type')['Monthly Cost'].sum().reset_index()
    fig_service = px.pie(
        service_cost, values='Monthly Cost', names='Service Type',
        title="Cloud Service Cost Distribution",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig_service.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0E1117', width=2)))
    fig_service.update_layout(**chart_layout, showlegend=False)
    st.plotly_chart(fig_service, use_container_width=True)

    st.markdown("---")

    # Cumulative Yearly Growth (Area Chart)
    df_sorted = filtered_df.sort_values('Date')
    monthly_sum = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))['Monthly Cost'].sum().reset_index()
    monthly_sum['Cumulative Cost'] = monthly_sum['Monthly Cost'].cumsum()
    monthly_sum['Date'] = monthly_sum['Date'].dt.to_timestamp()
    fig_cum = px.area(
        monthly_sum, x='Date', y='Cumulative Cost', 
        title="Cumulative Cloud Cost Growth over Time",
        color_discrete_sequence=['#ff4b4b']
    )
    fig_cum.update_layout(**chart_layout)
    fig_cum.update_xaxes(showgrid=False)
    fig_cum.update_yaxes(showgrid=True, gridcolor='#2D3748')
    st.plotly_chart(fig_cum, use_container_width=True)
    
    st.markdown("---")

    # Department Cost Comparison (Bar Chart)
    dept_costs = filtered_df.groupby('Department Name')['Monthly Cost'].sum().sort_values(ascending=False).reset_index()
    fig_dept = px.bar(
        dept_costs, x='Monthly Cost', y='Department Name', orientation='h',
        title="Total Cloud Cost by Department",
        color='Monthly Cost',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_dept.update_layout(**chart_layout, coloraxis_showscale=False)
    fig_dept.update_xaxes(showgrid=True, gridcolor='#2D3748')
    fig_dept.update_yaxes(showgrid=False)
    st.plotly_chart(fig_dept, use_container_width=True)

    st.markdown("---")

    # Department vs Vendor Cost Heatmap
    heatmap_data = filtered_df.pivot_table(index='Department Name', columns='Vendor Name', values='Monthly Cost', aggfunc='sum').fillna(0)
    fig_heat = px.imshow(
        heatmap_data, 
        text_auto=".0f", 
        aspect="auto",
        title="Cost Heatmap: Department vs Vendor",
        color_continuous_scale="Inferno"
    )
    fig_heat.update_layout(**chart_layout)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")

    # Cost Frequency Distribution (Histogram)
    fig_hist = px.histogram(
        filtered_df, x="Monthly Cost", nbins=30,
        title="Distribution of Monthly Billing Amounts",
        color_discrete_sequence=['cyan']
    )
    fig_hist.update_layout(**chart_layout)
    fig_hist.update_xaxes(showgrid=True, gridcolor='#2D3748')
    fig_hist.update_yaxes(showgrid=True, gridcolor='#2D3748')
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # CPU Usage vs Cost Scatter
    fig_cpu_scatter = px.scatter(
        filtered_df, x='CPU Usage %', y='Monthly Cost', color='Service Type',
        size='Usage Hours', hover_data=['Department Name'],
        title="CPU Usage vs Monthly Cost (Sized by Usage Hours)"
    )
    fig_cpu_scatter.update_layout(**chart_layout)
    fig_cpu_scatter.update_xaxes(showgrid=True, gridcolor='#2D3748')
    fig_cpu_scatter.update_yaxes(showgrid=True, gridcolor='#2D3748')
    st.plotly_chart(fig_cpu_scatter, use_container_width=True)

    st.markdown("---")

    # Outlier Detection Box Plot
    fig_box = px.box(
        filtered_df, x='Service Type', y='Monthly Cost', color='Service Type',
        title="Outlier Detection in Service Costs",
        color_discrete_sequence=px.colors.sequential.Magma
    )
    fig_box.update_layout(**chart_layout, showlegend=False)
    fig_box.update_xaxes(showgrid=False)
    fig_box.update_yaxes(showgrid=True, gridcolor='#2D3748')
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # Data Table
    st.markdown("### 📋 Detailed Billing Records")
    st.dataframe(
        filtered_df[['Billing ID', 'Date', 'Hospital Name', 'Service Type', 'Vendor Name', 'Monthly Cost', 'Payment Status']].sort_values('Date', ascending=False).head(100),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.markdown("### 🤖 Machine Learning Cost Analysis")
    
    st.markdown("#### Cost Prediction (Next 30 Days)")
    if not filtered_df.empty:
        ml_df = filtered_df.groupby('Date')['Monthly Cost'].sum().reset_index()
        ml_df['Day_Index'] = (ml_df['Date'] - ml_df['Date'].min()).dt.days

        X = ml_df[['Day_Index']]
        y = ml_df['Monthly Cost']
        
        if len(X) > 1:
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict next 30 days
            max_day = X['Day_Index'].max()
            future_days = np.array([[max_day + i] for i in range(1, 31)])
            future_preds = model.predict(future_days)
            predicted_next_month_cost = future_preds.sum()
            
            st.metric("Predicted Cloud Cost (Next 30 Days)", f"${predicted_next_month_cost:,.2f}")
            
            # Plot Regression Line
            fig_reg = go.Figure()
            fig_reg.add_trace(go.Scatter(x=ml_df['Date'], y=y, mode='markers', name='Actual Costs', marker=dict(color='#00F0FF', opacity=0.6)))
            
            # Create future dates
            future_dates = [ml_df['Date'].max() + pd.Timedelta(days=i) for i in range(1, 31)]
            all_dates = pd.concat([ml_df['Date'], pd.Series(future_dates)])
            all_days = np.array([[day] for day in range(max_day + 31)])
            all_preds = model.predict(all_days)
            
            fig_reg.add_trace(go.Scatter(x=all_dates, y=all_preds, mode='lines', name='Trend / Forecast', line=dict(color='#FF0055', width=3)))
            fig_reg.update_layout(title='Cost Trend Analysis & ML Prediction', **chart_layout)
            fig_reg.update_xaxes(showgrid=False)
            fig_reg.update_yaxes(showgrid=True, gridcolor='#2D3748')
            st.plotly_chart(fig_reg, use_container_width=True)
        else:
            st.warning("Not enough data to train prediction model. Please expand filters.")
    else:
        st.warning("No data available.")

    st.markdown("---")

    st.markdown("#### Anomaly Detection")
    if not filtered_df.empty and len(filtered_df) > 10:
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        filtered_df['Anomaly'] = iso_forest.fit_predict(filtered_df[['Monthly Cost', 'Usage Hours']])
        
        anomalies = filtered_df[filtered_df['Anomaly'] == -1]
        st.metric("Detected Anomalies", f"{len(anomalies)} Records")
        
        fig_anomaly = px.scatter(
            filtered_df, x='Usage Hours', y='Monthly Cost', color=filtered_df['Anomaly'].astype(str),
            hover_name='Hospital Name', hover_data=['Service Type', 'Vendor Name'],
            title='Anomaly Detection (Red = Outliers)',
            color_discrete_map={'-1': '#FF0055', '1': '#00F0FF'}
        )
        fig_anomaly.update_layout(**chart_layout)
        fig_anomaly.update_xaxes(showgrid=True, gridcolor='#2D3748')
        fig_anomaly.update_yaxes(showgrid=True, gridcolor='#2D3748')
        st.plotly_chart(fig_anomaly, use_container_width=True)
        
        if not anomalies.empty:
            with st.expander("View Anomalous Records"):
                st.dataframe(anomalies[['Billing ID', 'Hospital Name', 'Service Type', 'Monthly Cost', 'Usage Hours']].sort_values('Monthly Cost', ascending=False), hide_index=True)
    else:
        st.warning("Not enough data for anomaly detection. Minimum 10 records required.")

with tab3:
    st.markdown("### 💡 Cost Optimization Actions")
    if not filtered_df.empty:
        pending_payments = filtered_df[filtered_df['Payment Status'] == 'Pending']['Monthly Cost'].sum()
        total_cost_filtered = filtered_df['Monthly Cost'].sum()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            st.info(f"**Unpaid Bills Alert**\n\nTotal Pending Payments: **${pending_payments:,.2f}**")
            if pending_payments > total_cost_filtered * 0.1:
                st.warning("⚠️ High pending payments detected (>10% of total). Recommend automating invoice collection workflows.")
        
        with col_rec2:
            top_expensive_dept = filtered_df.groupby('Department Name')['Monthly Cost'].sum().idxmax()
            top_dept_cost = filtered_df.groupby('Department Name')['Monthly Cost'].sum().max()
            
            st.info(f"**Top Spending Department: {top_expensive_dept}**\n\nTotal Department Cost: **${top_dept_cost:,.2f}**")
            if top_dept_cost > total_cost_filtered * 0.2:
                st.warning(f"📉 {top_expensive_dept} consumes >20% of your filtered budget. Audit their usage for immediate savings.")
        
        st.markdown("---")
        st.markdown("#### Underutilized Resources")
        unused_resources = filtered_df[(filtered_df['Usage Hours'] < 50) & (filtered_df['Monthly Cost'] > 500)]
        if not unused_resources.empty:
            st.error(f"🛑 Found {len(unused_resources)} resources with very low usage (<50 hours) but high cost (>$500). Consider downsizing or shutting them down immediately.")
            st.dataframe(unused_resources[['Billing ID', 'Hospital Name', 'Department Name', 'Service Type', 'Monthly Cost', 'Usage Hours']], hide_index=True)
        else:
            st.success("✅ No significantly underutilized resources detected in the current filter context.")
    else:
        st.warning("No data available.")
