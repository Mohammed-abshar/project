import json

def create_notebook():
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    def add_markdown(text):
        notebook['cells'].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": text.splitlines(True)
        })

    def add_code(text):
        notebook['cells'].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + '\n' for line in text.split('\n')]
        })

    # Introduction
    add_markdown("""# 🏥 Cloud Cost Intelligence Platform for Healthcare
### Artificial Intelligence, Cloud Computing and DevOps-B (Final Year Project)

**Main Objective:** Develop a smart Healthcare Cloud Billing Analysis System that helps hospitals and healthcare organizations track, analyze, optimize, and predict cloud service costs.

This interactive notebook includes:
- **Data Preprocessing**: Cleaning and preparing billing data.
- **KPI Dashboard**: Advanced metrics for cloud cost management.
- **Professional Data Visualizations**: 10 distinct, interactive, and statically styled charts.
- **AI/Machine Learning**: Predictive cost modeling (Linear Regression) and Outlier/Anomaly Detection.
- **Exporting**: Excel reporting & PDF logic.
""")

    # 1. Imports
    add_markdown("## 1. Import Required Libraries")
    add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.metrics import mean_squared_error, r2_score
import warnings
import ipywidgets as widgets
from IPython.display import display, HTML

warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#1e1e1e", "figure.facecolor": "#121212", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white"})

print("✅ All libraries loaded successfully.")
""")

    # 2. Login Page
    add_markdown("## 2. Interactive Login & App Initialization")
    add_code("""# Simple Login Widget
def authenticate(btn):
    if username.value == "admin" and password.value == "healthcare123":
        login_output.clear_output()
        with login_output:
            display(HTML("<h3 style='color: limegreen;'>✅ Login Successful! Welcome to Healthcare Cloud Analytics.</h3>"))
    else:
        with login_output:
            display(HTML("<h4 style='color: red;'>❌ Invalid Credentials. Try again.</h4>"))

username = widgets.Text(description="Username:")
password = widgets.Password(description="Password:")
login_btn = widgets.Button(description="Login", button_style='success')
login_btn.on_click(authenticate)

login_output = widgets.Output()

display(HTML("<h3>🔐 System Authentication</h3>"))
display(username, password, login_btn, login_output)
""")

    # 3. Load Data
    add_markdown("## 3. Data Loading & Preprocessing")
    add_code("""# Load the dataset
try:
    df = pd.read_csv('healthcare_cloud_billing.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    print(f"✅ Data loaded successfully. Shape: {df.shape}")
except Exception as e:
    print(f"❌ Error loading data: {e}")

# Display first few rows
display(df.head())
""")

    # 4. KPI Dashboard
    add_markdown("## 4. Executive KPI Dashboard")
    add_code("""# Calculate KPIs
total_monthly_cost = df[df['Date'].dt.month == df['Date'].max().month]['Monthly Cost'].sum()
total_annual_cost = df['Monthly Cost'].sum()
top_expensive_dept = df.groupby('Department Name')['Monthly Cost'].sum().idxmax()
top_expensive_service = df.groupby('Service Type')['Monthly Cost'].sum().idxmax()
pending_payments = df[df['Payment Status'] == 'Pending']['Monthly Cost'].sum()

# Display KPIs using HTML/CSS Cards
kpi_html = f\"\"\"
<div style='display:flex; justify-content:space-around; flex-wrap:wrap; text-align:center;'>
    <div style='background-color:#2b2b2b; padding:20px; border-radius:10px; margin:10px; width:18%; border-left: 5px solid #00c3ff;'>
        <h4 style='color:#ccc; margin:0;'>Total Cost (YTD)</h4>
        <h2 style='color:#00c3ff; margin:10px 0;'>${total_annual_cost:,.2f}</h2>
    </div>
    <div style='background-color:#2b2b2b; padding:20px; border-radius:10px; margin:10px; width:18%; border-left: 5px solid #ff4b4b;'>
        <h4 style='color:#ccc; margin:0;'>Recent Month Cost</h4>
        <h2 style='color:#ff4b4b; margin:10px 0;'>${total_monthly_cost:,.2f}</h2>
    </div>
    <div style='background-color:#2b2b2b; padding:20px; border-radius:10px; margin:10px; width:18%; border-left: 5px solid #ffcc00;'>
        <h4 style='color:#ccc; margin:0;'>Pending Payments</h4>
        <h2 style='color:#ffcc00; margin:10px 0;'>${pending_payments:,.2f}</h2>
    </div>
    <div style='background-color:#2b2b2b; padding:20px; border-radius:10px; margin:10px; width:18%; border-left: 5px solid #00ff99;'>
        <h4 style='color:#ccc; margin:0;'>Top Dept</h4>
        <h3 style='color:#00ff99; margin:10px 0;'>{top_expensive_dept}</h3>
    </div>
    <div style='background-color:#2b2b2b; padding:20px; border-radius:10px; margin:10px; width:18%; border-left: 5px solid #cc00ff;'>
        <h4 style='color:#ccc; margin:0;'>Top Service</h4>
        <h3 style='color:#cc00ff; margin:10px 0;'>{top_expensive_service}</h3>
    </div>
</div>
\"\"\"
display(HTML(kpi_html))
""")

    # 5. Charts
    add_markdown("## 5. Advanced Data Visualizations\n### 5.1 Service Cost Distribution (Pie Chart)")
    add_code("""service_costs = df.groupby('Service Type')['Monthly Cost'].sum().reset_index()
fig1 = px.pie(service_costs, values='Monthly Cost', names='Service Type', hole=0.3,
             title='Cloud Service Cost Distribution', color_discrete_sequence=px.colors.sequential.Plasma)
fig1.update_layout(template='plotly_dark')
fig1.show()
""")

    add_markdown("### 5.2 Department Cost Comparison (Bar Chart)")
    add_code("""dept_costs = df.groupby('Department Name')['Monthly Cost'].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='Monthly Cost', y='Department Name', data=dept_costs, palette='viridis')
