"""
Lesson 2: Session State
Master the art of persisting data across reruns
"""

import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Session State", page_icon="🔄", layout="wide")

st.title("🔄 Lesson 2: The Session State")

# =============================================================================
# SECTION 1: Why Session State?
# =============================================================================
st.header("1. Why We Need Session State")

st.markdown("""
Remember from Lesson 1: **Streamlit reruns your entire script on every interaction**. 
This means **variables are reset every time**!

Let's see the problem and the solution:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.write("**❌ Without Session State:**")
    st.code("""
# This counter resets on every rerun!
counter = 0

if st.button("Increment"):
    counter += 1

st.write(f"Counter: {counter}")
# Always shows 0!
    """, language="python")
    
    st.write("**✅ With Session State:**")
    st.code("""
# Initialize in session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")
# Persists across reruns!
    """, language="python")

with demo_col:
    st.write("**❌ Try the broken version first:**")
    
    # Broken example - regular variable
    broken_counter = 0
    
    if st.button("Increment Broken Counter", key="broken_inc"):
        broken_counter += 1
    
    st.metric("Broken Counter", broken_counter)
    st.error("Always 0! Resets every time.")
    
    st.write("---")
    st.write("**✅ Now try the working version:**")
    
    # Working example with session state
    if 'working_counter' not in st.session_state:
        st.session_state.working_counter = 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕", key="work_inc"):
            st.session_state.working_counter += 1
    with col2:
        if st.button("➖", key="work_dec"):
            st.session_state.working_counter -= 1
    with col3:
        if st.button("🔄", key="work_reset"):
            st.session_state.working_counter = 0
    
    st.metric("Working Counter", st.session_state.working_counter)
    st.success("✅ Persists! Try incrementing, then clicking the broken counter above.")

st.markdown("---")

# =============================================================================
# SECTION 2: Session State Basics
# =============================================================================
st.header("2. Session State Basics")

st.markdown("""
`st.session_state` is a dictionary-like object that persists data across reruns.
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Initialize (always check first!)
if 'name' not in st.session_state:
    st.session_state.name = "Guest"

# Read
st.write(st.session_state.name)

# Update
st.session_state.name = "Alice"

# Delete
del st.session_state.name

# Check if exists
if 'name' in st.session_state:
    st.write("Name exists!")
    """, language="python")

with demo_col:
    st.write("**Try changing your name:**")
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "Guest"
    
    new_name = st.text_input("Enter your name:", st.session_state.user_name, key="name_input")
    
    if st.button("Save Name", key="save_name"):
        st.session_state.user_name = new_name
        st.success(f"Saved! Hello, {st.session_state.user_name}")
    
    st.write(f"Current name in session: **{st.session_state.user_name}**")
    st.caption("💡 Change the name, click Save, then interact with other widgets - your name stays saved!")

st.markdown("---")

# =============================================================================
# SECTION 3: Widget Keys and Session State
# =============================================================================
st.header("3. Widget Keys and Automatic State")

st.markdown("""
When you give a widget a `key`, it automatically syncs with session state:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Widget with key - auto-synced!
age = st.slider("Age", 0, 100, key="user_age")

# Access anywhere via session state
st.write(f"Age from session: {st.session_state.user_age}")

# You can even set it programmatically
if st.button("Set to 30"):
    st.session_state.user_age = 30
    """, language="python")

with demo_col:
    st.write("**Try the slider and button:**")
    
    age = st.slider("Age", 0, 100, key="demo_age")
    
    st.write(f"Widget value: **{age}**")
    st.write(f"Session state value: **{st.session_state.demo_age}**")
    st.caption("They're always in sync!")
    
    if st.button("Set to 30", key="set_age"):
        st.session_state.demo_age = 30
        st.rerun()
    
    st.info("💡 Move the slider, then click the button to see programmatic control")

st.markdown("---")

# =============================================================================
# SECTION 4: Callbacks
# =============================================================================
st.header("4. Callbacks: Immediate Reactions")

st.markdown("""
Callbacks run **before** the main script, perfect for immediate reactions to widget changes:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Callback function
def on_slider_change():
    # Runs BEFORE the rest of the script
    st.session_state.doubled = st.session_state.my_slider * 2

# Widget with callback
st.slider("Value", 0, 10, 
          key="my_slider",
          on_change=on_slider_change)

# Use the computed value
st.write(f"Doubled: {st.session_state.doubled}")
    """, language="python")

with demo_col:
    st.write("**Move the slider and watch the callback:**")
    
    if 'doubled' not in st.session_state:
        st.session_state.doubled = 0
    
    def on_demo_slider_change():
        st.session_state.doubled = st.session_state.demo_slider * 2
    
    st.slider("Value", 0, 10, key="demo_slider", on_change=on_demo_slider_change)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Original", st.session_state.get('demo_slider', 0))
    with col2:
        st.metric("Doubled", st.session_state.doubled)
    
    st.caption("💡 The doubling happens immediately as you move the slider!")

st.markdown("---")

# =============================================================================
# SECTION 5: Forms
# =============================================================================
st.header("5. Forms: Batch Multiple Inputs")

st.markdown("""
Forms prevent reruns until you click submit. Great for multiple inputs!
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", 0, 120)
    email = st.text_input("Email")
    
    # Every form needs a submit button
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.success(f"Thanks {name}!")
        # Process form data here
    """, language="python")

with demo_col:
    st.write("**Fill out the form - notice no rerun until Submit:**")
    
    with st.form("demo_form"):
        name = st.text_input("Name", key="form_name")
        age = st.number_input("Age", 0, 120, value=25, key="form_age")
        email = st.text_input("Email", key="form_email")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.success(f"Thanks {name}!")
            st.write(f"Age: {age}, Email: {email}")
    
    st.caption("💡 Type in the fields above - the page doesn't rerun until you click Submit!")

st.caption("💡 Notice how the page doesn't rerun as you type in the form - only when you click Submit!")

st.markdown("---")

# =============================================================================
# SECTION 6: Multi-Step Workflows
# =============================================================================
st.header("6. Multi-Step Workflows")

st.markdown("""
Use session state to track progress through multi-step processes:
""")

# Initialize wizard
if 'wizard_step' not in st.session_state:
    st.session_state.wizard_step = 1
if 'wizard_data' not in st.session_state:
    st.session_state.wizard_data = {}

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Track current step
if 'step' not in st.session_state:
    st.session_state.step = 1

# Step 1
if st.session_state.step == 1:
    name = st.text_input("Name")
    if st.button("Next"):
        st.session_state.data = {'name': name}
        st.session_state.step = 2
        st.rerun()

# Step 2
elif st.session_state.step == 2:
    email = st.text_input("Email")
    if st.button("Submit"):
        st.session_state.data['email'] = email
        st.success("Complete!")
    """, language="python")

