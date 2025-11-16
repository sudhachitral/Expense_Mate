import streamlit as st
import pandas as pd
import plotly.express as px
from db import create_table, insert_expense, fetch_expenses, delete_expense

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Load table
create_table()

st.title("💸 Expense Tracker (Advanced Version)")

# Sidebar Filters
st.sidebar.header("Filters")
selected_category = st.sidebar.selectbox(
    "Filter By Category",
    ["All"] + ["food", "transport", "shopping", "bills", "others"]
)

search_text = st.sidebar.text_input("Search Description")

# Add new expense
with st.expander("➕ Add New Expense"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date")
    with col2:
        category = st.selectbox("Category", ["food", "transport", "shopping", "bills", "others"])
    with col3:
        amount = st.number_input("Amount (₹)", min_value=0.0)

    description = st.text_input("Description")

    if st.button("Add Expense"):
        insert_expense(str(date), category, amount, description)
        st.success("Expense added successfully!")

# Fetch Data
rows = fetch_expenses()
df = pd.DataFrame(rows, columns=["ID", "Date", "Category", "Amount", "Description"])

# Apply Filters
if selected_category != "All":
    df = df[df["Category"] == selected_category]

if search_text.strip():
    df = df[df["Description"].str.contains(search_text, case=False, na=False)]

# Summary Stats
total_spent = df["Amount"].sum()
monthly_total = total_spent
biggest_expense = df["Amount"].max() if not df.empty else 0
food_total = df[df["Category"] == "food"]["Amount"].sum()

# Summary Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total This Month", f"₹{monthly_total}")
col2.metric("Biggest Expense", f"₹{biggest_expense}")
col3.metric("Food Expenses", f"₹{food_total}")

# Charts
if not df.empty:
    colA, colB = st.columns(2)

    with colA:
        fig = px.pie(df, names="Category", values="Amount", title="Category Breakdown")
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        df_sorted = df.sort_values("Date")
        fig2 = px.line(df_sorted, x="Date", y="Amount", title="Spending Trend")
        st.plotly_chart(fig2, use_container_width=True)

# Display Table
st.subheader("📄 All Expenses")
st.dataframe(df, use_container_width=True)

# Delete Option
delete_id = st.number_input("Enter ID to Delete", min_value=1)
if st.button("Delete Expense"):
    delete_expense(delete_id)
    st.warning("Expense Deleted!")
