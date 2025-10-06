"""
Lesson 3: Caching
Make your app blazing fast with proper caching strategies
"""

import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Caching", page_icon="⚡", layout="wide")

st.title("⚡ Lesson 3: Caching")

# =============================================================================
# SECTION 1: Why Caching Matters
# =============================================================================
st.header("1. Why Caching Matters")

st.markdown("""
Remember: Streamlit **reruns your entire script** on every interaction. Without caching:

- Data loads happen every time
- Expensive computations run repeatedly  
- API calls are made over and over
- Users wait... and wait... and wait...

**Caching** tells Streamlit to remember results and reuse them!
""")

st.markdown("---")

# =============================================================================
# SECTION 2: The Problem (Without Caching)
# =============================================================================
st.header("2. The Problem: Without Caching")

st.markdown("""
Without caching, expensive queries run on every interaction. Let's use a real example: querying login history.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Without caching - this query runs EVERY time
def load_login_history():
    query = '''
    SELECT 
        user_name,
        client_ip,
        reported_client_type,
        first_authentication_factor,
        is_success,
        error_message
    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
    WHERE event_timestamp >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    LIMIT 100
    '''
    return session.sql(query).to_pandas()

# Every button click reruns this query
data = load_login_history()
st.dataframe(data)
    """, language="python")

with demo_col:
    st.info("⏳ Without caching, this query would run on every interaction")
    st.caption("💡 With real queries, caching becomes essential for performance")

st.markdown("---")

# =============================================================================
# SECTION 3: The Solution - @st.cache_data
# =============================================================================
st.header("3. @st.cache_data: Cache Data Operations")

st.markdown("""
Use `@st.cache_data` to cache query results. Perfect for Snowflake queries!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
@st.cache_data
def load_login_history():
    query = '''
    SELECT 
        user_name,
        client_ip,
        reported_client_type,
        is_success,
        COUNT(*) as login_count
    FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
    WHERE event_timestamp >= DATEADD(day, -7, CURRENT_TIMESTAMP())
    GROUP BY 1, 2, 3, 4
    LIMIT 50
    '''
    return session.sql(query).to_pandas()

# First call: queries Snowflake (cached)
# Subsequent calls: instant from cache! ⚡
data = load_login_history()
st.dataframe(data)
    """, language="python")

with demo_col:
    st.write("**Query login history with caching:**")
    
    from utils.auth import get_snowflake_session
    session = get_snowflake_session()
    
    @st.cache_data
    def cached_login_history():
        query = """
        SELECT 
            USER_NAME,
            CLIENT_IP,
            REPORTED_CLIENT_TYPE,
            IS_SUCCESS,
            COUNT(*) as LOGIN_COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
        WHERE EVENT_TIMESTAMP >= DATEADD(day, -7, CURRENT_TIMESTAMP())
        GROUP BY 1, 2, 3, 4
        ORDER BY LOGIN_COUNT DESC
        LIMIT 50
        """
        return session.sql(query).to_pandas()
    
    if st.button("Load Login History", key="cached_load_btn"):
        start = time.time()
        with st.spinner("Querying Snowflake..."):
            cached_data = cached_login_history()
        elapsed = time.time() - start
        
        if elapsed < 0.1:
            st.success(f"⚡ From cache! ({elapsed:.4f}s)")
            st.info("Click again - still instant!")
        else:
            st.info(f"First load: {elapsed:.2f}s (now cached)")
            st.success("Click again - watch it be instant!")
        
        st.dataframe(cached_data.head(10), use_container_width=True)
    
    if st.button("Another Button (Query Still Cached)", key="cached_btn"):
        st.success("Even this triggers a rerun, but query stays cached!")

st.markdown("---")

# =============================================================================
# SECTION 4: Caching with Parameters
# =============================================================================
st.header("4. Caching with Parameters")

st.markdown("""
Cache keys are based on function parameters. Different inputs = different cache.
Let's query warehouse usage for different time periods:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
@st.cache_data
def load_warehouse_usage(days_back):
    query = f'''
    SELECT 
        warehouse_name,
        ROUND(SUM(credits_used), 2) as total_credits
    FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
    WHERE start_time >= DATEADD(day, -{days_back}, CURRENT_TIMESTAMP())
    GROUP BY warehouse_name
    ORDER BY total_credits DESC
    LIMIT 10
    '''
    return session.sql(query).to_pandas()

# Each unique days_back value is cached separately
days = st.selectbox("Time Period", [1, 7, 30])
data = load_warehouse_usage(days)
st.dataframe(data)
    """, language="python")

