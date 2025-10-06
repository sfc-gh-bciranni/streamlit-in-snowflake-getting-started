"""
Lesson 5: Streamlit-in-Snowflake Integration
Leverage the power of Snowflake directly in your apps
"""

import streamlit as st
from utils.auth import get_snowflake_session
import pandas as pd
import numpy as np

st.set_page_config(page_title="Snowflake Integration", page_icon="🏔️", layout="wide")

st.title("🏔️ Lesson 5: Streamlit-in-Snowflake Integration")

# Get session
session = get_snowflake_session()

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
    st.info("💻 Running Locally (using configured Snowflake connection)")

st.markdown("---")

# =============================================================================
# SECTION 1: Why Streamlit-in-Snowflake?
# =============================================================================
st.header("1. Why Streamlit-in-Snowflake?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Traditional Streamlit")
    st.markdown("""
    - You manage hosting
    - Handle security yourself  
    - Configure credentials
    - Maintain infrastructure
    - Pay for separate hosting
    """)

with col2:
    st.subheader("Streamlit-in-Snowflake")
    st.markdown("""
    - ✅ Snowflake handles hosting
    - ✅ Inherits Snowflake RBAC
    - ✅ No credential management
    - ✅ Fully managed platform
    - ✅ No extra hosting costs
    """)

st.markdown("### Key Benefits:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🔐 Security**
    - Role-based access
    - Row-level security
    - Built-in audit logs
    - No exposed credentials
    """)

with col2:
    st.markdown("""
    **⚡ Performance**
    - Direct data access
    - Snowflake compute
    - Result caching
    - Auto-scaling
    """)

with col3:
    st.markdown("""
    **🔄 Deployment**
    - Git integration
    - Auto-updates
    - Version control
    - High availability
    """)

st.markdown("---")

# =============================================================================
# SECTION 2: Getting the Snowpark Session
# =============================================================================
st.header("2. Getting the Snowpark Session")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
from snowflake.snowpark.context import get_active_session

# In Streamlit-in-Snowflake
session = get_active_session()

# For local development
from snowflake.snowpark import Session
session = Session.builder.config(
    "connection_name", 
    "my_connection"
).create()
    """, language="python")
    
    st.info("""
    The `utils/auth.py` file handles both environments automatically!
    """)

with demo_col:
    st.write("**Your Current Session:**")
    try:
        current_db = session.get_current_database()
        current_schema = session.get_current_schema()
        current_warehouse = session.get_current_warehouse()
        current_role = session.get_current_role()
        
        st.write(f"📊 Database: `{current_db or 'N/A'}`")
        st.write(f"📁 Schema: `{current_schema or 'N/A'}`")
        st.write(f"🏭 Warehouse: `{current_warehouse or 'N/A'}`")
        st.write(f"👤 Role: `{current_role or 'N/A'}`")
    except Exception as e:
        st.warning(f"Could not get session info: {e}")

st.markdown("---")

# =============================================================================
# SECTION 3: Querying Data
# =============================================================================
st.header("3. Querying Snowflake Data")

st.markdown("There are multiple ways to query data from Snowflake:")

tab1, tab2, tab3 = st.tabs(["SQL Queries", "Snowpark DataFrame", "When to Use Each"])

with tab1:
    st.subheader("Direct SQL Queries")
    
    code_col, info_col = st.columns([1, 1])
    
    with code_col:
        st.code("""
# Execute SQL
result = session.sql('''
    SELECT * FROM my_table
    WHERE date >= '2024-01-01'
    LIMIT 100
''').to_pandas()

st.dataframe(result)
        """, language="python")
    
    with info_col:
        st.markdown("""
        **Best for:**
        - Simple queries
        - When you know SQL well
        - Quick data exploration
        - One-off analysis
        """)
    
    st.write("**Example: System Information**")
    try:
        query = "SELECT CURRENT_VERSION() as VERSION, CURRENT_ACCOUNT() as ACCOUNT, CURRENT_REGION() as REGION"
        result = session.sql(query).to_pandas()
        st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

