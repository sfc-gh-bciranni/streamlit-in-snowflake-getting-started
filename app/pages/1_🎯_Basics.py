"""
Lesson 1: Streamlit Basics
Understanding how Streamlit works and exploring basic widgets
"""

import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(page_title="Basics", page_icon="🎯", layout="wide")

st.title("🎯 Lesson 1: Streamlit Basics")

# =============================================================================
# SECTION 1: How Streamlit Works
# =============================================================================
st.header("1. How Streamlit Works: The Rerun Model")

st.markdown("""
### 🔄 The Key Concept: Everything Reruns

Unlike traditional web frameworks, Streamlit has a unique execution model:

- **The entire script runs from top to bottom** every time a user interacts with a widget
- Each interaction (button click, slider move, text input) triggers a **rerun**
- There's no separate "event handler" code - it's all linear!
""")

# Live demonstration of reruns
st.subheader("See It In Action")

col1, col2 = st.columns([1, 1])

with col1:
    st.write("**The Code:**")
    st.code("""
# Show current time to prove rerun
st.write("Execution time:", 
         time.strftime("%H:%M:%S"))

# Track reruns
if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1
st.info(f"Executed {st.session_state.counter} times")

if st.button("Trigger Rerun"):
    st.success("Button clicked!")
    """, language="python")

with col2:
    st.write("**The Result - Click the button!**")
    st.write("Execution time:", time.strftime("%H:%M:%S"))
    
    if 'rerun_counter' not in st.session_state:
        st.session_state.rerun_counter = 0
    
    st.session_state.rerun_counter += 1
    st.info(f"📊 Executed **{st.session_state.rerun_counter}** times")
    
    if st.button("Trigger Rerun"):
        st.success("Button clicked! Notice the count increased?")
    
    st.caption("💡 Click the button and watch the execution count increase!")

st.markdown("---")

# =============================================================================
# SECTION 2: Text Input Widgets
# =============================================================================
st.header("2. Text Input Widgets")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Simple text input
name = st.text_input("Your Name", "John")
st.write(f"Hello, {name}!")

# Multi-line text
bio = st.text_area("About You", 
                   "Tell us about yourself")

# Password input
password = st.text_input("Password", 
                         type="password")

# Number input
age = st.number_input("Age", 
                      min_value=0, 
                      max_value=120, 
                      value=25)
    """, language="python")

with demo_col:
    st.write("**Try each input:**")
    
    name = st.text_input("Your Name", "John", key="name1")
    st.write(f"Hello, {name}!")
    
    bio = st.text_area("About You", "Tell us about yourself", key="bio1")
    
    password = st.text_input("Password", type="password", key="pass1")
    if password:
        st.write(f"Password length: {len(password)}")
    
    age = st.number_input("Age", min_value=0, max_value=120, value=25, key="age1")
    st.write(f"In 5 years: {age + 5}")
    
    st.caption("💡 Type in the inputs and see the results update immediately!")

st.markdown("---")

# =============================================================================
# SECTION 3: Selection Widgets
# =============================================================================
st.header("3. Selection Widgets")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Dropdown selection
color = st.selectbox("Favorite Color", 
                     ["Red", "Blue", "Green"])

# Multiple selection
interests = st.multiselect("Interests",
                          ["Sports", "Music", "Art"],
                          default=["Music"])

# Radio buttons
size = st.radio("T-Shirt Size", 
                ["Small", "Medium", "Large"])

# Checkbox
agree = st.checkbox("I agree to terms")

# Slider
volume = st.slider("Volume", 0, 100, 50)
    """, language="python")

with demo_col:
    st.write("**Try each selection widget:**")
    
    color = st.selectbox("Favorite Color", ["Red", "Blue", "Green"], key="color1")
    st.write(f"You chose: {color}")
    
    interests = st.multiselect("Interests", ["Sports", "Music", "Art"], 
                               default=["Music"], key="interests1")
    st.write(f"Selected {len(interests)} interests")
    
    size = st.radio("T-Shirt Size", ["Small", "Medium", "Large"], key="size1")
    st.write(f"Size: {size}")
    
    agree = st.checkbox("I agree to terms", key="agree1")
    if agree:
        st.success("✅ Thank you!")
    
    volume = st.slider("Volume", 0, 100, 50, key="vol1")
    st.write(f"Volume: {volume}%")
    
    st.caption("💡 Change the selections and see results update instantly!")

st.markdown("---")

# =============================================================================
# SECTION 4: Buttons and Actions
# =============================================================================
st.header("4. Buttons and Actions")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Simple button
if st.button("Click Me"):
    st.success("Button was clicked!")

# File uploader
uploaded_file = st.file_uploader("Upload CSV")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