with demo_col:
    st.write("**Select time period, then load:**")
    
    @st.cache_data
    def cached_warehouse_usage(days_back):
        query = f"""
        SELECT 
            WAREHOUSE_NAME,
            ROUND(SUM(CREDITS_USED), 2) as TOTAL_CREDITS,
            COUNT(*) as QUERY_COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        WHERE START_TIME >= DATEADD(day, -{days_back}, CURRENT_TIMESTAMP())
        GROUP BY WAREHOUSE_NAME
        ORDER BY TOTAL_CREDITS DESC
        LIMIT 10
        """
        return session.sql(query).to_pandas()
    
    days_back = st.selectbox("Days Back", [1, 7, 30, 90], key="days_slider")
    
    if st.button("Load Warehouse Usage", key="load_filtered_btn"):
        start = time.time()
        with st.spinner("Querying..."):
            filtered = cached_warehouse_usage(days_back)
        elapsed = time.time() - start
        
        if elapsed < 0.1:
            st.success(f"⚡ From cache! ({elapsed:.4f}s)")
        else:
            st.info(f"First query for {days_back} days: {elapsed:.2f}s (now cached)")
        
        if len(filtered) > 0:
            st.dataframe(filtered, use_container_width=True)
        else:
            st.info("No warehouse usage found")
        
        st.caption(f"💡 Query {days_back} days again - instant! Change period - new query, then cached!")

st.markdown("---")

# =============================================================================
# SECTION 5: @st.cache_resource for Connections
# =============================================================================
st.header("5. @st.cache_resource: Cache Global Resources")

st.markdown("""
Use `@st.cache_resource` for **global resources** like:
- Database connections
- ML models
- API clients

**Key difference:** Returns the **same object** (not a copy), shared across all users.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
@st.cache_resource
def get_database_connection():
    # Expensive connection setup
    time.sleep(2)
    return create_connection()

# All users share this same connection
conn = get_database_connection()
data = conn.query("SELECT * FROM table")
    """, language="python")

with demo_col:
    st.write("**Click the button - same connection every time:**")
    
    @st.cache_resource
    def demo_get_connection():
        time.sleep(0.5)
        return {
            'connected_at': datetime.now().strftime("%H:%M:%S"),
            'connection_id': np.random.randint(10000, 99999),
            'status': 'active'
        }
    
    if st.button("Get Connection", key="conn_btn"):
        start = time.time()
        conn = demo_get_connection()
        elapsed = time.time() - start
        
        if elapsed < 0.1:
            st.success(f"⚡ Reused existing connection ({elapsed:.4f}s)")
        else:
            st.info(f"Created new connection ({elapsed:.2f}s)")
        
        st.json(conn)
        st.caption("💡 Click again - same connection_id and timestamp every time!")

st.markdown("---")