plt.title('Total Cloud Cost by Department', fontsize=16, color='white')
plt.xlabel('Total Cost ($)', color='white')
plt.ylabel('Department', color='white')
plt.show()
""")

    add_markdown("### 5.3 Monthly Cost Trend (Line Chart)")
    add_code("""monthly_trend = df.groupby('Month')['Monthly Cost'].sum().reset_index()
fig3 = px.line(monthly_trend, x='Month', y='Monthly Cost', markers=True, 
               title='Monthly Cloud Cost Trend', line_shape='spline')
fig3.update_traces(line_color='#00ff99', line_width=3, marker=dict(size=8, color='white'))
fig3.update_layout(template='plotly_dark', xaxis_title='Month', yaxis_title='Cost ($)')
fig3.show()
""")

    add_markdown("### 5.4 Vendor Share (Donut Chart)")
    add_code("""vendor_share = df.groupby('Vendor Name')['Monthly Cost'].sum().reset_index()
fig4 = px.pie(vendor_share, values='Monthly Cost', names='Vendor Name', hole=0.5,
              title='Cloud Provider Market Share', color_discrete_sequence=['#ff9900', '#0078d4', '#ea4335'])
fig4.update_layout(template='plotly_dark')
fig4.show()
""")

    add_markdown("### 5.5 Department vs Cost (Heatmap)")
    add_code("""heatmap_data = df.pivot_table(index='Department Name', columns='Vendor Name', values='Monthly Cost', aggfunc='sum').fillna(0)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="inferno", linewidths=.5)
plt.title('Cost Heatmap: Department vs Vendor', color='white', fontsize=14)
plt.show()
""")

    add_markdown("### 5.6 Cost Frequency Distribution (Histogram)")
    add_code("""plt.figure(figsize=(10, 5))
sns.histplot(df['Monthly Cost'], bins=30, kde=True, color='cyan')
plt.title('Distribution of Monthly Billing Amounts', color='white')
plt.xlabel('Cost ($)')
plt.show()
""")

    add_markdown("### 5.7 CPU Usage vs Cost (Scatter Plot)")
    add_code("""fig7 = px.scatter(df, x='CPU Usage %', y='Monthly Cost', color='Service Type',
                    size='Usage Hours', hover_data=['Department Name'],
                    title='CPU Usage vs Monthly Cost (Sized by Usage Hours)')
fig7.update_layout(template='plotly_dark')
fig7.show()
""")

    add_markdown("### 5.8 Outlier Detection (Box Plot)")
    add_code("""plt.figure(figsize=(12, 6))
sns.boxplot(x='Service Type', y='Monthly Cost', data=df, palette='magma')
plt.title('Outlier Detection in Service Costs', color='white')
plt.xticks(rotation=45)
plt.show()
""")

    add_markdown("### 5.9 Region Wise Cost (Treemap)")
    add_code("""region_cost = df.groupby(['Region', 'Vendor Name'])['Monthly Cost'].sum().reset_index()
fig9 = px.treemap(region_cost, path=['Region', 'Vendor Name'], values='Monthly Cost',
                  title='Cost Distribution by Region and Vendor', color='Monthly Cost',
                  color_continuous_scale='RdBu')
fig9.update_layout(template='plotly_dark')
fig9.show()
""")

    add_markdown("### 5.10 Cumulative Yearly Growth (Area Chart)")
    add_code("""df_sorted = df.sort_values('Date')
