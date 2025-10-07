"""
Lesson 7: AI with Snowflake Cortex
Leverage Cortex AI functions for intelligent data processing
"""

import streamlit as st
from utils.auth import get_snowflake_session
import pandas as pd
from PIL import Image

st.set_page_config(page_title="AI with Cortex", page_icon="🤖", layout="wide")

st.title("🤖 Lesson 7: AI with Snowflake Cortex")

st.markdown("""
Snowflake Cortex brings powerful AI capabilities directly into your data platform. 
No need for external API keys or infrastructure - just use SQL functions!
""")

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
# SECTION 0: Setup - Create Stage for Images
# =============================================================================
st.header("0. Setup - Create Stage for Images")

st.markdown("""
First, let's set up a stage in `DEMO.PUBLIC` for storing images that Cortex will analyze. 
This stage will be used by the image analysis examples below.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.code("""
# Create stage for images in DEMO.PUBLIC
# Use fully qualified path
session.sql('''
    CREATE STAGE IF NOT EXISTS DEMO.PUBLIC.CORTEX_STAGE
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
''').collect()

st.success("Stage created: @DEMO.PUBLIC.CORTEX_STAGE")
    """, language="python")

with col2:
    st.markdown("**Create your stage:**")
    
    try:
        if st.button("Create Stage", key="create_stage_btn"):
            with st.spinner("Creating stage..."):
                try:
                    # Create stage with encryption using fully qualified path
                    session.sql("""
                        CREATE STAGE IF NOT EXISTS DEMO.PUBLIC.CORTEX_STAGE
                        ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
                    """).collect()
                    
                    st.success("✅ Stage created: `@DEMO.PUBLIC.CORTEX_STAGE`")
                    st.caption("This stage can now be used for image analysis!")
                    
                except Exception as e:
                    st.error(f"Error creating stage: {e}")
                    st.info("💡 Make sure you have CREATE STAGE privileges in DEMO.PUBLIC")
        
        # Show existing stages
        with st.expander("View existing stages in DEMO.PUBLIC"):
            try:
                stages = session.sql("SHOW STAGES IN SCHEMA DEMO.PUBLIC").collect()
                if stages:
                    stage_df = pd.DataFrame([
                        {'Name': row['name'], 'Type': row['type']}
                        for row in stages
                    ])
                    st.dataframe(stage_df, use_container_width=True)
                else:
                    st.info("No stages found")
            except Exception as e:
                st.warning(f"Could not list stages: {e}")
                
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("💡 Make sure the DEMO database and PUBLIC schema exist")

st.markdown("---")

# =============================================================================
# SECTION 1: Image Analysis
# =============================================================================
st.header("1. Image Analysis with Cortex")

st.markdown("""
Upload an image and let Cortex AI describe what's in it using advanced vision models!
Images are stored in a Snowflake stage and processed using TO_FILE.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**How it works:**")
    st.code("""
# Upload image to stage
uploaded_file = st.file_uploader("Upload Image")
if uploaded_file:
    # Save image to temp location
    temp_path = f"/tmp/{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Upload file to stage using fully qualified path
    stage_location = '@DEMO.PUBLIC.CORTEX_STAGE/uploads'
    session.file.put(
        temp_path,
        stage_location,
        auto_compress=False
    )
    
    # Use Cortex COMPLETE with TO_FILE
    # Note: stage and path are separate arguments
    result = session.sql(f'''
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'claude-3-5-sonnet',
            'Describe this image in detail',
            TO_FILE('@DEMO.PUBLIC.CORTEX_STAGE', 'uploads/{uploaded_file.name}')
        ) as response
    ''').to_pandas()
    
    st.write(result['RESPONSE'][0])
    """, language="python")

with col2:
    st.markdown("**Try it yourself:**")
    
    try:
        # Default to DEMO.PUBLIC.CORTEX_STAGE
        default_db = 'DEMO'
        default_schema = 'PUBLIC'
        default_stage = 'CORTEX_STAGE'
        
        # Get available databases
        dbs = session.sql("SHOW DATABASES").collect()
        db_names = [row['name'] for row in dbs if row['name'] not in ['SNOWFLAKE', 'SNOWFLAKE_SAMPLE_DATA']]
        
        # Set default index
        default_db_idx = db_names.index(default_db) if default_db in db_names else 0
        
        selected_db = st.selectbox("Database", db_names, index=default_db_idx, key="img_db")
        
        # Get schemas
        schemas = session.sql(f"SHOW SCHEMAS IN DATABASE {selected_db}").collect()
        schema_names = [row['name'] for row in schemas if row['name'] != 'INFORMATION_SCHEMA']
        
        # Set default schema index
        default_schema_idx = schema_names.index(default_schema) if default_schema in schema_names else 0
        
        selected_schema = st.selectbox("Schema", schema_names, index=default_schema_idx, key="img_schema")
        
        # Get stages - use fully qualified path
        stages = session.sql(f"SHOW STAGES IN SCHEMA {selected_db}.{selected_schema}").collect()
        stage_names = [row['name'] for row in stages]
        
        if stage_names:
            # Set default stage index
            default_stage_idx = stage_names.index(default_stage) if default_stage in stage_names else 0
            
            selected_stage = st.selectbox("Stage", stage_names, index=default_stage_idx, key="img_stage")
            
            uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="image_upload")
            
            if uploaded_file is not None:
                # Display the image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image")
                
                if st.button("Analyze Image", key="analyze_btn"):
                    with st.spinner("Uploading and analyzing image with Cortex AI..."):
                        try:
                            # Save image temporarily
                            temp_path = f"/tmp/{uploaded_file.name}"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Upload to stage using fully qualified path
                            stage_location = f"@{selected_db}.{selected_schema}.{selected_stage}/cortex_images"
                            upload_result = session.file.put(
                                temp_path, 
                                stage_location, 
                                auto_compress=False, 
                                overwrite=True
                            )
                            
                            st.info(f"✅ File uploaded to stage")
                            
                            # Construct the file path for TO_FILE
                            # TO_FILE expects fully qualified stage and relative path separately
                            file_path = f"cortex_images/{uploaded_file.name}"
                            
                            # Use Cortex COMPLETE with TO_FILE using fully qualified stage path
                            query = f"""
                                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                                    'claude-3-5-sonnet',
                                    'Describe this image in detail. What objects, people, or scenes do you see?',
                                    TO_FILE('@{selected_db}.{selected_schema}.{selected_stage}', '{file_path}')
                                ) as response
                            """
                            
                            result = session.sql(query).to_pandas()
                            
                            st.success("✅ Analysis Complete!")
                            st.markdown("**AI Description:**")
                            st.write(result['RESPONSE'][0])
                            
                        except Exception as e:
                            st.error(f"Error analyzing image: {e}")
                            st.info("💡 Make sure you have access to Cortex AI functions and the stage has server-side encryption enabled")
        else:
            st.warning("⚠️ No stages found. Please create the CORTEX_STAGE in Section 0 above.")
                
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("💡 Make sure DEMO database and PUBLIC schema exist, and create CORTEX_STAGE in Section 0 above.")

