import pandas as pd
import streamlit as st
import pandasql as ps

st.title("CSV Explorer with SQL Query")

data_file = st.file_uploader("Upload a CSV file", type=["csv"])

if data_file is not None:

    df = pd.read_csv(data_file)

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Column Data Types")
    st.write(df.dtypes)


    st.subheader("Enter SQL Query")
    st.markdown("Use data as the table name in your SQL query.")
    
    query = st.text_area(
        "enter your SQL query here",
    )

    if st.button("Run Query"):
        try:
            result = ps.sqldf(query, {"data": df})
            st.subheader("Query Result")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error executing query: {e}")
