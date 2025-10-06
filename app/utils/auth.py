from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSessionException
from utils.config import CONNECTION_NAME

def get_snowflake_session():
    try:
        session = get_active_session()
    except SnowparkSessionException as e:
        session = Session.builder.config("connection_name", CONNECTION_NAME).create()
    except Exception as e:
        print(f"Error getting snowflake session: {e}")
    return session
        