with demo_col:
    st.write("**Work through the wizard:**")
    st.progress(st.session_state.wizard_step / 3)
    st.write(f"**Step {st.session_state.wizard_step} of 3**")
    
    if st.session_state.wizard_step == 1:
        wizard_name = st.text_input("Your Name", key="wiz_name")
        if st.button("Next →", key="wiz_next1") and wizard_name:
            st.session_state.wizard_data['name'] = wizard_name
            st.session_state.wizard_step = 2
            st.rerun()
    
    elif st.session_state.wizard_step == 2:
        wizard_email = st.text_input("Your Email", key="wiz_email")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="wiz_back2"):
                st.session_state.wizard_step = 1
                st.rerun()
        with col2:
            if st.button("Next →", key="wiz_next2") and wizard_email:
                st.session_state.wizard_data['email'] = wizard_email
                st.session_state.wizard_step = 3
                st.rerun()
    
    else:  # Step 3
        st.write("**Review Your Info:**")
        st.write(f"Name: {st.session_state.wizard_data.get('name', 'N/A')}")
        st.write(f"Email: {st.session_state.wizard_data.get('email', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="wiz_back3"):
                st.session_state.wizard_step = 2
                st.rerun()
        with col2:
            if st.button("✅ Submit", key="wiz_submit"):
                st.balloons()
                st.success("Complete!")
                st.session_state.wizard_step = 1
                st.session_state.wizard_data = {}

st.markdown("---")

# =============================================================================
# SECTION 7: Toggle States
# =============================================================================
st.header("7. Toggle States")

st.markdown("""
Perfect for showing/hiding content:
""")

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Initialize
if 'show_details' not in st.session_state:
    st.session_state.show_details = False

# Toggle button
if st.button("Toggle Details"):
    st.session_state.show_details = not st.session_state.show_details

# Conditional display
if st.session_state.show_details:
    st.write("Here are the details!")
else:
    st.write("Details hidden")
    """, language="python")

with demo_col:
    st.write("**Click the button to toggle:**")
    
    if 'show_demo_details' not in st.session_state:
        st.session_state.show_demo_details = False
    
    if st.button("Toggle Details", key="toggle_demo"):
        st.session_state.show_demo_details = not st.session_state.show_demo_details
    
    if st.session_state.show_demo_details:
        st.info("🎉 Here are the details you wanted to see!")
        st.write("This content toggles on and off.")
    else:
        st.warning("Details are hidden. Click the button to reveal them!")
    
    st.caption("💡 The button remembers whether details are shown or hidden")

st.markdown("---")

# =============================================================================
# SECTION 8: Complete Example - Todo List
# =============================================================================
st.header("8. Complete Example: Todo List")

st.markdown("A practical example using everything we've learned:")

# Initialize
if 'todos' not in st.session_state:
    st.session_state.todos = []

code_col, demo_col = st.columns([1, 1])

with code_col:
    st.code("""
# Initialize
if 'todos' not in st.session_state:
    st.session_state.todos = []

# Add new todo
with st.form("add_todo", clear_on_submit=True):
    new_todo = st.text_input("New task")
    if st.form_submit_button("Add"):
        st.session_state.todos.append({
            'task': new_todo,
            'done': False
        })
        st.rerun()

# Display todos
for i, todo in enumerate(st.session_state.todos):
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col1:
        done = st.checkbox("", todo['done'], 
                          key=f"todo_{i}")
    with col2:
        text = todo['task']
        if done:
            st.markdown(f"~~{text}~~")
        else:
            st.write(text)
    with col3:
        if st.button("🗑️", key=f"del_{i}"):
            st.session_state.todos.pop(i)
            st.rerun()
    """, language="python")

with demo_col:
    # Add new todo
    with st.form("demo_add_todo", clear_on_submit=True):
        new_todo = st.text_input("Add a new task", key="new_todo_input")
        submitted = st.form_submit_button("➕ Add")
        if submitted and new_todo:
            st.session_state.todos.append({
                'task': new_todo,
                'done': False,
                'id': len(st.session_state.todos)
            })
            st.rerun()
    
    # Display todos
    if st.session_state.todos:
        for i, todo in enumerate(st.session_state.todos):
            col1, col2, col3 = st.columns([0.5, 3, 0.5])
            
            with col1:
                done = st.checkbox("", value=todo['done'], key=f"demo_todo_done_{i}")
                if done != todo['done']:
                    st.session_state.todos[i]['done'] = done
                    st.rerun()
            
            with col2:
                if todo['done']:
                    st.markdown(f"~~{todo['task']}~~")
                else:
                    st.write(todo['task'])
            
            with col3:
                if st.button("🗑️", key=f"demo_delete_{i}"):
                    st.session_state.todos.pop(i)
                    st.rerun()
    else:
        st.info("No tasks yet! Add one above.")

st.markdown("---")

# =============================================================================
# SECTION 9: Debugging Session State
# =============================================================================
st.header("9. Debugging Session State")

st.markdown("""
Want to see everything in your session state? Here's a useful pattern:
""")

with st.expander("🔧 View All Session State"):
    st.json(dict(st.session_state))

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
1. **st.session_state** persists data across reruns
2. **Always check** if a key exists before using it: `if 'key' not in st.session_state:`
3. **Widget keys** automatically sync widget values to session state
4. **Callbacks** run before the main script - great for immediate reactions
5. **Forms** batch multiple inputs and prevent reruns until submit
6. **st.rerun()** manually triggers a rerun when needed
7. **Session state is per-user** - each user has their own separate state

### What's Next?

In **Lesson 3: Caching**, you'll learn how to make your app blazing fast by caching expensive operations!
""")
