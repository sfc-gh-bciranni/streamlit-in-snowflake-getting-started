"""
Lesson 6: Advanced Patterns
Production-ready techniques for building robust applications
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

st.set_page_config(page_title="Advanced Patterns", page_icon="🚀", layout="wide")

st.title("🚀 Lesson 6: Advanced Patterns")

st.markdown("""
These patterns will help you build production-quality Streamlit applications.
""")

st.markdown("---")

# =============================================================================
# PATTERN 1: Dependent Dropdowns with Callbacks
# =============================================================================
st.header("1. Dependent Dropdowns")

st.markdown("""
A common pattern: one dropdown's options depend on another's selection.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Data structure
categories = {
    'Electronics': ['Laptop', 'Phone'],
    'Clothing': ['Shirt', 'Pants'],
    'Food': ['Pizza', 'Burger']
}

# Callback to reset item when category changes
def on_category_change():
    st.session_state.selected_item = None
    st.session_state.items = categories[
        st.session_state.category
    ]

# Category dropdown with callback
category = st.selectbox(
    "Category",
    options=list(categories.keys()),
    key='category',
    on_change=on_category_change
)

# Item dropdown (options update automatically)
item = st.selectbox(
    "Item",
    options=st.session_state.items,
    key='selected_item'
)
    """, language="python")

with demo_col:
    st.write("**Try selecting different categories:**")
    
    # Initialize
    if 'demo_category' not in st.session_state:
        st.session_state.demo_category = 'Electronics'
    if 'demo_selected_item' not in st.session_state:
        st.session_state.demo_selected_item = None
    
    # Data
    demo_categories = {
        'Electronics': ['Laptop', 'Phone', 'Tablet'],
        'Clothing': ['Shirt', 'Pants', 'Shoes'],
        'Food': ['Pizza', 'Burger', 'Salad']
    }
    
    def on_demo_category_change():
        st.session_state.demo_selected_item = None
        st.session_state.demo_items = demo_categories[st.session_state.demo_category]
    
    # Category dropdown
    category = st.selectbox(
        "Select Category",
        options=list(demo_categories.keys()),
        key='demo_category',
        on_change=on_demo_category_change
    )
    
    # Item dropdown
    if 'demo_items' not in st.session_state:
        st.session_state.demo_items = demo_categories[category]
    
    item = st.selectbox(
        "Select Item",
        options=st.session_state.demo_items,
        key='demo_selected_item'
    )
    
    st.success(f"Selected: {category} → {item if item else 'None'}")
    st.caption("💡 Change category - the items update automatically!")

st.markdown("---")

# =============================================================================
# PATTERN 2: Multi-Step Forms
# =============================================================================
st.header("2. Multi-Step Forms")

st.markdown("""
Guide users through a process step-by-step, perfect for data collection or configuration.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Track current step
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.data = {}

# Step 1: Basic Info
if st.session_state.step == 1:
    name = st.text_input("Name")
    if st.button("Next"):
        st.session_state.data['name'] = name
        st.session_state.step = 2
        st.rerun()

