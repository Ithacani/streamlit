import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


# Read the excel data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # You can also add columns if you want e.g. add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


# Create sidebar using column headers in the dataframe
st.sidebar.header("Please Filter Here:")


city = st.sidebar.radio(
    "Select the City:",
    df["City"].unique()
)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)
gender = st.sidebar.segmented_control(
    "Select the Gender:",
    options=df["Gender"].unique(),
    selection_mode="multi",
    default=df["Gender"].unique()
)
products = st.sidebar.segmented_control(
    "Select the Product:",
    options=df["Product_line"].unique(),
    selection_mode="multi",
    default=df["Product_line"].unique()
)
payments = st.sidebar.segmented_control(
    "Select payment type:",
    options=df["Payment"].unique(),
    selection_mode="multi",
    default=df["Payment"].unique()
)

# Then query the dataframe based on the above sidebar toggles we've created
df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender & Product_line ==@products & Payment ==@payments"
)


# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution


# Mainpage
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


# TOP section = 3 main KPI stats drawing from the df_selection variable (built on the dataframe query we've run)
total_sales = int(df_selection["Total"].sum()) # Returns the sum of the selected axis
average_rating = round(df_selection["Rating"].mean(), 1) # Returns the mean of the selected axis
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3) # Create 3 columns (st.columns(3) with our own variable names
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product_line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)