import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Setup (The "Professional Polish")
st.set_page_config(page_title="Global Sales Dashboard", page_icon="🌍", layout="wide")
st.title("🌍 Executive Sales Monitor")
st.markdown("##")

# 2. Load Real Data (Cached for performance)
# A senior analyst caches data to prevent reloading it on every user interaction.
@st.cache_data
def load_data():
    # Using a different, known-stable public CSV for sales data
    url = "https://raw.githubusercontent.com/dataprofessor/data/master/supermarket_sales.csv"
    df = pd.read_csv(url)
    return df

try:
    df = get_data()
except Exception as e:
    st.error("Error loading data. Please check your internet connection.")
    st.stop()

# 3. Sidebar Filters (User Control)
st.sidebar.header("Filter Options")

# Create a filter for 'Region'
region = st.sidebar.multiselect(
    "Select Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()[:3] # Default to first 3 regions
)

# Create a filter for 'Category'
category = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply Filters
df_selection = df.query(
    "Region == @region & Category == @category"
)

# Check if dataframe is empty
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

# 4. KPI Section (Top-Level Metrics)
total_sales = df_selection["Sales"].sum()
total_profit = df_selection["Profit"].sum()
avg_margin = (total_profit / total_sales) * 100

left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with mid_col:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
with right_col:
    st.metric(label="Profit Margin", value=f"{avg_margin:.1f}%")

st.markdown("---")

# 5. Interactive Charts (Plotly)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    # Bar Chart
    fig_bar = px.bar(
        df_selection,
        x="Category",
        y="Sales",
        color="Category",
        template="plotly_white",
        title="<b>Sales Performance</b>"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Profit vs Sales Analysis")
    # Scatter Plot
    fig_scatter = px.scatter(
        df_selection,
        x="Sales",
        y="Profit",
        color="Region",
        size="Quantity",
        hover_data=["Sub-Category"],
        template="plotly_white",
        title="<b>Profitability Cluster</b>"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# 6. Data Table (Transparency)
with st.expander("View Raw Data Source"):
    st.dataframe(df_selection)