# Step 2: Details
elif st.session_state.step == 2:
    email = st.text_input("Email")
    if st.button("Back"):
        st.session_state.step = 1
        st.rerun()
    if st.button("Submit"):
        st.session_state.data['email'] = email
        st.success("Complete!")
    """, language="python")

with demo_col:
    st.write("**Walk through the form:**")
    
    # Initialize
    if 'form_step' not in st.session_state:
        st.session_state.form_step = 1
        st.session_state.form_data = {}
    
    # Progress indicator
    st.progress(st.session_state.form_step / 3)
    st.write(f"Step {st.session_state.form_step} of 3")
    
    if st.session_state.form_step == 1:
        name = st.text_input("Your Name", key="step1_name")
        if st.button("Next →", key="form_next1") and name:
            st.session_state.form_data['name'] = name
            st.session_state.form_step = 2
            st.rerun()
    
    elif st.session_state.form_step == 2:
        email = st.text_input("Your Email", key="step2_email")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="form_back2"):
                st.session_state.form_step = 1
                st.rerun()
        with col2:
            if st.button("Next →", key="form_next2") and email:
                st.session_state.form_data['email'] = email
                st.session_state.form_step = 3
                st.rerun()
    
    else:  # Step 3
        st.write("**Review:**")
        st.write(f"Name: {st.session_state.form_data.get('name', 'N/A')}")
        st.write(f"Email: {st.session_state.form_data.get('email', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="form_back3"):
                st.session_state.form_step = 2
                st.rerun()
        with col2:
            if st.button("✅ Submit", key="form_submit"):
                st.balloons()
                st.success("Form submitted!")
                # Reset
                st.session_state.form_step = 1
                st.session_state.form_data = {}

st.markdown("---")

# =============================================================================
# PATTERN 3: Progress Tracking
# =============================================================================
st.header("3. Progress Tracking for Long Operations")

st.markdown("""
Show users progress when processing large datasets or running long operations.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
if st.button("Process 100 Items"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        # Process item
        process_item(i)
        
        # Update UI
        progress = (i + 1) / 100
        progress_bar.progress(progress)
        status_text.text(f"Processing {i+1}/100")
        
    status_text.success("Complete!")
    """, language="python")

with demo_col:
    st.write("**See progress tracking in action:**")
    
    if st.button("Process 100 Items", key="progress_btn"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        result_text = st.empty()
        
        for i in range(100):
            # Simulate processing
            time.sleep(0.02)
            
            # Update progress
            progress = (i + 1) / 100
            progress_bar.progress(progress)
            status_text.text(f"Processing item {i+1}/100...")
            
            # Show interim results
            if (i + 1) % 20 == 0:
                result_text.info(f"✅ Completed {i+1} items")
        
        status_text.success("✅ All 100 items processed!")
        result_text.empty()

st.markdown("---")

# =============================================================================
# PATTERN 4: Data Validation
# =============================================================================
st.header("4. Input Validation")

st.markdown("""
Validate user input before processing to ensure data quality.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
with st.form("validated_form"):
    email = st.text_input("Email")
    age = st.number_input("Age", 0, 150)
    password = st.text_input("Password", type="password")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        errors = []
        
        # Validate email
        if '@' not in email:
            errors.append("Invalid email")
        
        # Validate age
        if age < 18:
            errors.append("Must be 18+")
        
        # Validate password
        if len(password) < 8:
            errors.append("Password must be 8+ chars")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.success("Valid!")
    """, language="python")

with demo_col:
    st.write("**Try submitting with invalid data:**")
    
    with st.form("validation_form"):
        val_email = st.text_input("Email", key="val_email")
        val_age = st.number_input("Age", 0, 150, value=25, key="val_age")
        val_password = st.text_input("Password", type="password", key="val_password")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            errors = []
            
            if not val_email or '@' not in val_email:
                errors.append("❌ Invalid email address")
            
            if val_age < 18:
                errors.append("❌ Must be 18 or older")
            
            if len(val_password) < 8:
                errors.append("❌ Password must be at least 8 characters")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.success("✅ All inputs valid!")
                st.balloons()

st.markdown("---")

# =============================================================================
# PATTERN 5: Pagination
# =============================================================================
st.header("5. Pagination for Large Datasets")

st.markdown("""
Display large datasets efficiently by showing one page at a time.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Generate large dataset
if 'data' not in st.session_state:
    st.session_state.data = generate_large_dataset()

# Pagination state
if 'page' not in st.session_state:
    st.session_state.page = 0

rows_per_page = 25
total_pages = len(st.session_state.data) // rows_per_page

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("◀ Prev"):
        st.session_state.page = max(0, st.session_state.page - 1)
with col2:
    st.write(f"Page {st.session_state.page + 1} of {total_pages}")
with col3:
    if st.button("Next ▶"):
        st.session_state.page = min(total_pages - 1, st.session_state.page + 1)

# Display current page
start = st.session_state.page * rows_per_page
end = start + rows_per_page
st.dataframe(st.session_state.data[start:end])
    """, language="python")

with demo_col:
    st.write("**Navigate through 500 rows:**")
    
    # Generate data
    if 'pagination_data' not in st.session_state:
        st.session_state.pagination_data = pd.DataFrame({
            'ID': range(1, 501),
            'Name': [f'Item {i}' for i in range(1, 501)],
            'Value': np.random.randint(1, 100, 500),
            'Category': np.random.choice(['A', 'B', 'C'], 500)
        })
    
    if 'pagination_page' not in st.session_state:
        st.session_state.pagination_page = 0
    
    rows_per_page = 25
    total_pages = len(st.session_state.pagination_data) // rows_per_page
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.button("⏮️", key="page_first"):
            st.session_state.pagination_page = 0
            st.rerun()
    
    with col2:
        if st.button("◀", key="page_prev"):
            st.session_state.pagination_page = max(0, st.session_state.pagination_page - 1)
            st.rerun()
    
    with col3:
        st.write(f"Page {st.session_state.pagination_page + 1} of {total_pages}")
    
    with col4:
        if st.button("▶", key="page_next"):
            st.session_state.pagination_page = min(total_pages - 1, st.session_state.pagination_page + 1)
            st.rerun()
    
    with col5:
        if st.button("⏭️", key="page_last"):
            st.session_state.pagination_page = total_pages - 1
            st.rerun()
    
    # Display page
    start = st.session_state.pagination_page * rows_per_page
    end = start + rows_per_page
    st.dataframe(st.session_state.pagination_data.iloc[start:end], use_container_width=True)
    st.caption("💡 Navigate through pages - only 25 rows displayed at a time")

st.markdown("---")

# =============================================================================
# PATTERN 6: Error Handling
# =============================================================================
st.header("6. Robust Error Handling")

st.markdown("""
Handle errors gracefully and provide helpful feedback to users.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
def safe_operation(data):
    try:
        result = process_data(data)
        return result, None
    except ValueError as e:
        return None, f"Invalid data: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"

# Use it
result, error = safe_operation(user_input)

if error:
    st.error(error)
    st.info("Please check your input and try again")
else:
    st.success("Operation successful!")
    st.dataframe(result)
    """, language="python")

with demo_col:
    st.write("**Select different operations:**")
    
    operations = {
        "Valid Operation": lambda: 10 / 2,
        "Division by Zero": lambda: 10 / 0,
        "Type Error": lambda: "text" + 5,
        "Index Error": lambda: [1, 2, 3][10]
    }
    
    operation = st.selectbox("Choose Operation", list(operations.keys()), key="error_op")
    
    if st.button("Execute", key="error_btn"):
        try:
            result = operations[operation]()
            st.success(f"✅ Result: {result}")
        except ZeroDivisionError:
            st.error("❌ Cannot divide by zero!")
            st.info("💡 Check your denominator")
        except TypeError as e:
            st.error(f"❌ Type error: {e}")
            st.info("💡 Ensure compatible types")
        except IndexError:
            st.error("❌ Index out of range!")
            st.info("💡 Check your indices")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

st.markdown("---")

# =============================================================================
# PATTERN 7: Async Query Execution
# =============================================================================
st.header("7. Async Query Execution")

st.markdown("""
Run long-running Snowflake queries asynchronously to keep your UI responsive. 
Perfect for analytics workloads, logging operations, and database writebacks!
""")

from utils.auth import get_snowflake_session
session = get_snowflake_session()

st.subheader("📊 Basic Async Query")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
from snowflake.snowpark import Session

# Start query asynchronously
df = session.sql('''
    SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
    WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP())
''')

# Execute without blocking
async_job = df.collect_nowait()

# Check status while waiting
while not async_job.is_done():
    st.write(f"Status: {async_job.status()}")
    time.sleep(0.5)

# Get results when ready
if async_job.is_done():
    results = async_job.result()
    st.dataframe(results)
    """, language="python")