with tab2:
    st.subheader("Snowpark DataFrame API")
    
    code_col, info_col = st.columns([1, 1])
    
    with code_col:
        st.code("""
from snowflake.snowpark.functions import col, sum

# Build query programmatically
df = session.table("sales")
result = df.filter(col("amount") > 100) \\
           .group_by("region") \\
           .agg(sum("amount").alias("total"))

# Convert to Pandas when needed
pandas_df = result.to_pandas()
        """, language="python")
    
    with info_col:
        st.markdown("""
        **Best for:**
        - Complex transformations
        - Dynamic filtering
        - Type-safe operations
        - Large datasets
        
        **Key advantage:**
        Computation happens in Snowflake!
        """)

with tab3:
    st.markdown("""
    ### Decision Guide
    
    | Scenario | Use This |
    |----------|----------|
    | Simple SELECT query | SQL |
    | Need to build query dynamically | Snowpark DataFrame |
    | Large dataset (>1M rows) | Snowpark DataFrame |
    | Complex joins and aggregations | Either (your preference) |
    | Small result set (<10K rows) | Either |
    | Want type safety | Snowpark DataFrame |
    """)

st.markdown("---")

# =============================================================================
# SECTION 4: Creating Snowflake Objects
# =============================================================================
st.header("4. Creating Snowflake Objects")

st.markdown("""
Unlike traditional BI tools, Streamlit-in-Snowflake can **create and modify** Snowflake objects!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'score': [95, 87, 92]
})

# Write to Snowflake
session.write_pandas(
    df, 
    table_name='DEMO_TABLE',
    database='MY_DB',
    schema='MY_SCHEMA',
    auto_create_table=True,
    overwrite=True
)

st.success("Table created!")
    """, language="python")

with demo_col:
    st.write("**Try creating a demo table:**")
    
    # Query available databases and schemas
    try:
        # Get available databases
        dbs_result = session.sql("SHOW DATABASES").collect()
        available_dbs = [row['name'] for row in dbs_result]
        
        if available_dbs:
            selected_db = st.selectbox("Select Database", available_dbs, key="create_db")
            
            # Get schemas for selected database
            schemas_result = session.sql(f"SHOW SCHEMAS IN DATABASE {selected_db}").collect()
            available_schemas = [row['name'] for row in schemas_result if row['name'] not in ['INFORMATION_SCHEMA']]
            
            if available_schemas:
                selected_schema = st.selectbox("Select Schema", available_schemas, key="create_schema")
                
                table_name = st.text_input("Table Name", "STREAMLIT_DEMO_TABLE", key="table_name")
                
                # Sample data
                sample_df = pd.DataFrame({
                    'id': [1, 2, 3],
                    'name': ['Alice', 'Bob', 'Charlie'],
                    'score': [95, 87, 92]
                })
                
                st.write("**Data to write:**")
                st.dataframe(sample_df, use_container_width=True)
                
                if st.button("Create Table", key="create_table_btn"):
                    try:
                        with st.spinner(f"Creating table {selected_db}.{selected_schema}.{table_name}..."):
                            session.write_pandas(
                                sample_df,
                                table_name=table_name,
                                database=selected_db,
                                schema=selected_schema,
                                auto_create_table=True,
                                overwrite=True
                            )
                        st.success(f"✅ Table created: {selected_db}.{selected_schema}.{table_name}")
                        st.info("💡 You can query this table in the section below!")
                    except Exception as e:
                        st.error(f"❌ Error creating table: {e}")
                        st.caption("You may not have CREATE TABLE permissions in this schema.")
            else:
                st.warning("No schemas available in this database")
        else:
            st.warning("No databases available")
            
    except Exception as e:
        st.error(f"Error querying databases: {e}")
        st.info("""
        **What you can create:**
        - Tables
        - Views  
        - Stored procedures
        - Tasks
        - Streams
        
        **Use cases:**
        - Data upload tools
        - Admin dashboards
        - ETL interfaces
        - Schema management
        """)

st.markdown("---")

# =============================================================================
# SECTION 5: Performance Best Practices
# =============================================================================
st.header("5. Performance Best Practices")

