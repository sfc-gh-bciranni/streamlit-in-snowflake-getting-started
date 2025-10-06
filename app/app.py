"""
Streamlit Learning Hub - Main Page
This app teaches Streamlit concepts from the ground up, including:
- Basic concepts and widgets
- Session state management
- Caching strategies
- Streamlit execution model
- Streamlit-in-Snowflake specific features
"""

import streamlit as st
from utils.auth import get_snowflake_session

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Streamlit Learning Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get Snowflake session
session = get_snowflake_session()

# Main page header
st.title("🎓 Welcome to the Streamlit Learning Hub!")
st.markdown("### Learn Streamlit from the Ground Up")

# Detect environment
is_in_snowflake = False
try:
    from snowflake.snowpark.context import get_active_session
    get_active_session()
    is_in_snowflake = True
except:
    pass

# Environment indicator
if is_in_snowflake:
    st.success("🏔️ Running in Streamlit-in-Snowflake")
else:
    st.info("💻 Running Locally")

st.markdown("---")

# Introduction
st.markdown("""
## 📚 What You'll Learn

This interactive guide teaches you Streamlit through live examples. Each lesson shows you the code alongside the working result, so you can see exactly how everything works.

### Course Outline:

1. **🎯 Basics** - How Streamlit works and essential widgets
2. **🔄 Session State** - Persisting data across interactions
3. **⚡ Caching** - Making your app blazing fast
4. **🎨 Layouts & Design** - Interactive data exploration
5. **🏔️ Snowflake Integration** - Leveraging Streamlit-in-Snowflake
6. **🚀 Advanced Patterns** - Async queries & production techniques
7. **📖 Quick Reference** - Cheat sheet for quick lookup

### How This Works:

Every lesson shows you **the code** and **the result** side-by-side. You'll see exactly what code creates each widget and output.

""")

st.markdown("---")

# Quick reference card
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔑 Key Concepts You'll Master:
    
    - **Reruns**: How Streamlit executes from top to bottom
    - **Widgets**: Interactive components and their state
    - **Session State**: Persisting data across interactions
    - **Caching**: `@st.cache_data` and `@st.cache_resource`
    - **Forms**: Batching widget inputs
    - **Callbacks**: Functions that run on widget changes
    """)

with col2:
    st.markdown("""
    ### 🏔️ Streamlit-in-Snowflake Benefits:
    
    - **Direct Data Access**: Query Snowflake directly
    - **Async Queries**: Run queries without blocking UI
    - **Object Management**: Create/modify tables and views
    - **Built-in Security**: Snowflake role-based access
    - **Scalability**: Leverage Snowflake compute
    - **No Server Management**: Fully managed platform
    - **Version Control**: Git integration for deployment
    """)