st.markdown("---")

# =============================================================================
# SECTION 2: Text Sentiment Analysis
# =============================================================================
st.header("2. Sentiment Analysis")

st.markdown("""
Analyze the sentiment of text to understand emotions and opinions.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.code("""
# Analyze sentiment
text = "I love using Snowflake Cortex! It's amazing!"

result = session.sql(f'''
    SELECT SNOWFLAKE.CORTEX.SENTIMENT('{text}') 
    as sentiment
''').to_pandas()

# Returns: 1 (positive), 0 (neutral), -1 (negative)
st.write(f"Sentiment: {result['SENTIMENT'][0]}")
    """, language="python")

with col2:
    st.markdown("**Try different texts:**")
    
    sentiment_text = st.text_area(
        "Enter text to analyze:",
        value="I love using Snowflake Cortex! It's amazing!",
        height=100,
        key="sentiment_input"
    )
    
    if st.button("Analyze Sentiment", key="sentiment_btn"):
        try:
            # Escape single quotes in the text
            escaped_text = sentiment_text.replace("'", "''")
            
            query = f"""
                SELECT SNOWFLAKE.CORTEX.SENTIMENT('{escaped_text}') as sentiment
            """
            
            result = session.sql(query).to_pandas()
            sentiment_score = result['SENTIMENT'][0]
            
            # Display result with emoji
            if sentiment_score > 0.3:
                st.success(f"😊 Positive Sentiment: {sentiment_score:.2f}")
            elif sentiment_score < -0.3:
                st.error(f"😞 Negative Sentiment: {sentiment_score:.2f}")
            else:
                st.info(f"😐 Neutral Sentiment: {sentiment_score:.2f}")
            
            st.caption("Score ranges from -1 (most negative) to 1 (most positive)")
            
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 3: Text Summarization
# =============================================================================
st.header("3. Text Summarization")

st.markdown("""
Automatically generate concise summaries of long text documents.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.code("""
# Summarize long text
long_text = "..."  # Your long document

result = session.sql(f'''
    SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
        '{long_text}'
    ) as summary
''').to_pandas()

st.write(result['SUMMARY'][0])
    """, language="python")

with col2:
    st.markdown("**Summarize any text:**")
    
    default_text = """Snowflake is a cloud-based data platform that enables organizations to mobilize their data with Snowflake's Data Cloud. The platform provides instant, secure, and governed access to their entire network of data, while enabling near-unlimited scalability, concurrency, and performance. Snowflake runs on multiple cloud providers including AWS, Azure, and Google Cloud Platform. It separates compute from storage, allowing users to scale up or down as needed without disruption. The architecture consists of three key layers: database storage, query processing, and cloud services. Snowflake supports structured and semi-structured data, making it versatile for various data types. It offers features like time travel, zero-copy cloning, and data sharing capabilities."""
    
    summary_text = st.text_area(
        "Enter text to summarize:",
        value=default_text,
        height=150,
        key="summary_input"
    )
    
    if st.button("Generate Summary", key="summary_btn"):
        try:
            with st.spinner("Generating summary..."):
                # Escape single quotes
                escaped_text = summary_text.replace("'", "''")
                
                query = f"""
                    SELECT SNOWFLAKE.CORTEX.SUMMARIZE('{escaped_text}') as summary
                """
                
                result = session.sql(query).to_pandas()
                
                st.success("✅ Summary Generated!")
                st.markdown("**Summary:**")
                st.info(result['SUMMARY'][0])
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 4: Language Translation
# =============================================================================
st.header("4. Language Translation")

st.markdown("""
Translate text between languages using Cortex AI.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.code("""
# Translate text
text = "Hello, how are you?"
target_language = "es"  # Spanish

result = session.sql(f'''
    SELECT SNOWFLAKE.CORTEX.TRANSLATE(
        '{text}',
        'en',  -- source language
        '{target_language}'  -- target language
    ) as translation
''').to_pandas()

st.write(result['TRANSLATION'][0])
    """, language="python")

with col2:
    st.markdown("**Translate text:**")
    
    translate_text = st.text_input(
        "Enter text to translate:",
        value="Hello, how are you today?",
        key="translate_input"
    )
    
    col_src, col_tgt = st.columns(2)
    
    with col_src:
        source_lang = st.selectbox(
            "From:",
            ["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            key="source_lang"
        )
    
    with col_tgt:
        target_lang = st.selectbox(
            "To:",
            ["es", "en", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            index=0,
            key="target_lang"
        )
    
    if st.button("Translate", key="translate_btn"):
        try:
            # Escape single quotes
            escaped_text = translate_text.replace("'", "''")
            
            query = f"""
                SELECT SNOWFLAKE.CORTEX.TRANSLATE(
                    '{escaped_text}',
                    '{source_lang}',
                    '{target_lang}'
                ) as translation
            """
            
            result = session.sql(query).to_pandas()
            
            st.success("✅ Translation Complete!")
            st.markdown(f"**{target_lang.upper()}:**")
            st.info(result['TRANSLATION'][0])
            
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 5: Text Generation & Completion
# =============================================================================
st.header("5. AI Text Generation")

st.markdown("""
Generate text completions using Large Language Models (LLMs) with Cortex COMPLETE.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.code("""
# Generate text with LLM
prompt = "Write a haiku about data"

result = session.sql(f'''
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'llama3.1-8b',  -- or mistral-large, etc.
        '{prompt}'
    ) as response
''').to_pandas()

st.write(result['RESPONSE'][0])
    """, language="python")

with col2:
    st.markdown("**Generate creative text:**")
    
    # Model selection
    llm_model = st.selectbox(
        "Select Model:",
        ["llama3.1-8b", "llama3.1-70b", "mistral-large", "mixtral-8x7b"],
        key="llm_model"
    )
    
    generation_prompt = st.text_area(
        "Enter your prompt:",
        value="Write a short poem about data analytics and insights",
        height=100,
        key="generation_input"
    )
    
    if st.button("Generate Text", key="generate_btn"):
        try:
            with st.spinner(f"Generating with {llm_model}..."):
                # Escape single quotes
                escaped_prompt = generation_prompt.replace("'", "''")
                
                query = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        '{llm_model}',
                        '{escaped_prompt}'
                    ) as response
                """
                
                result = session.sql(query).to_pandas()
                
                st.success("✅ Text Generated!")
                st.markdown("**AI Response:**")
                st.markdown(result['RESPONSE'][0])
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# =============================================================================
# SECTION 6: Bulk Processing with Cortex
# =============================================================================
st.header("6. Batch Processing Data")

st.markdown("""
Process entire datasets with Cortex AI functions - perfect for analyzing customer feedback, reviews, or documents at scale!
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**Processing text data:**")
    st.code("""
# Create sample data
sample_reviews = pd.DataFrame({
    'review_id': [1, 2, 3],
    'review_text': [
        'Great product! Highly recommend.',
        'Terrible experience. Very disappointed.',
        'It works as expected.'
    ]
})

# Write to Snowflake
session.create_dataframe(sample_reviews)\\
       .write.save_as_table('reviews', mode='overwrite')

# Analyze all reviews at once
result = session.sql('''
    SELECT 
        review_id,
        review_text,
        SNOWFLAKE.CORTEX.SENTIMENT(review_text) as sentiment,
        SNOWFLAKE.CORTEX.SUMMARIZE(review_text) as summary
    FROM reviews
''').to_pandas()

st.dataframe(result)
    """, language="python")
    
    st.markdown("**Processing images in batch:**")
    st.code("""
# Process all images in a stage
result = session.sql('''
    SELECT 
        RELATIVE_PATH,
        SNOWFLAKE.CORTEX.COMPLETE(
            'claude-3-5-sonnet',
            PROMPT(
                'Classify the input image {0} in no more than 2 words. Respond in JSON',
                TO_FILE('@myimages', RELATIVE_PATH)
            )
        ) as image_classification
    FROM DIRECTORY(@myimages)
''').to_pandas()

st.dataframe(result)
    """, language="python")

with col2:
    st.markdown("**Batch process sample reviews:**")
    
    # Get database and schema for table creation
    try:
        # Defaults
        default_db = 'DEMO'
        default_schema = 'PUBLIC'
        
        dbs = session.sql("SHOW DATABASES").collect()
        db_names = [row['name'] for row in dbs if row['name'] not in ['SNOWFLAKE', 'SNOWFLAKE_SAMPLE_DATA']]
        
        if db_names:
            # Set default index
            default_db_idx = db_names.index(default_db) if default_db in db_names else 0
            
            batch_db = st.selectbox("Database", db_names, index=default_db_idx, key="batch_db")
            
            schemas = session.sql(f"SHOW SCHEMAS IN DATABASE {batch_db}").collect()
            schema_names = [row['name'] for row in schemas if row['name'] != 'INFORMATION_SCHEMA']
            
            if schema_names:
                # Set default schema index
                default_schema_idx = schema_names.index(default_schema) if default_schema in schema_names else 0
                
                batch_schema = st.selectbox("Schema", schema_names, index=default_schema_idx, key="batch_schema")
                
                if st.button("Process Sample Reviews", key="batch_btn"):
                    try:
                        with st.spinner("Creating sample data..."):
                            # Sample reviews
                            sample_reviews = pd.DataFrame({
                                'REVIEW_ID': range(1, 6),
                                'REVIEW_TEXT': [
                                    'Absolutely love this product! Best purchase ever. Highly recommend to everyone!',
                                    'Terrible experience. Product broke after one day. Do not buy.',
                                    'It works as expected. Nothing special but does the job.',
                                    'Amazing customer service and great quality. Will buy again!',
                                    'Waste of money. Poor quality and slow shipping.'
                                ]
                            })
                            
                            # Create table using fully qualified path
                            table_name = f"{batch_db}.{batch_schema}.CORTEX_REVIEWS_DEMO"
                            session.create_dataframe(sample_reviews).write.save_as_table(
                                table_name,
                                mode='overwrite'
                            )
                            
                            st.info(f"✅ Created table: {table_name}")
                        
                        with st.spinner("Analyzing all reviews with Cortex..."):
                            # Analyze with Cortex
                            query = f"""
                                SELECT 
                                    REVIEW_ID,
                                    REVIEW_TEXT,
                                    SNOWFLAKE.CORTEX.SENTIMENT(REVIEW_TEXT) as SENTIMENT_SCORE,
                                    CASE 
                                        WHEN SNOWFLAKE.CORTEX.SENTIMENT(REVIEW_TEXT) > 0.3 THEN 'Positive'
                                        WHEN SNOWFLAKE.CORTEX.SENTIMENT(REVIEW_TEXT) < -0.3 THEN 'Negative'
                                        ELSE 'Neutral'
                                    END as SENTIMENT_LABEL
                                FROM {table_name}
                                ORDER BY REVIEW_ID
                            """
                            
                            result = session.sql(query).to_pandas()
                            
                            st.success(f"✅ Processed {len(result)} reviews!")
                            st.dataframe(result, use_container_width=True)
                            
                            # Show statistics
                            st.markdown("**Sentiment Distribution:**")
                            sentiment_counts = result['SENTIMENT_LABEL'].value_counts()
                            st.bar_chart(sentiment_counts)
                            
                            # Cleanup
                            st.caption(f"💡 Table created: {table_name}")
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.info("💡 Make sure you have access to Cortex AI functions and write permissions")
            else:
                st.warning("No schemas available")
        else:
            st.warning("No databases available")
    except Exception as e:
        st.warning(f"Setup required: {e}")

st.markdown("---")

# =============================================================================
# Key Takeaways
# =============================================================================
st.header("🎓 Key Takeaways")

st.markdown("""
### Available Cortex AI Functions:

1. **📸 COMPLETE (with TO_FILE)** - Analyze images stored in Snowflake stages
2. **😊 SENTIMENT** - Analyze text sentiment (-1 to 1)
3. **📝 SUMMARIZE** - Generate concise summaries
4. **🌍 TRANSLATE** - Translate between languages
5. **🤖 COMPLETE** - Text generation with LLMs
6. **📊 Batch Processing** - Process entire datasets with AI functions

### Supported Models:

**Vision Models (with TO_FILE):**
- **claude-3-5-sonnet** - Advanced image understanding (max 3.75 MB, 8000x8000)
- **pixtral-large** - Vision model (max 10 MB, supports .bmp)

**Text Models:**
- **llama3.1-8b** - Fast, efficient for most tasks
- **llama3.1-70b** - More powerful, better reasoning
- **mistral-large** - High-quality text generation
- **mixtral-8x7b** - Great for complex tasks

### Key Benefits:

✅ **No External APIs** - Everything runs in Snowflake
✅ **Data Privacy** - Your data never leaves Snowflake
✅ **SQL Integration** - Use AI in standard SQL queries
✅ **Scalability** - Process millions of records
✅ **Cost Effective** - Pay only for compute used

### Best Practices:

1. **Batch Processing** - Analyze datasets in bulk for efficiency
2. **Caching** - Cache AI results for repeated queries
3. **Model Selection** - Choose the right model for your task
4. **Error Handling** - Always handle potential errors gracefully
5. **Prompt Engineering** - Clear prompts get better results

### Common Use Cases:

- **Customer Feedback Analysis** - Sentiment and summarization at scale
- **Content Moderation** - Classify and filter content
- **Document Processing** - Summarize and extract insights from documents
- **Multilingual Support** - Translate content between languages
- **Image Analysis** - Analyze and categorize images from stages
- **Data Enrichment** - Enhance datasets with AI-generated insights

### Performance Tips:

- Use appropriate model size for your task
- Batch process when analyzing multiple records
- Combine multiple Cortex functions in one query
- Cache results with `@st.cache_data` for repeated operations

### What's Next?

Explore combining Cortex AI with:
- **Caching (Lesson 3)** - Cache AI results for better performance
- **Snowflake Integration (Lesson 5)** - Process entire tables
- **Advanced Patterns (Lesson 6)** - Build production AI features

Check out **Lesson 8: Quick Reference** for a complete cheat sheet!
""")

st.markdown("---")

st.info("""
💡 **Important Notes:** 
- Cortex AI functions require proper Snowflake account setup and permissions
- Image analysis requires images to be stored in Snowflake stages with server-side encryption enabled
- Supported image formats: .jpg, .jpeg, .png, .gif, .webp (and .bmp for pixtral-large)
- Maximum image size: 3.75 MB for claude-3-5-sonnet, 10 MB for pixtral-large
- Features may vary based on your Snowflake edition and region
""")