st.markdown("""
**Golden Rule:** Keep data in Snowflake, push computation there!
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ Don't Do This")
    st.code("""
# Downloads ALL data to Python
df = session.table("huge_table").to_pandas()

# Filters in Python (slow!)
filtered = df[df['amount'] > 100]

# Aggregates in Python (slow!)
summary = filtered.groupby('region')['amount'].sum()
    """, language="python")
    
    st.error("This downloads millions of rows just to filter and aggregate!")

with col2:
    st.subheader("✅ Do This Instead")
    st.code("""
# Filters in Snowflake (fast!)
result = session.table("huge_table") \\
    .filter(col("amount") > 100) \\
    .group_by("region") \\
    .agg(sum("amount"))

# Only download the summary
summary = result.to_pandas()
    """, language="python")
    
    st.success("Only downloads the aggregated results!")

st.markdown("---")

# =============================================================================
# SECTION 6: User Context and Security
# =============================================================================
st.header("6. User Context and Security")

st.markdown("""
Streamlit-in-Snowflake automatically knows who the user is and what they can access:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Get current user info
user_info = session.sql('''
    SELECT 
        CURRENT_USER() as user,
        CURRENT_ROLE() as role,
        CURRENT_ACCOUNT() as account
''').to_pandas()

st.write(f"Welcome, {user_info.iloc[0, 0]}!")

# Query respects user's permissions
data = session.sql('SELECT * FROM sensitive_table').to_pandas()
# User only sees what they're authorized to see!
    """, language="python")

with demo_col:
    st.markdown("""
    **Security Benefits:**
    
    - ✅ No credentials in code
    - ✅ Inherits Snowflake RBAC
    - ✅ Row-level security works
    - ✅ Audit logging automatic
    - ✅ Users can't escalate permissions
    """)
    
    try:
        user_query = "SELECT CURRENT_USER() as USER_NAME, CURRENT_ROLE() as ROLE"
        user_info = session.sql(user_query).to_pandas()
        st.success(f"👋 Logged in as: **{user_info.iloc[0, 0]}**")
        st.write(f"Role: **{user_info.iloc[0, 1]}**")
    except Exception as e:
        st.info("User context available when running in Snowflake")

st.markdown("---")

# =============================================================================
# SECTION 7: Caching with Snowflake
# =============================================================================
st.header("7. Caching Snowflake Queries")

st.markdown("""
Combine Streamlit caching with Snowflake's built-in result cache for maximum performance:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_sales_data(start_date, end_date):
    query = f'''
        SELECT * FROM sales
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
    '''
    return session.sql(query).to_pandas()

# First call: Queries Snowflake
# Subsequent calls: From Streamlit cache
# If Streamlit cache expires: Snowflake result cache may still have it!
df = load_sales_data('2024-01-01', '2024-12-31')
    """, language="python")

with demo_col:
    st.markdown("""
    **Double Caching:**
    
    1. **Snowflake Result Cache** (automatic)
       - Caches query results in Snowflake
       - Shared across all users
       - Very fast for repeated queries
    
    2. **Streamlit Cache** (@st.cache_data)
       - Caches the Pandas DataFrame
       - Avoids network call to Snowflake
       - Per-user caching
    
    **Result:** ⚡ Lightning fast! ⚡
    """)

st.markdown("---")

# =============================================================================
# SECTION 8: Querying Account Usage
# =============================================================================
st.header("8. Query Account Usage Data")

st.markdown("""
**Every Snowflake account has access to the `SNOWFLAKE.ACCOUNT_USAGE` schema.**

This schema contains valuable insights about your Snowflake usage, queries, and resources.
Let's explore some practical examples:
""")

st.subheader("Example 1: Query History")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Query recent SQL executions
query = '''
SELECT 
    query_text,
    user_name,
    warehouse_name,
    execution_status,
    total_elapsed_time / 1000 as seconds,
    start_time
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
ORDER BY start_time DESC
LIMIT 10
'''

df = session.sql(query).to_pandas()
st.dataframe(df)
    """, language="python")

