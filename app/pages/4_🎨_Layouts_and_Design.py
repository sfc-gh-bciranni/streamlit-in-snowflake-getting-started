"""
Lesson 4: Layouts and Design
Create beautiful, organized interfaces for interactive data exploration
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import get_snowflake_session

st.set_page_config(page_title="Layouts & Design", page_icon="🎨", layout="wide")

st.title("🎨 Lesson 4: Layouts and Design")

st.markdown("""
Good layouts make data exploration intuitive and interactive. Let's use real Snowflake data to demonstrate!
""")

# Get session
session = get_snowflake_session()

st.markdown("---")

# =============================================================================
# SECTION 1: Columns with Real Metrics
# =============================================================================
st.header("1. Columns: Side-by-Side Metrics")

st.markdown("""
Columns are perfect for displaying KPIs side-by-side. Let's show real Snowflake usage metrics:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Query Snowflake for real metrics
query = '''
SELECT 
    COUNT(DISTINCT warehouse_name) as total_warehouses,
    ROUND(SUM(credits_used), 2) as total_credits,
    COUNT(*) as total_queries
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
'''

metrics = session.sql(query).to_pandas()

# Display in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Warehouses", metrics['TOTAL_WAREHOUSES'][0])
with col2:
    st.metric("Credits Used", metrics['TOTAL_CREDITS'][0])
with col3:
    st.metric("Queries", metrics['TOTAL_QUERIES'][0])
    """, language="python")

with demo_col:
    st.write("**Your Snowflake metrics:**")
    
    if st.button("Load Metrics", key="load_metrics"):
        try:
            query = """
            SELECT 
                COUNT(DISTINCT WAREHOUSE_NAME) as TOTAL_WAREHOUSES,
                ROUND(SUM(CREDITS_USED), 2) as TOTAL_CREDITS,
                COUNT(*) as TOTAL_QUERIES
            FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
            WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
            """
            metrics = session.sql(query).to_pandas()
            
            if len(metrics) > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Warehouses", int(metrics['TOTAL_WAREHOUSES'][0]))
                with col2:
                    st.metric("Credits Used", f"{metrics['TOTAL_CREDITS'][0]:.2f}")
                with col3:
                    st.metric("Queries", int(metrics['TOTAL_QUERIES'][0]))
                st.caption("Last 7 days")
            else:
                st.info("No data available")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 2: Tabs for Data Exploration
# =============================================================================
st.header("2. Tabs: Organize Different Views")

st.markdown("""
Tabs let users explore different aspects of data without scrolling. 
Let's explore queries, warehouses, and users:
""")

st.code("""
tab1, tab2, tab3 = st.tabs(["📊 Queries", "🏭 Warehouses", "👥 Users"])

with tab1:
    queries = session.sql("SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY ...").to_pandas()
    st.dataframe(queries)
    
with tab2:
    warehouses = session.sql("SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY ...").to_pandas()
    st.bar_chart(warehouses)
    
with tab3:
    users = session.sql("SELECT user_name, COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY ...").to_pandas()
    st.dataframe(users)