monthly_sum = df_sorted.groupby('Month')['Monthly Cost'].sum().reset_index()
monthly_sum['Cumulative Cost'] = monthly_sum['Monthly Cost'].cumsum()

fig10 = px.area(monthly_sum, x='Month', y='Cumulative Cost', title='Cumulative Cloud Cost Growth over Time',
                color_discrete_sequence=['#ff4b4b'])
fig10.update_layout(template='plotly_dark')
fig10.show()
""")

    # 6. AI Features
    add_markdown("## 6. AI & Smart Features\n### 6.1 Predicting Next Month Cost (Linear Regression)")
    add_code("""# Preparing data for ML
ml_df = df.groupby('Date')['Monthly Cost'].sum().reset_index()
ml_df['Day_Index'] = (ml_df['Date'] - ml_df['Date'].min()).dt.days

X = ml_df[['Day_Index']]
y = ml_df['Monthly Cost']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"🤖 Model Performance: MSE = {mse:.2f}, R2 Score = {r2:.2f}")

# Predict next 30 days
future_days = np.array([[X['Day_Index'].max() + i] for i in range(1, 31)])
future_preds = model.predict(future_days)
predicted_next_month_cost = future_preds.sum()

display(HTML(f"<h4>🔮 Predicted Cloud Cost for Next 30 Days: <span style='color:lime'>${predicted_next_month_cost:,.2f}</span></h4>"))

# Plot Regression Line
plt.figure(figsize=(10, 5))
plt.scatter(X, y, color='cyan', label='Actual Costs', alpha=0.5)
plt.plot(X, model.predict(X), color='magenta', linewidth=2, label='Regression Trend')
plt.title('Cost Trend Analysis & ML Prediction', color='white')
plt.xlabel('Days Since Start', color='white')
plt.ylabel('Daily Cost ($)', color='white')
plt.legend()
plt.show()
""")

    add_markdown("### 6.2 Anomaly Detection (Isolation Forest)")
    add_code("""# Detecting Abnormal High Bills
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df['Anomaly'] = iso_forest.fit_predict(df[['Monthly Cost', 'Usage Hours']])

anomalies = df[df['Anomaly'] == -1]
print(f"🚨 Detected {len(anomalies)} abnormal billing records!")
display(anomalies[['Billing ID', 'Department Name', 'Service Type', 'Monthly Cost']].head())

# Visualizing Anomalies
fig11 = px.scatter(df, x='Usage Hours', y='Monthly Cost', color=df['Anomaly'].astype(str),
                   title='Anomaly Detection in Cloud Billing (Red = Outliers)',
                   color_discrete_map={'-1': 'red', '1': '#00ff99'})
fig11.update_layout(template='plotly_dark')
fig11.show()
""")

    add_markdown("### 6.3 Cost Optimization Recommendations")
    add_code("""print("💡 Cost Optimization AI Recommendations:")
# Simple rule-based recommendations based on data insights
if pending_payments > total_annual_cost * 0.1:
    print("- ⚠️ Alert: High pending payments detected. Automate invoice collection.")
    
expensive_dept_cost = df[df['Department Name'] == top_expensive_dept]['Monthly Cost'].sum()
if expensive_dept_cost > total_annual_cost * 0.2:
    print(f"- 📉 Suggestion: {top_expensive_dept} consumes >20% budget. Audit their {top_expensive_service} usage.")

unused_resources = df[(df['Usage Hours'] < 50) & (df['Monthly Cost'] > 500)]
if not unused_resources.empty:
    print(f"- 🛑 Action: {len(unused_resources)} resources have low usage but high cost. Consider downsizing or shutting them down.")
""")

    # 7. Exporting
    add_markdown("## 7. Professional Export Features\n### Export Data & Analytics to Excel")
    add_code("""def export_to_excel():
    file_name = "Cloud_Cost_Intelligence_Report.xlsx"
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        # Summary Sheet
        summary_df = pd.DataFrame({
            "Metric": ["Total Cost", "Total Pending", "Top Dept", "Predicted Next Month"],
            "Value": [total_annual_cost, pending_payments, top_expensive_dept, predicted_next_month_cost]
        })
        summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
        
        dept_costs.to_excel(writer, sheet_name='Dept Analysis', index=False)
        
    print(f"✅ Full report successfully exported to {file_name}")

# Button to trigger export
export_btn = widgets.Button(description="📥 Download Excel Report", button_style='primary', icon='download')
export_out = widgets.Output()

def on_export_click(b):
    with export_out:
        export_out.clear_output()
        export_to_excel()

export_btn.on_click(on_export_click)
display(export_btn, export_out)
""")

    with open("Healthcare_Cloud_Cost_Intelligence.ipynb", "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)
    print("Notebook successfully created.")

if __name__ == "__main__":
    create_notebook()
