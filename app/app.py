import streamlit as st
from utils.auth import get_snowflake_session

session = get_snowflake_session()

st.title("Snowflake Streamlit Demo")

st.write(session.sql("SELECT CURRENT_USER()").collect())