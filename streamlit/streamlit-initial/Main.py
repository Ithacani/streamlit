import streamlit as st
import duckdb
import numpy as np
import pandas as pd

st.link_button("Profile","/Profile")

st.write("Hello World")

x = st.text_input("Favourite movie")
st.write(f"Your favourite movie is: {x}")

st.dataframe((duckdb.read_csv('data.csv')))

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=["a","b","c"]
)

st.bar_chart(chart_data)
st.line_chart(chart_data)

st.checkbox(label="Monday")
st.checkbox(label="Tuesday")
st.checkbox(label="Wed")
st.checkbox(label="Thur")
st.checkbox(label="Friday")

with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    background_colour = st.color_picker(
        "Pick A Color", 
        "#00f900"
    )