with demo_col:
    st.write("**Run a query asynchronously:**")
    
    if st.button("Start Async Query", key="async_basic"):
        try:
            with st.spinner("Starting async query..."):
                # Query recent queries
                df = session.sql("""
                    SELECT 
                        QUERY_TYPE,
                        USER_NAME,
                        EXECUTION_STATUS,
                        ROUND(TOTAL_ELAPSED_TIME/1000, 2) as SECONDS
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                    WHERE START_TIME >= DATEADD(day, -1, CURRENT_TIMESTAMP())
                    LIMIT 100
                """)
                
                # Execute asynchronously
                async_job = df.collect_nowait()
                
                # Create status placeholder
                status_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                # Poll for status
                iterations = 0
                max_iterations = 20
                while not async_job.is_done() and iterations < max_iterations:
                    status_placeholder.info(f"📊 Query Status: {async_job.status()}")
                    progress_bar.progress((iterations + 1) / max_iterations)
                    time.sleep(0.3)
                    iterations += 1
                
                # Get results
                if async_job.is_done():
                    results = async_job.result()
                    status_placeholder.success(f"✅ Query completed! Query ID: {async_job.query_id}")
                    progress_bar.progress(100)
                    
                    # Convert to pandas for display
                    df_results = pd.DataFrame(results)
                    st.dataframe(df_results.head(20), use_container_width=True)
                    st.caption(f"Returned {len(df_results)} rows")
                    
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

