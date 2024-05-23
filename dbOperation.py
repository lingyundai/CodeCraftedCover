import streamlit as st

def create_database(cur, db_name):
    # Create a new database
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def switch_database(cur, db_name):
    # Switch to the new database
    cur.execute(f"USE DATABASE {db_name}")

def create_table(cur, table_name):
    # Create a new table with predefined columns
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            filename VARCHAR(200) UNIQUE,
            content VARCHAR(16777216)  -- Maximum length for VARCHAR in Snowflake
        )
    """)

def insert_data(cur, table_name, data):
    # Check if the filename already exists in the table
    cur.execute(f"""
        SELECT filename FROM "{table_name}" WHERE filename = %s
    """, (data[0]['file_name'],))
    if cur.fetchone() is not None:
        print(f"Filename {data[0]['file_name']} already exists in the table.")
        return

    # If the filename does not exist, insert the data into the table
    try:
        cur.execute(f"""
            INSERT INTO "{table_name}" (filename, content) 
            VALUES (%s, %s)
        """, (data[0]['file_name'], data[0]['file_content']))
        print(f"Successfully inserted data into {table_name}")
        st.rerun()
    except Exception as e:
        print(f"Failed to insert data: {e}")

def fetch_data(cur, table_name):
    # Fetch all data from the table
    data = cur.execute(f"""
        SELECT filename, content FROM "{table_name}"
    """)
    return data.fetchall()

def delete_file(cur, table_name, filename):
    # Delete the file from the table
    cur.execute(f"""
        DELETE FROM "{table_name}" WHERE filename = %s
    """, (filename,))
    print(f"Successfully deleted {filename} from the {table_name}.")
    return