""", language="python")

st.subheader("Interactive Example:")

if st.button("Load Data for Tabs", key="load_tabs"):
    try:
        with st.spinner("Loading data..."):
            # Query for queries
            query_history = session.sql("""
                SELECT 
                    USER_NAME,
                    WAREHOUSE_NAME,
                    QUERY_TYPE,
                    EXECUTION_STATUS,
                    ROUND(TOTAL_ELAPSED_TIME/1000, 2) as SECONDS
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -1, CURRENT_TIMESTAMP())
                LIMIT 100
            """).to_pandas()
            
            # Query for warehouse usage
            warehouse_usage = session.sql("""
                SELECT 
                    WAREHOUSE_NAME,
                    ROUND(SUM(CREDITS_USED), 2) as CREDITS
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                GROUP BY WAREHOUSE_NAME
                ORDER BY CREDITS DESC
            """).to_pandas()
            
            # Query for user activity
            user_activity = session.sql("""
                SELECT 
                    USER_NAME,
                    COUNT(*) as QUERY_COUNT,
                    ROUND(SUM(TOTAL_ELAPSED_TIME)/1000, 2) as TOTAL_SECONDS
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                GROUP BY USER_NAME
                ORDER BY QUERY_COUNT DESC
                LIMIT 10
            """).to_pandas()
        
        tab1, tab2, tab3 = st.tabs(["📊 Recent Queries", "🏭 Warehouse Usage", "👥 Top Users"])
        
        with tab1:
            st.write(f"**{len(query_history)} queries in last 24 hours**")
            st.dataframe(query_history, use_container_width=True)
        
        with tab2:
            if len(warehouse_usage) > 0:
                st.write("**Credit usage by warehouse (last 7 days)**")
                fig = px.bar(warehouse_usage, x='WAREHOUSE_NAME', y='CREDITS', 
                            title='Credits by Warehouse')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No warehouse usage data")
        
        with tab3:
            st.write("**Most active users (last 7 days)**")
            st.dataframe(user_activity, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 3: Interactive Filtering
# =============================================================================
st.header("3. Interactive Filtering")

st.markdown("""
Combine layouts with filters to enable dynamic data exploration - 
something you can't easily do in static dashboards!
""")

st.code("""
# Filters in sidebar or columns
col1, col2 = st.columns(2)
with col1:
    days_back = st.selectbox("Time Period", [1, 7, 30])
with col2:
    warehouse = st.selectbox("Warehouse", warehouse_list)

# Query based on filters
query = f'''
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(day, -{days_back}, CURRENT_TIMESTAMP())
AND warehouse_name = '{warehouse}'
'''
filtered_data = session.sql(query).to_pandas()
st.dataframe(filtered_data)
""", language="python")

st.subheader("Try Interactive Filtering:")

# Get available warehouses first
try:
    warehouses_df = session.sql("""
        SELECT DISTINCT WAREHOUSE_NAME 
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        AND WAREHOUSE_NAME IS NOT NULL
        ORDER BY WAREHOUSE_NAME
    """).to_pandas()
    
    if len(warehouses_df) > 0:
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            days_filter = st.selectbox("Days Back", [1, 7, 30], key="filter_days")
        
        with filter_col2:
            warehouse_filter = st.selectbox(
                "Warehouse", 
                ["All"] + warehouses_df['WAREHOUSE_NAME'].tolist(),
                key="filter_warehouse"
            )
        
        if st.button("Apply Filters", key="apply_filters"):
            try:
                warehouse_clause = "" if warehouse_filter == "All" else f"AND WAREHOUSE_NAME = '{warehouse_filter}'"
                
                query = f"""
                SELECT 
                    QUERY_TYPE,
                    WAREHOUSE_NAME,
                    EXECUTION_STATUS,
                    USER_NAME,
                    ROUND(TOTAL_ELAPSED_TIME/1000, 2) as SECONDS
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -{days_filter}, CURRENT_TIMESTAMP())
                {warehouse_clause}
                LIMIT 100
                """
                
                filtered_data = session.sql(query).to_pandas()
                
                st.success(f"✅ Found {len(filtered_data)} queries")
                st.dataframe(filtered_data, use_container_width=True)
                
                # Show summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Queries", len(filtered_data))
                with col2:
                    success_rate = (filtered_data['EXECUTION_STATUS'] == 'SUCCESS').sum() / len(filtered_data) * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                with col3:
                    avg_time = filtered_data['SECONDS'].mean()
                    st.metric("Avg Time", f"{avg_time:.2f}s")
                    
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("No warehouse data available")
        
except Exception as e:
    st.warning("Unable to load warehouses. Try the demo with available data.")

st.markdown("---")

# =============================================================================
# SECTION 4: Expanders for Detailed Analysis
# =============================================================================
st.header("4. Expanders: Hide Details Until Needed")

st.markdown("""
Use expanders to show detailed analysis without cluttering the interface:
""")

st.code("""
st.subheader("Query Analysis")

with st.expander("📊 View Detailed Statistics"):
    st.write("**Query Type Distribution:**")
    st.bar_chart(query_type_counts)
    
with st.expander("🔍 View Slowest Queries"):
    slowest = data.nlargest(10, 'execution_time')
    st.dataframe(slowest)
    
