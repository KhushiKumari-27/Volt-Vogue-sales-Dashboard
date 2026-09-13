import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Volt & Vogue Executive Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df=pd.read_csv("volt_and_vogue_sales_200_rows.csv")
    df["Revenue"] = df["Quantity"] * df["Unit_Price"] * (1 - df["Discount_Applied"])
    return df
df=load_data()

# header in the sidebar
st.sidebar.header("🔎 Global Filters")

# Location Filter 
all_locations = df["Location"].unique()
selected_locations = st.sidebar.multiselect(
    "Select Region(s):",
    options=all_locations,
    default=all_locations
)

#  Customer Age Filter 
min_age = int(df["Customer_Age"].min())
max_age = int(df["Customer_Age"].max())
selected_age_range = st.sidebar.slider(
    "Customer Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age) 
)

#  Product Category Filter 
all_categories = df["Product_Category"].unique()
selected_categories = st.sidebar.multiselect(
    "Select Product Category:",
    options=all_categories,
    default=all_categories
)


filtered_df = df[
    (df["Location"].isin(selected_locations)) &
    (df["Customer_Age"].between(selected_age_range[0], selected_age_range[1])) &
    (df["Product_Category"].isin(selected_categories))
]




#  Main Dashboard Header
st.title("⚡ Volt & Vogue Performance Dashboard")
st.markdown("Operational data analytics executive review panel.")

metric_col1, metric_col2, metric_col3, metric_col4, metric_col5= st.columns(5)

# Column 1: Total Revenue Calculation & Display
with metric_col1:
    with st.container(height=150,width=250,border=True):
        total_rev = filtered_df["Revenue"].sum() if not filtered_df.empty else 0.0
        st.metric(
            label="💰 Total Revenue", 
            value=f"${total_rev:,.2f}"  # Formats numbers with commas and 2 decimal places (e.g., $12,450.50)
        )

# Column 2: Total Orders
with metric_col2:
    with st.container(height=150,width=250,border=True):
        total_orders = filtered_df["Order_ID"].nunique() if not filtered_df.empty else 0
        st.metric(
            label="📦 Total Orders", 
            value=total_orders
        )

# Column 3: Average Customer Rating
with metric_col3:
    with st.container(height=150,width=250,border=True):
        avg_rating = filtered_df["Customer_Rating"].mean() if not filtered_df.empty else 0.0
        st.metric(
            label="🌟 Avg Customer Rating", 
            value=f"{avg_rating:.1f} / 5.0"
        )

# Column 4: Average Discount Rate
with metric_col4:
    # Multiplied by 100 to convert decimal (0.1) to percentage (10%)
    with st.container(height=150,width=250,border=True):
        avg_discount = (filtered_df["Discount_Applied"].mean() * 100) if not filtered_df.empty else 0.0
        st.metric(
            label="📉 Avg Discount Rate", 
            value=f"{avg_discount:.1f}%"
        )
#Column 5: Total number of customers
with metric_col5:
    with st.container(height=150,width=250,border=True):
        Total_customers = filtered_df["Customer_ID"].nunique() if not filtered_df.empty else 0
        st.metric(
            label="Worked with ", 
            value=f"{Total_customers} Customers"
        )





# 2nd row 
chart_col1, chart_col2 = st.columns(2)

#  Column 1: Plotly Interactive Chart
with chart_col1:
    with st.container(border=True,height=575):
        st.subheader("💡 Demographic Trends: Age vs Revenue")
        
        
        if not filtered_df.empty:
            
            fig_scatter = px.scatter(
                filtered_df,
                x="Customer_Age",
                y="Revenue",
                color="Product_Category",      # Automatically color-codes data points by category
                size="Quantity",              # Dot size expands based on how many items were ordered
                hover_name="Product_Name",    # Shows the exact item name when a user hovers over a dot
                title="Revenue Distribution by Customer Age & Category",
                labels={"Customer_Age": "Customer Age", "Revenue": "Net Revenue ($)"},
                template="plotly_white"       # Clean, modern visual theme
            )
            
        
            st.plotly_chart(fig_scatter, width="stretch")
        else:
            st.warning("⚠️ No data available for the selected filters to generate a chart.")

# Column 2: Filtered Transaction Ledger
with chart_col2:
    with st.container(border=True,height=575):
        st.subheader("📋 Filtered Transaction Ledger")
        
        if not filtered_df.empty:
           
            st.dataframe(
                filtered_df[[
                    "Order_ID", "Date", "Customer_Age", "Location", 
                    "Product_Category", "Product_Name", "Revenue", "Customer_Rating"
                ]],
                width="stretch",   # Expands the table to fit the full column width
                hide_index=True            # Removes the ugly default row numbers index column
            )
        else:
            st.info("ℹ️ The ledger is empty because the current filters returned 0 rows.")





#  Row 3
trend_col1, trend_col2 = st.columns(2)

# Left Column: Regional Efficiency Breakdown (Bar + Color mapping)
with trend_col1:
     with st.container(border=True):
        st.subheader("📍 Regional Performance vs. Customer Satisfaction")
        
        if not filtered_df.empty:
            # Group data by location to find total revenue and average rating per region
            region_summary = filtered_df.groupby("Location").agg(
                Total_Revenue=("Revenue", "sum"),
                Avg_Rating=("Customer_Rating", "mean")
            ).reset_index()
            
            # Build a bar chart where height represents cash flow, but color reflects review rating
            fig_region = px.bar(
                region_summary,
                x="Location",
                y="Total_Revenue",
                color="Avg_Rating",
                color_continuous_scale="RdYlGn", # Red-Yellow-Green gradient (Red = bad score, Green = great score)
                title="Revenue vs Avg Rating by Region",
                labels={"Total_Revenue": "Total Net Revenue ($)", "Avg_Rating": "Avg Rating (1-5)"}
            )
            st.plotly_chart(fig_region, width="stretch")
        else:
            st.warning("⚠️ Select filters in the sidebar to populate regional breakdown charts.")

# Right Column: Timeline Sales Analysis (Chronological Line Chart)
with trend_col2:
     with st.container(border=True):
        st.subheader("📅 Monthly Sales Velocity & Seasonality")
        
        if not filtered_df.empty:
            # Create a shallow copy of the filtered dataframe to avoid setting with copy warnings
            chart_df = filtered_df.copy()
            
            # 🔥 FIX: Explicitly convert the date column by telling Pandas that Day comes first!
            chart_df["Date"] = pd.to_datetime(chart_df["Date"], format="mixed", dayfirst=True)
            
            # Extract Month name or period value to group your data Chronologically (e.g., '2025-01')
            chart_df["Year_Month"] = chart_df["Date"].dt.to_period("M").astype(str)
            
            monthly_trend = chart_df.groupby("Year_Month")["Revenue"].sum().reset_index()
            # Sort chronologically to keep the timeline straight
            monthly_trend = monthly_trend.sort_values("Year_Month")
            
            # Draw a sleek line chart showing peaks and troughs over time
            fig_trend = px.line(
                monthly_trend,
                x="Year_Month",
                y="Revenue",
                markers=True, # Adds clear coordinate dots on line peaks
                title="Net Business Revenue Trajectory",
                labels={"Year_Month": "Timeline (Months)", "Revenue": "Net Revenue ($)"}
            )
            
            # Personalize line aesthetics
            fig_trend.update_traces(line_color="#1f77b4", line_width=3)
            st.plotly_chart(fig_trend, width="stretch")
        else:
            st.warning("⚠️ Select filters in the sidebar to populate trend graphs.")

