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

### Deploying to Streamlit-in-Snowflake

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```

2. **Create Streamlit App in Snowflake**
   ```sql
   CREATE STREAMLIT streamlit_learning_hub
     ROOT_LOCATION = '@<stage>/<path>'
     MAIN_FILE = 'app.py'
     QUERY_WAREHOUSE = '<warehouse_name>';
   ```

3. **Link to GitHub Repository**
   
   Follow Snowflake's documentation to connect your GitHub repository

4. **Access Your App**
   
   Your app will be available in Snowsight under Apps → Streamlit

## 📂 Project Structure

```
streamlit-in-snowflake-getting-started/
├── app/
│   ├── app.py                           # Main landing page
│   ├── requirements.txt                 # Python dependencies
│   ├── pages/                          # Lesson pages (auto-discovered by Streamlit)
│   │   ├── 1_🎯_Basics.py
│   │   ├── 2_🔄_Session_State.py
│   │   ├── 3_⚡_Caching.py
│   │   ├── 4_🎨_Layouts_and_Design.py
│   │   ├── 5_🏔️_Snowflake_Integration.py
│   │   ├── 6_🚀_Advanced_Patterns.py
│   └── utils/
│       ├── auth.py                     # Snowflake session management
│       └── config.py                   # Configuration settings
├── README.md
└── LICENSE
```

## 🔑 Key Features

### Dual Environment Support
- **Local Development**: Uses SnowSQL connections for local testing
- **Streamlit-in-Snowflake**: Automatically detects and uses native Snowflake session
- Seamless switching between environments

### Interactive Learning
- **Side-by-Side Format**: See the code and the result together
- **Live Examples**: Every concept shown with working demonstrations
- **Demo-Ready**: Perfect for customer presentations and live walkthroughs
- **Progressive Difficulty**: Each lesson builds on previous concepts
- **Button-Triggered**: Explicit user actions for all interactions

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

## 💡 Teaching Methodology

This tutorial follows these principles:

1. **Show, Don't Just Tell**: Every concept has a live, interactive example
2. **Common Pitfalls First**: Learn from mistakes others have made
3. **Progressive Complexity**: Start simple, build to advanced
4. **Real-World Focus**: Examples based on actual use cases
5. **Best Practices**: Not just "how" but "how well"

## 🎯 Learning Objectives

After completing this tutorial, you'll be able to:

- ✅ Build interactive Streamlit applications from scratch
- ✅ Manage complex application state effectively
- ✅ Optimize app performance with caching
- ✅ Create professional, well-designed layouts
- ✅ Query and manipulate Snowflake data
- ✅ Execute async queries for better performance
- ✅ Build interactive data exploration interfaces
- ✅ Apply production-ready patterns
- ✅ Deploy apps to Streamlit-in-Snowflake

## 🔧 Configuration

### Snowflake Connection

The app uses a flexible connection system that works in both environments:

**Local Development:**
```python
# app/utils/config.py
CONNECTION_NAME = "your_connection_name"  # From SnowSQL config
```

**Streamlit-in-Snowflake:**
```python
# Automatically uses get_active_session() - no configuration needed
```

### Customization

You can customize the learning content by:
- Modifying existing lesson pages in `app/pages/`
- Adding new lesson pages (they'll auto-appear in sidebar)
- Updating the landing page in `app/app.py`
- Adding utility functions in `app/utils/`

## 🤝 Contributing

This is a learning resource! If you find issues or want to improve it:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both locally and in Snowflake (if possible)
5. Submit a pull request

## 📖 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit-in-Snowflake Docs](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [Snowpark Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/index)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)

## 🐛 Troubleshooting

### Common Issues

**Problem**: `SnowparkSessionException` when running locally
**Solution**: Ensure your SnowSQL connection is configured correctly and the connection name matches in `config.py`

**Problem**: Pages not showing in sidebar
**Solution**: Ensure files in `pages/` directory follow naming convention and have proper imports

**Problem**: Import errors
**Solution**: Reinstall requirements: `pip install -r app/requirements.txt`

**Problem**: Slow performance
**Solution**: Check that caching is being used for expensive operations (see Lesson 3)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

Built to help the community learn Streamlit and leverage the power of Streamlit-in-Snowflake!

---

**Happy Learning! 🚀**

Questions? Open an issue or start a discussion!