"""
Sales Performance Analytics — Streamlit Dashboard
Run locally with:  streamlit run app.py
Expects Dataset/cleaned_sales.csv to sit one level above this file
(adjust DATA_PATH below if you place app.py elsewhere).
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = "../Dataset/cleaned_sales.csv"


# ------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])
    return df


try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Couldn't find `{DATA_PATH}`. Update DATA_PATH at the top of app.py "
        "to point at your cleaned_sales.csv."
    )
    st.stop()


# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")

min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category", options=categories, default=categories
)

countries = sorted(df["Country"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Country (leave empty for all)", options=countries, default=[]
)

# Apply filters
mask = (
    (df["Order Date"] >= pd.to_datetime(date_range[0]))
    & (df["Order Date"] <= pd.to_datetime(date_range[1]))
    & (df["Category"].isin(selected_categories))
)
if selected_countries:
    mask &= df["Country"].isin(selected_countries)

fdf = df[mask]

if fdf.empty:
    st.warning("No data matches the current filters. Adjust the sidebar and try again.")
    st.stop()


# ------------------------------------------------------------------
# Header + KPIs
# ------------------------------------------------------------------
st.title("Sales Performance Analytics")
st.caption("Global Superstore dataset — sales trends, profitability, and forecasting")

total_sales = fdf["Sales"].sum()
total_profit = fdf["Profit"].sum()
total_orders = fdf["Order ID"].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Sales", f"${total_sales:,.0f}")
k2.metric("Total Profit", f"${total_profit:,.0f}")
k3.metric("Total Orders", f"{total_orders:,}")
k4.metric("Profit Margin", f"{profit_margin:.1f}%")

st.divider()


# ------------------------------------------------------------------
# Sales & profit by category / region
# ------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales & Profit by Category")
    cat_summary = (
        fdf.groupby("Category")[["Sales", "Profit"]].sum().reset_index().sort_values("Sales", ascending=False)
    )
    fig = px.bar(cat_summary, x="Category", y=["Sales", "Profit"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Countries by Sales")
    country_summary = (
        fdf.groupby("Country")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    )
    fig = px.bar(country_summary, x="Sales", y="Country", orientation="h")
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------
# Monthly sales trend
# ------------------------------------------------------------------
st.subheader("Monthly Sales & Profit Trend")
monthly = (
    fdf.set_index("Order Date")
    .resample("MS")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)
fig = px.line(monthly, x="Order Date", y=["Sales", "Profit"])
st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------
# Top products
# ------------------------------------------------------------------
st.subheader("Top 10 Products by Sales")
top_products = (
    fdf.groupby("Product Name")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
)
fig = px.bar(top_products, x="Sales", y="Product Name", orientation="h")
fig.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------
# Discount vs Profit
# ------------------------------------------------------------------
st.subheader("Discount vs. Profit")
fig = px.scatter(
    fdf.sample(min(3000, len(fdf)), random_state=42),
    x="Discount",
    y="Profit",
    color="Category",
    opacity=0.6,
)
st.plotly_chart(fig, use_container_width=True)

st.divider()


# ------------------------------------------------------------------
# Forecasting panel (Linear Regression with lag features)
# ------------------------------------------------------------------
st.header("Sales Forecast")
st.caption("Linear Regression with lag features (Lag_1, Lag_2, Lag_12) — same approach as the project notebook")

full_monthly = (
    df.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
)
full_monthly.columns = ["Date", "Sales"]
full_monthly["Lag_1"] = full_monthly["Sales"].shift(1)
full_monthly["Lag_2"] = full_monthly["Sales"].shift(2)
full_monthly["Lag_12"] = full_monthly["Sales"].shift(12)
lag_data = full_monthly.dropna().reset_index(drop=True)

if len(lag_data) < 10:
    st.info("Not enough months of data to build a reliable lag-feature forecast.")
else:
    split_index = int(len(lag_data) * 0.8)
    train, test = lag_data.iloc[:split_index], lag_data.iloc[split_index:]

    features = ["Lag_1", "Lag_2", "Lag_12"]
    model = LinearRegression()
    model.fit(train[features], train["Sales"])

    pred = model.predict(test[features])
    mae = mean_absolute_error(test["Sales"], pred)
    rmse = np.sqrt(mean_squared_error(test["Sales"], pred))
    r2 = r2_score(test["Sales"], pred)

    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{mae:,.0f}")
    m2.metric("RMSE", f"{rmse:,.0f}")
    m3.metric("R²", f"{r2:.3f}")

    results = test[["Date", "Sales"]].copy()
    results["Predicted"] = pred
    fig = px.line(results, x="Date", y=["Sales", "Predicted"], title="Actual vs. Predicted Monthly Sales")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Project Sales Forward")
    horizon = st.slider("Months to forecast ahead", min_value=1, max_value=6, value=3)

    history = full_monthly[["Date", "Sales"]].copy()
    future_rows = []
    for _ in range(horizon):
        lag_1 = history["Sales"].iloc[-1]
        lag_2 = history["Sales"].iloc[-2]
        lag_12 = history["Sales"].iloc[-12] if len(history) >= 12 else history["Sales"].mean()
        next_features = pd.DataFrame([[lag_1, lag_2, lag_12]], columns=features)
        next_pred = model.predict(next_features)[0]
        next_date = history["Date"].iloc[-1] + pd.DateOffset(months=1)
        future_rows.append({"Date": next_date, "Sales": next_pred})
        history = pd.concat([history, pd.DataFrame([{"Date": next_date, "Sales": next_pred}])], ignore_index=True)

    future_df = pd.DataFrame(future_rows)
    combined = pd.concat(
        [full_monthly[["Date", "Sales"]].assign(Type="Actual"), future_df.assign(Type="Forecast")]
    )
    fig = px.line(combined, x="Date", y="Sales", color="Type", title="Sales History + Forecast")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(future_df.assign(Sales=future_df["Sales"].round(2)), use_container_width=True, hide_index=True)

st.divider()
st.caption("Built with Streamlit · Data: Global Superstore 2016")