# Date and time
date = st.date_input("Select Date")
time_val = st.time_input("Select Time")
    """, language="python")

with demo_col:
    st.write("**Try these interactive widgets:**")
    
    if st.button("Click Me", key="btn1"):
        st.success("Button was clicked!")
        st.info("⚠️ But this message disappears on next interaction")
    
    uploaded_file = st.file_uploader("Upload CSV", key="file1")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
        except:
            st.error("Error reading file")
    
    date = st.date_input("Select Date", key="date1")
    time_val = st.time_input("Select Time", key="time1")
    
    st.caption("💡 Click the button, then change the date to see button state disappear!")

st.markdown("---")

# =============================================================================
# SECTION 5: Displaying Content
# =============================================================================
st.header("5. Displaying Content")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Text display
st.write("Universal display method")
st.markdown("**Bold** and *italic*")
st.caption("Small caption text")

# Status messages
st.success("Success message")
st.info("Information")
st.warning("Warning")
st.error("Error message")

# Metrics
st.metric("Revenue", "$1,234", "+12%")
    """, language="python")

with demo_col:
    st.write("Universal display method")
    st.markdown("**Bold** and *italic*")
    st.caption("Small caption text")
    
    st.success("Success message")
    st.info("Information")
    st.warning("Warning")
    st.error("Error message")
    
    st.metric("Revenue", "$1,234", "+12%")

st.markdown("---")

# =============================================================================
# SECTION 6: Data Display
# =============================================================================
st.header("6. Data Display")

# Create sample data
sample_df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
})

# Interactive dataframe
st.dataframe(df)

# Static table
st.table(df)

# JSON
st.json({"key": "value", "count": 42})
    """, language="python")

with demo_col:
    st.write("**Interactive DataFrame:**")
    st.dataframe(sample_df, use_container_width=True)
    
    st.write("**Static Table:**")
    st.table(sample_df)

st.markdown("---")

# =============================================================================
# SECTION 7: Charts
# =============================================================================
st.header("7. Simple Charts")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Create sample data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# Built-in charts
st.line_chart(chart_data)
st.area_chart(chart_data)
st.bar_chart(chart_data['A'])
    """, language="python")

with demo_col:
    st.write("**Line Chart:**")
    st.line_chart(chart_data)
    
    st.write("**Area Chart:**")
    st.area_chart(chart_data)
    
    st.write("**Bar Chart:**")
    st.bar_chart(chart_data[['A']])

st.markdown("---")

# =============================================================================
# SECTION 8: Complete Example
# =============================================================================
st.header("8. Complete Example: Simple Calculator")

st.markdown("Here's a complete mini-app putting it all together:")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Get inputs
num1 = st.number_input("First Number", 
                       value=10.0)
num2 = st.number_input("Second Number", 
                       value=5.0)
operation = st.selectbox("Operation", 
                        ["Add", "Subtract", 
                         "Multiply", "Divide"])

# Calculate
if operation == "Add":
    result = num1 + num2
elif operation == "Subtract":
    result = num1 - num2
elif operation == "Multiply":
    result = num1 * num2
else:
    result = num1 / num2 if num2 != 0 else "Error"

# Display
st.success(f"Result: {result}")
    """, language="python")

with demo_col:
    st.write("**Try the calculator:**")
    
    num1 = st.number_input("First Number", value=10.0, key="calc_num1")
    num2 = st.number_input("Second Number", value=5.0, key="calc_num2")
    operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"], key="calc_op")
    
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    else:
        result = num1 / num2 if num2 != 0 else "Error"
    
    st.success(f"Result: {result}")
    
    st.caption("💡 Change the numbers or operation - result updates automatically!")

st.markdown("---")

# =============================================================================
# SECTION 9: Important Note About Buttons
# =============================================================================
st.header("9. ⚠️ Important: Button State")

st.markdown("""
**A common gotcha:** Button state only lasts for one rerun!

A button returns `True` only during the rerun when it was clicked. On the next rerun, it returns `False`.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# This won't work as expected
if st.button("Click Me"):
    st.success("Clicked!")
    # This disappears if you click anything else

# Solution: Use session state (Lesson 2!)
if st.button("Better Way"):
    st.session_state.clicked = True

if 'clicked' in st.session_state:
    st.success("This persists!")
    """, language="python")

with demo_col:
    st.write("**See the button gotcha:**")
    
    if st.button("Click Me", key="btn_demo1"):
        st.success("Clicked!")
        st.warning("Now move the slider below ⬇️")
    
    slider_val = st.slider("Move me", 0, 10, 5, key="slider_demo")
    st.caption("💡 Click the button, then move the slider - the success message disappears!")

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
1. **Streamlit runs from top to bottom** on every interaction
2. **Every widget interaction triggers a rerun** of the entire script
3. **Widgets return values directly** - no need for complex state management (yet!)
4. **Button states don't persist** - they only return `True` during the rerun when clicked
5. **st.write() is magic** - it can display almost anything intelligently
6. **Start simple** - Streamlit makes it easy to build interactive apps quickly!

### What's Next?

In **Lesson 2: Session State**, you'll learn how to persist data across reruns and build more complex interactive applications.
""")