st.subheader("🚀 Multiple Parallel Queries")

st.markdown("""
Run multiple queries in parallel for maximum efficiency - like querying different time periods simultaneously!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Start multiple queries in parallel
jobs = []

# Query 1: Today's data
df1 = session.sql("SELECT ... WHERE date = CURRENT_DATE()")
jobs.append(df1.collect_nowait())

# Query 2: Last week's data  
df2 = session.sql("SELECT ... WHERE date >= DATEADD(day, -7, CURRENT_DATE())")
jobs.append(df2.collect_nowait())

# Query 3: Last month's data
df3 = session.sql("SELECT ... WHERE date >= DATEADD(day, -30, CURRENT_DATE())")
jobs.append(df3.collect_nowait())

# Wait for all to complete
results = []
for job in jobs:
    while not job.is_done():
        time.sleep(0.5)
    results.append(job.result())

# All queries done!
st.success(f"Completed {len(results)} queries in parallel")
    """, language="python")

with demo_col:
    st.write("**Run multiple queries at once:**")
    
    if st.button("Start Parallel Queries", key="async_parallel"):
        try:
            with st.spinner("Starting parallel queries..."):
                jobs = []
                query_names = []
                
                # Query 1: Queries in last 1 day
                q1 = session.sql("""
                    SELECT COUNT(*) as COUNT, 'Last 1 Day' as PERIOD
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                    WHERE START_TIME >= DATEADD(day, -1, CURRENT_TIMESTAMP())
                """)
                jobs.append(q1.to_pandas(block=False))
                query_names.append("Last 1 Day")
                
                # Query 2: Queries in last 7 days
                q2 = session.sql("""
                    SELECT COUNT(*) as COUNT, 'Last 7 Days' as PERIOD
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                    WHERE START_TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
                """)
                jobs.append(q2.to_pandas(block=False))
                query_names.append("Last 7 Days")
                
                # Query 3: Queries in last 30 days
                q3 = session.sql("""
                    SELECT COUNT(*) as COUNT, 'Last 30 Days' as PERIOD
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                    WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
                """)
                jobs.append(q3.to_pandas(block=False))
                query_names.append("Last 30 Days")
                
                st.info(f"🚀 Started {len(jobs)} queries in parallel")
                
                # Track progress
                progress_cols = st.columns(len(jobs))
                status_placeholders = [col.empty() for col in progress_cols]
                
                # Poll all jobs
                completed = [False] * len(jobs)
                while not all(completed):
                    for i, job in enumerate(jobs):
                        if not completed[i]:
                            if job.is_done():
                                completed[i] = True
                                status_placeholders[i].success(f"✅ {query_names[i]}")
                            else:
                                status_placeholders[i].info(f"⏳ {query_names[i]}")
                    time.sleep(0.3)
                
                # Collect results
                st.success("🎉 All queries completed!")
                results_data = []
                for i, job in enumerate(jobs):
                    result = job.result()
                    results_data.append({
                        'Period': query_names[i],
                        'Query Count': int(result['COUNT'][0])
                    })
                
                results_df = pd.DataFrame(results_data)
                st.dataframe(results_df, use_container_width=True)
                
                # Show chart
                import plotly.express as px
                fig = px.bar(results_df, x='Period', y='Query Count',
                           title='Query Volume by Time Period')
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

