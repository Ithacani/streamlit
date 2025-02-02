import streamlit as st
import pandas as pd
import numpy as np
import duckdb

st.write("Movies")
st.write("### This is a H2 Title!")
x = st.text_input("Movie", "Star Wars")

if st.button("Click Me"):
    st.write(f"Your favourite movie is `{x}`")


st.write("## Pandas read_csv w/ st.write")
data = pd.read_csv("./movies.csv")
st.write(data)

st.write("## duckdb.read_csv with st.dataframe")
other_data = (duckdb.read_csv("./movies.csv"))
st.dataframe(other_data)

st.write("## pd DataFrame with random numpy numbers")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.bar_chart(chart_data)