with demo_col:
    st.write("**See your recent queries:**")
    
    if st.button("Load Query History", key="query_history_btn"):
        try:
            with st.spinner("Loading query history..."):
                query = """
                SELECT 
                    QUERY_TEXT,
                    USER_NAME,
                    WAREHOUSE_NAME,
                    EXECUTION_STATUS,
                    ROUND(TOTAL_ELAPSED_TIME / 1000, 2) as SECONDS,
                    START_TIME
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                WHERE START_TIME >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
                ORDER BY START_TIME DESC
                LIMIT 10
                """
                result = session.sql(query).to_pandas()
            
            st.success(f"✅ Found {len(result)} recent queries")
            st.dataframe(result, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

st.subheader("Example 2: Warehouse Usage")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Analyze warehouse credit usage
query = '''
SELECT 
    warehouse_name,
    SUM(credits_used) as total_credits,
    COUNT(*) as num_queries
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC
'''

df = session.sql(query).to_pandas()
st.bar_chart(df.set_index('WAREHOUSE_NAME')['TOTAL_CREDITS'])
    """, language="python")

with demo_col:
    st.write("**Analyze warehouse usage:**")
    
    if st.button("Load Warehouse Usage", key="warehouse_usage_btn"):
        try:
            with st.spinner("Loading warehouse usage..."):
                query = """
                SELECT 
                    WAREHOUSE_NAME,
                    ROUND(SUM(CREDITS_USED), 2) as TOTAL_CREDITS,
                    COUNT(*) as NUM_QUERIES
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
                WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                GROUP BY WAREHOUSE_NAME
                ORDER BY TOTAL_CREDITS DESC
                LIMIT 10
                """
                result = session.sql(query).to_pandas()
            
            if len(result) > 0:
                st.success(f"✅ Found usage for {len(result)} warehouses")
                st.dataframe(result, use_container_width=True)
                
                if 'TOTAL_CREDITS' in result.columns and 'WAREHOUSE_NAME' in result.columns:
                    st.bar_chart(result.set_index('WAREHOUSE_NAME')['TOTAL_CREDITS'])
            else:
                st.info("No warehouse usage found in the last 7 days")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

st.subheader("Example 3: Table Storage")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Find largest tables
query = '''
SELECT 
    table_catalog || '.' || table_schema || '.' || table_name as full_table_name,
    ROUND(active_bytes / 1024 / 1024 / 1024, 2) as size_gb,
    row_count
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE deleted IS NULL
ORDER BY active_bytes DESC
LIMIT 10
'''

df = session.sql(query).to_pandas()
st.dataframe(df)
    """, language="python")

with demo_col:
    st.write("**Find your largest tables:**")
    
    if st.button("Load Table Storage", key="table_storage_btn"):
        try:
            with st.spinner("Loading table storage metrics..."):
                query = """
                SELECT 
                    TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME as FULL_TABLE_NAME,
                    ROUND(ACTIVE_BYTES / 1024 / 1024 / 1024, 2) as SIZE_GB,
                    ROW_COUNT
                FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
                WHERE DELETED IS NULL
                ORDER BY ACTIVE_BYTES DESC
                LIMIT 10
                """
                result = session.sql(query).to_pandas()
            
            if len(result) > 0:
                st.success(f"✅ Found {len(result)} tables")
                st.dataframe(result, use_container_width=True)
            else:
                st.info("No table storage metrics available")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
### Streamlit-in-Snowflake Benefits:

1. **🔐 Security** - Inherits Snowflake RBAC, no credential management
2. **⚡ Performance** - Direct data access, leverage Snowflake compute
3. **🔄 Deployment** - Git integration, automatic updates
4. **🛠️ Full Access** - Query, create, and modify Snowflake objects

### Best Practices:

✅ **DO:**
- Push computation to Snowflake
- Use Snowpark DataFrame for large data
- Cache expensive queries
- Leverage user context for security

❌ **DON'T:**
- Download large datasets to Pandas
- Process big data in Python
- Hardcode credentials
- Forget about Snowflake compute costs

### Performance Tips:

- Filter and aggregate in Snowflake, not Python
- Use `@st.cache_data` for queries
- Combine Snowflake's result cache with Streamlit caching
- Monitor warehouse usage

### Account Usage Schema:

The `SNOWFLAKE.ACCOUNT_USAGE` schema is incredibly powerful for monitoring and analytics:
- Query performance analysis
- Cost tracking and optimization
- Storage management
- User activity monitoring
- Security and compliance auditing

### What's Next?

In **Lesson 6: Advanced Patterns**, you'll see production-ready techniques for building robust applications!
""")
