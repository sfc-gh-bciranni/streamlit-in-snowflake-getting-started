# 🎓 Streamlit Learning Hub

A comprehensive, interactive tutorial application designed to teach Streamlit from the ground up, with special emphasis on Streamlit-in-Snowflake deployment.

## 📚 What You'll Learn

This application provides a complete learning path covering:

1. **🎯 Basics** - Understanding how Streamlit works and basic widgets
2. **🔄 Session State** - Managing state across reruns
3. **⚡ Caching** - Making your app fast with proper caching
4. **🎨 Layouts & Design** - Creating beautiful, organized interfaces
5. **🏔️ Snowflake Integration** - Leveraging Streamlit-in-Snowflake features
6. **🚀 Advanced Patterns** - Async queries, database writebacks & production techniques

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Snowflake account (for Snowflake-specific features)
- SnowSQL configured with a connection (for local development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd streamlit-in-snowflake-getting-started
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Configure Snowflake connection**
   
   Update `app/utils/config.py` with your Snowflake connection name:
   ```python
   CONNECTION_NAME = "your_connection_name"
   ```

5. **Run the app**
   ```bash
   streamlit run app/app.py
   ```

6. **Open your browser**
   
   Navigate to `http://localhost:8501`


## Topics Covered

### Dual Environment Support
- **Local Development**: Uses SnowSQL connections for local testing
- **Streamlit-in-Snowflake**: Automatically detects and uses native Snowflake session
- Seamless switching between environments

### Production-Ready Patterns
- Session state management
- Caching strategies (`@st.cache_data`, `@st.cache_resource`)
- Async query execution (non-blocking Snowflake queries)
- Error handling and validation
- Input validation
- Multi-step workflows
- Pagination for large datasets
- Progress tracking
- Dependent dropdowns
- Database writebacks
