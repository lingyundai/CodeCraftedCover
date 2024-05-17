def create_database(cur, db_name):
    # Create a new database
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def switch_database(cur, db_name):
    # Switch to the new database
    cur.execute(f"USE DATABASE {db_name}")

def create_table(cur, table_name):
    # Create a new table with predefined columns
    cur.execute(f"""
        CREATE TABLE  IF NOT EXISTS "{table_name}" (
            filename VARCHAR(200),
            content VARCHAR(16777216)  -- Maximum length for VARCHAR in Snowflake
        )
    """)
def insert_data(cur, table_name, data):
    print(data[0]['file_name'])
    print(data[0]['file_content'])
    print(table_name)
    # Insert the data into the table
    cur.execute(f"""
        INSERT INTO "{table_name}" (filename, content) 
        VALUES (%s, %s)
    """, (data[0]['file_name'], data[0]['file_content']))

def fetch_data(cur, table_name):
    # Fetch the data from the table
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    for row in rows:
        print(row)