st.subheader("💾 Async Database Writebacks")

st.markdown("""
Write data to Snowflake asynchronously - perfect for logging, audit trails, or background data updates!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Create data to write
log_data = pd.DataFrame({
    'timestamp': [datetime.now()],
    'user': ['current_user'],
    'action': ['button_click'],
    'value': [42]
})

# Set database context (required for temp operations)
session.sql('USE DATABASE MY_DATABASE').collect()
session.sql('USE SCHEMA MY_SCHEMA').collect()

# Write asynchronously (non-blocking)
df = session.create_dataframe(log_data)
async_job = df.write.save_as_table(
    "MY_DATABASE.MY_SCHEMA.MY_LOG_TABLE",
    mode="append",
    block=False  # Don't wait!
)

# UI stays responsive
st.success("Write started in background!")

# Check status later
if async_job.is_done():
    st.success("✅ Data written successfully")
else:
    st.info("⏳ Still writing...")
    """, language="python")

with demo_col:
    st.write("**Async write to Snowflake:**")
    
    # Get available databases and schemas
    try:
        # Defaults
        default_db = 'DEMO'
        default_schema = 'PUBLIC'
        
        dbs = session.sql("SHOW DATABASES").collect()
        db_names = [row['name'] for row in dbs if row['name'] not in ['SNOWFLAKE', 'SNOWFLAKE_SAMPLE_DATA']]
        
        if db_names:
            # Set default index
            default_db_idx = db_names.index(default_db) if default_db in db_names else 0
            
            selected_db = st.selectbox("Select Database", db_names, index=default_db_idx, key="async_db")
            
            schemas = session.sql(f"SHOW SCHEMAS IN DATABASE {selected_db}").collect()
            schema_names = [row['name'] for row in schemas if row['name'] != 'INFORMATION_SCHEMA']
            
            if schema_names:
                # Set default schema index
                default_schema_idx = schema_names.index(default_schema) if default_schema in schema_names else 0
                
                selected_schema = st.selectbox("Select Schema", schema_names, index=default_schema_idx, key="async_schema")
                
                if st.button("Create Sample Log Table (Async)", key="async_write"):
                    try:
                        # Set database context first
                        session.sql(f'USE DATABASE {selected_db}').collect()
                        session.sql(f'USE SCHEMA {selected_schema}').collect()
                        
                        # Create sample data
                        log_data = pd.DataFrame({
                            'LOG_TIMESTAMP': [pd.Timestamp.now()],
                            'USER_NAME': ['STREAMLIT_USER'],
                            'ACTION': ['ASYNC_WRITE_TEST'],
                            'VALUE': [np.random.randint(1, 100)]
                        })
                        
                        table_name = f"{selected_db}.{selected_schema}.STREAMLIT_ASYNC_LOG"
                        
                        with st.spinner("Starting async write..."):
                            # Create dataframe
                            df = session.create_dataframe(log_data)
                            
                            # Write asynchronously
                            async_job = df.write.save_as_table(
                                table_name,
                                mode="overwrite",
                                table_type="temporary",
                                block=False  # Non-blocking!
                            )
                            
                            st.info(f"⏳ Write started! Query ID: {async_job.query_id}")
                            st.caption("UI remains responsive while writing...")
                            
                            # Track progress
                            progress_placeholder = st.empty()
                            iterations = 0
                            while not async_job.is_done() and iterations < 10:
                                progress_placeholder.info(f"Status: {async_job.status()}")
                                time.sleep(0.5)
                                iterations += 1
                            
                            if async_job.is_done():
                                if async_job.is_failed():
                                    st.error("❌ Write failed")
                                else:
                                    result = async_job.result()
                                    progress_placeholder.success(f"✅ Data written successfully to {table_name}")
                                    
                                    # Verify by reading back
                                    verify_df = session.table(table_name).to_pandas()
                                    st.write("**Verification - Data written:**")
                                    st.dataframe(verify_df, use_container_width=True)
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("No writable schemas found")
        else:
            st.warning("No writable databases found")
            
    except Exception as e:
        st.warning(f"Note: {e}")