# =============================================================================
# SECTION 6: cache_data vs cache_resource
# =============================================================================
st.header("6. When to Use Which?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("@st.cache_data")
    st.code("""
@st.cache_data
def load_data():
    return pd.DataFrame(...)

@st.cache_data
def fetch_api():
    return requests.get(...).json()

@st.cache_data
def process_data(df):
    return df.groupby(...).sum()
    """, language="python")
    
    st.success("""
    **Use for:**
    - DataFrames
    - Lists, dicts
    - API calls
    - Computations
    
    Returns a **copy**
    """)

with col2:
    st.subheader("@st.cache_resource")
    st.code("""
@st.cache_resource
def get_connection():
    return create_db_connection()

@st.cache_resource
def load_ml_model():
    return load_model("model.pkl")

@st.cache_resource
def get_api_client():
    return APIClient(credentials)
    """, language="python")
    
    st.warning("""
    **Use for:**
    - Database connections
    - ML models
    - Thread pools
    - API clients
    
    Returns **same object**
    """)

st.markdown("---")

# =============================================================================
# SECTION 7: Time-to-Live (TTL)
# =============================================================================
st.header("7. Time-to-Live (TTL)")

st.markdown("""
Set how long data stays cached:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Cache for 1 hour
@st.cache_data(ttl=3600)
def fetch_live_data():
    return api.get_latest()

# Cache for 5 minutes
@st.cache_data(ttl=300)
def get_weather():
    return weather_api.current()

# No TTL = cached forever
@st.cache_data
def load_static_data():
    return pd.read_csv("static.csv")
    """, language="python")

with demo_col:
    st.write("**Click to see TTL in action:**")
    
    @st.cache_data(ttl=10)  # 10 seconds
    def demo_ttl_data():
        return datetime.now().strftime("%H:%M:%S")
    
    if st.button("Get Current Time (Cached for 10s)", key="ttl_btn"):
        timestamp = demo_ttl_data()
        st.metric("Cached Timestamp", timestamp)
        st.info("Click again within 10 seconds - same time!")
        st.caption("Wait 10+ seconds and click again - new time!")
    
    if st.button("Clear Cache Manually", key="clear_cache"):
        st.cache_data.clear()
        st.success("Cache cleared! Click 'Get Current Time' to see new timestamp.")
        st.rerun()

st.markdown("---")

# =============================================================================
# SECTION 8: Real-World Example: Multi-Step Analysis
# =============================================================================
st.header("8. Real-World Example: Multi-Step Analysis")

st.markdown("Cache each step of a complex analysis pipeline:")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
@st.cache_data
def load_query_history(days):
    query = f'''
    SELECT * 
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE start_time >= DATEADD(day, -{days}, CURRENT_TIMESTAMP())
    '''
    return session.sql(query).to_pandas()

@st.cache_data
def analyze_by_user(df):
    return df.groupby('USER_NAME').agg({
        'QUERY_ID': 'count',
        'TOTAL_ELAPSED_TIME': 'sum'
    })

@st.cache_data  
def find_top_users(df, n=10):
    return df.nlargest(n, 'TOTAL_ELAPSED_TIME')

# Each step cached independently
days = st.selectbox("Days", [1, 7, 30])
queries = load_query_history(days)
by_user = analyze_by_user(queries)
top_users = find_top_users(by_user)
    """, language="python")

with demo_col:
    st.write("**Analyze query patterns:**")
    
    @st.cache_data
    def pipeline_load_queries(days):
        query = f"""
        SELECT 
            USER_NAME,
            QUERY_ID,
            TOTAL_ELAPSED_TIME,
            WAREHOUSE_NAME
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
        WHERE START_TIME >= DATEADD(day, -{days}, CURRENT_TIMESTAMP())
        LIMIT 1000
        """
        return session.sql(query).to_pandas()
    
    @st.cache_data
    def pipeline_analyze(df):
        return df.groupby('USER_NAME').agg({
            'QUERY_ID': 'count',
            'TOTAL_ELAPSED_TIME': 'sum'
        }).rename(columns={'QUERY_ID': 'QUERY_COUNT', 'TOTAL_ELAPSED_TIME': 'TOTAL_TIME_MS'})
    
    days_analysis = st.selectbox("Analysis Period", [1, 7, 30], key="pipeline_days")
    
    if st.button("Run Analysis", key="run_pipeline_btn"):
        start = time.time()
        with st.spinner("Running analysis..."):
            queries = pipeline_load_queries(days_analysis)
            if len(queries) > 0:
                by_user = pipeline_analyze(queries)
                top_users = by_user.nlargest(10, 'TOTAL_TIME_MS')
        elapsed = time.time() - start
        
        if elapsed < 0.2:
            st.success(f"⚡ Analysis from cache ({elapsed:.4f}s)")
        else:
            st.info(f"Analysis complete ({elapsed:.2f}s - now cached)")
        
        if len(queries) > 0:
            st.dataframe(top_users, use_container_width=True)
            st.caption(f"Top 10 users by query time over {days_analysis} days")
        else:
            st.info("No queries found in this period")
        
        st.caption("💡 Run same period again - instant! Each step is cached!")

st.markdown("---")

# =============================================================================
# SECTION 9: Common Gotcha
# =============================================================================
st.header("9. ⚠️ Common Gotcha: Don't Mutate Cached Objects")

st.markdown("""
With `@st.cache_resource`, you get the **same object**. Don't modify it!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.write("**❌ Dangerous:**")
    st.code("""
@st.cache_resource
def get_list():
    return []

shared_list = get_list()
shared_list.append("item")  # ❌ Affects ALL users!
    """, language="python")
    
    st.write("**✅ Safe:**")
    st.code("""
@st.cache_data
def get_list():
    return []

my_list = get_list()
my_list.append("item")  # ✅ Only affects this user
    """, language="python")

with demo_col:
    st.warning("""
    **Rule of Thumb:**
    
    - `@st.cache_data` - Returns copy, safe to modify
    - `@st.cache_resource` - Returns original, don't modify!
    """)
    
    st.info("""
    **Best Practice:**
    
    Use `@st.cache_data` for data you might modify.
    Use `@st.cache_resource` only for true shared resources.
    """)

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
### Two Caching Decorators:

1. **@st.cache_data** 
   - For data (DataFrames, lists, dicts)
   - Returns a copy (safe to modify)
   - Use for: data loading, transformations, computations
   
2. **@st.cache_resource**
   - For global resources (connections, models)
   - Returns the same object (shared across users)
   - Use for: database connections, ML models, API clients

### Best Practices:

- ✅ Cache expensive operations
- ✅ Use TTL for data that changes periodically
- ✅ Different parameters = different cache entries
- ✅ Clear cache when needed with `.clear()`
- ❌ Don't mutate objects from `@st.cache_resource`

### Performance Impact:

Caching can make your app **10-100x faster**! Cache early and often.

### What's Next?

In **Lesson 4: Layouts & Design**, you'll learn how to create beautiful, organized interfaces!
""")