with st.expander("⚙️ Advanced Settings"):
    threshold = st.slider("Performance Threshold (seconds)", 1, 60)
    st.write(f"Queries slower than {threshold}s")
""", language="python")

st.subheader("Interactive Example:")

if st.button("Load Query Analysis", key="load_analysis"):
    try:
        analysis_data = session.sql("""
            SELECT 
                QUERY_TYPE,
                COUNT(*) as COUNT,
                ROUND(AVG(TOTAL_ELAPSED_TIME)/1000, 2) as AVG_SECONDS,
                ROUND(MAX(TOTAL_ELAPSED_TIME)/1000, 2) as MAX_SECONDS
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
            AND QUERY_TYPE IS NOT NULL
            GROUP BY QUERY_TYPE
            ORDER BY COUNT DESC
            LIMIT 10
        """).to_pandas()
        
        st.success(f"✅ Analyzed queries from last 7 days")
        
        with st.expander("📊 Query Type Distribution", expanded=True):
            if len(analysis_data) > 0:
                fig = px.bar(analysis_data, x='QUERY_TYPE', y='COUNT',
                            title='Queries by Type')
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(analysis_data, use_container_width=True)
        
        with st.expander("🐌 Performance Analysis"):
            slowest_queries = session.sql("""
                SELECT 
                    QUERY_TEXT,
                    USER_NAME,
                    ROUND(TOTAL_ELAPSED_TIME/1000, 2) as SECONDS,
                    EXECUTION_STATUS
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                AND TOTAL_ELAPSED_TIME IS NOT NULL
                ORDER BY TOTAL_ELAPSED_TIME DESC
                LIMIT 10
            """).to_pandas()
            
            if len(slowest_queries) > 0:
                st.write("**Top 10 slowest queries:**")
                st.dataframe(slowest_queries, use_container_width=True)
        
        with st.expander("⚙️ Custom Analysis Settings"):
            threshold = st.slider("Time Threshold (seconds)", 1, 60, 10)
            slow_count = session.sql(f"""
                SELECT COUNT(*) as SLOW_QUERIES
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                AND TOTAL_ELAPSED_TIME > {threshold * 1000}
            """).to_pandas()
            
            if len(slow_count) > 0:
                st.metric(f"Queries > {threshold}s", int(slow_count['SLOW_QUERIES'][0]))
                
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 5: Complete Interactive Dashboard
# =============================================================================
st.header("5. Complete Interactive Dashboard")

st.markdown("""
Putting it all together: a fully interactive Snowflake monitoring dashboard!
This shows how Streamlit enables exploration beyond static BI tools.
""")

st.subheader("Snowflake Usage Dashboard")

if st.button("🚀 Launch Interactive Dashboard", key="launch_dashboard"):
    try:
        with st.spinner("Loading dashboard data..."):
            # Get overall metrics
            metrics_query = """
            SELECT 
                COUNT(DISTINCT USER_NAME) as TOTAL_USERS,
                COUNT(DISTINCT WAREHOUSE_NAME) as TOTAL_WAREHOUSES,
                COUNT(*) as TOTAL_QUERIES,
                ROUND(SUM(TOTAL_ELAPSED_TIME)/1000, 2) as TOTAL_TIME_SECONDS
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
            """
            metrics = session.sql(metrics_query).to_pandas()
            
            # Get time series data
            timeseries_query = """
            SELECT 
                DATE(START_TIME) as DATE,
                COUNT(*) as QUERY_COUNT
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
            GROUP BY DATE(START_TIME)
            ORDER BY DATE
            """
            timeseries = session.sql(timeseries_query).to_pandas()
        
        # Display metrics
        st.markdown("### 📊 7-Day Overview")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Active Users", int(metrics['TOTAL_USERS'][0]))
        with kpi2:
            st.metric("Warehouses Used", int(metrics['TOTAL_WAREHOUSES'][0]))
        with kpi3:
            st.metric("Total Queries", int(metrics['TOTAL_QUERIES'][0]))
        with kpi4:
            st.metric("Total Time", f"{metrics['TOTAL_TIME_SECONDS'][0]:.0f}s")
        
        # Time series chart
        st.markdown("### 📈 Query Trend")
        if len(timeseries) > 0:
            fig = px.line(timeseries, x='DATE', y='QUERY_COUNT',
                         title='Queries per Day')
            st.plotly_chart(fig, use_container_width=True)
        
        # Interactive tabs for deeper analysis
        analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs([
            "🏭 Warehouse Analysis",
            "👥 User Activity", 
            "🔍 Query Details"
        ])
        
        with analysis_tab1:
            warehouse_data = session.sql("""
                SELECT 
                    WAREHOUSE_NAME,
                    COUNT(*) as QUERIES,
                    ROUND(AVG(TOTAL_ELAPSED_TIME)/1000, 2) as AVG_TIME_SEC
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                AND WAREHOUSE_NAME IS NOT NULL
                GROUP BY WAREHOUSE_NAME
                ORDER BY QUERIES DESC
                LIMIT 10
            """).to_pandas()
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Query Count by Warehouse**")
                if len(warehouse_data) > 0:
                    fig = px.pie(warehouse_data, values='QUERIES', names='WAREHOUSE_NAME')
                    st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.write("**Average Query Time**")
                if len(warehouse_data) > 0:
                    st.dataframe(warehouse_data, use_container_width=True)
        
        with analysis_tab2:
            user_data = session.sql("""
                SELECT 
                    USER_NAME,
                    COUNT(*) as QUERIES,
                    ROUND(SUM(TOTAL_ELAPSED_TIME)/1000, 2) as TOTAL_TIME_SEC
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                GROUP BY USER_NAME
                ORDER BY QUERIES DESC
                LIMIT 15
            """).to_pandas()
            
            if len(user_data) > 0:
                st.write("**Top Users by Query Count**")
                fig = px.bar(user_data, x='USER_NAME', y='QUERIES',
                            title='Queries per User')
                st.plotly_chart(fig, use_container_width=True)
        
        with analysis_tab3:
            # Interactive query explorer
            status_filter = st.multiselect(
                "Filter by Status",
                ["SUCCESS", "FAILED", "RUNNING"],
                default=["SUCCESS", "FAILED"]
            )
            
            if status_filter:
                status_clause = "'" + "','".join(status_filter) + "'"
                query_details = session.sql(f"""
                    SELECT 
                        QUERY_TYPE,
                        EXECUTION_STATUS,
                        USER_NAME,
                        WAREHOUSE_NAME,
                        ROUND(TOTAL_ELAPSED_TIME/1000, 2) as SECONDS
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                    WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                    AND EXECUTION_STATUS IN ({status_clause})
                    LIMIT 100
                """).to_pandas()
                
                if len(query_details) > 0:
                    st.dataframe(query_details, use_container_width=True)
                    
                    # Download option
                    csv = query_details.to_csv(index=False)
                    st.download_button(
                        "📥 Download Query Data",
                        csv,
                        "query_analysis.csv",
                        "text/csv"
                    )
        
        st.success("✨ Dashboard loaded! Explore different tabs and filters.")
        st.caption("💡 This level of interactivity goes beyond traditional BI dashboards!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
### Layout Components for Interactive Exploration:

1. **Columns** - Perfect for side-by-side metrics and comparisons
2. **Tabs** - Organize different data views without scrolling
3. **Expanders** - Hide details until needed, keep interface clean
4. **Filters + Queries** - Enable dynamic data exploration
5. **Combined Layouts** - Create full interactive dashboards

### Beyond Static Dashboards:

Traditional BI tools show **fixed views** of data. With Streamlit:
- ✅ Users can **filter and explore** interactively
- ✅ Queries **update dynamically** based on selections
- ✅ Multiple analysis paths in **one application**
- ✅ **Download capabilities** for further analysis
- ✅ Real-time exploration of **Snowflake metadata**

### Best Practices:

✅ **DO:**
- Use columns for KPIs and metrics
- Group related views in tabs
- Add filters for interactive exploration
- Hide advanced options in expanders
- Show loading indicators for queries
- Provide download options

❌ **DON'T:**
- Nest columns too deeply (max 2-3 levels)
- Put too much in sidebar
- Create overly complex layouts
- Forget loading states

### What's Next?

In **Lesson 5: Snowflake Integration**, you'll dive deeper into querying and manipulating Snowflake data!
""")