st.markdown("---")

st.subheader("📊 Query Status Monitoring")

st.markdown("""
Monitor long-running queries in real-time and cancel if needed!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Start a long query
df = session.sql("SELECT SYSTEM$WAIT(10)")
async_job = df.collect_nowait()

# Monitor with status checks
status_placeholder = st.empty()

while not async_job.is_done():
    status = async_job.status()
    status_placeholder.info(f"Status: {status}")
    
    # Option to cancel
    if st.button("Cancel Query"):
        async_job.cancel()
        st.warning("Query cancelled!")
        break
    
    time.sleep(1)

# Check if succeeded or failed
if async_job.is_done():
    if async_job.is_failed():
        st.error("Query failed!")
    else:
        st.success("Query completed!")
        results = async_job.result()
    """, language="python")

with demo_col:
    st.write("**Monitor and control query execution:**")
    
    if 'monitoring_job' not in st.session_state:
        st.session_state.monitoring_job = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Long Query", key="start_long"):
            try:
                # Start a query that takes a few seconds
                df = session.sql("""
                    SELECT 
                        COUNT(*) as TOTAL_QUERIES,
                        COUNT(DISTINCT USER_NAME) as UNIQUE_USERS,
                        ROUND(AVG(TOTAL_ELAPSED_TIME)/1000, 2) as AVG_TIME
                    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
                    WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
                """)
                async_job = df.to_pandas(block=False)
                st.session_state.monitoring_job = async_job
                st.info("✅ Query started!")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("Cancel Query", key="cancel_query"):
            if st.session_state.monitoring_job:
                try:
                    st.session_state.monitoring_job.cancel()
                    st.warning("❌ Query cancelled!")
                    st.session_state.monitoring_job = None
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # Show status
    if st.session_state.monitoring_job:
        job = st.session_state.monitoring_job
        
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.metric("Status", job.status())
        with status_col2:
            st.metric("Done?", "Yes" if job.is_done() else "No")
        with status_col3:
            st.metric("Failed?", "Yes" if job.is_failed() else "No")
        
        if job.is_done() and not job.is_failed():
            st.success("✅ Query completed!")
            try:
                result = job.result()
                st.dataframe(result, use_container_width=True)
                st.session_state.monitoring_job = None
            except Exception as e:
                st.error(f"Error getting results: {e}")

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
### Production-Ready Patterns:

1. **Dependent Dropdowns** - Use callbacks to update options dynamically
2. **Multi-Step Forms** - Guide users through complex processes
3. **Progress Tracking** - Show progress for long operations
4. **Input Validation** - Validate before processing
5. **Pagination** - Handle large datasets efficiently
6. **Error Handling** - Catch and explain errors gracefully
7. **Async Query Execution** - Run queries without blocking the UI

### Async Query Benefits:

✅ **Performance:**
- UI stays responsive during long queries
- Run multiple queries in parallel
- Better user experience for analytics workloads

✅ **Use Cases:**
- Background data processing
- Audit logging and writebacks
- Long-running aggregations
- Real-time query monitoring

✅ **Key Methods:**
- `.collect_nowait()` - Execute query asynchronously
- `.to_pandas(block=False)` - Get pandas DataFrame async
- `.is_done()` - Check if query completed
- `.is_failed()` - Check if query failed
- `.cancel()` - Cancel running query
- `block=False` - For write operations

### Best Practices:

✅ **Always:**
- Validate user inputs
- Provide clear error messages
- Show progress for long operations
- Handle edge cases
- Test with real data

✅ **Consider:**
- User experience flow
- Mobile responsiveness
- Performance with large data
- Error recovery paths
- Accessibility

### Building Production Apps:

These patterns form the foundation of robust, user-friendly Streamlit applications. 
Combine them with caching (Lesson 3) and Snowflake integration (Lesson 5) for powerful data applications.

### What's Next?

Check out **Lesson 7: AI with Cortex** to learn how to use Snowflake's powerful AI capabilities, or jump to **Lesson 8: Quick Reference** for a handy cheat sheet of all Streamlit commands!
""")
