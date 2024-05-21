from snowflake.snowpark import Session
import snowflake.connector as snconn
import streamlit as st


def connection(account, username, password):
    error = None
    connection_parameters = {
        "account": account,
        "user": username,
        "password": password,
    }  
    try:
        if account and username and password:
            session = Session.builder.configs(connection_parameters).create()
            print("New session created successfully!")
    except Exception as e:
        error = str(e)
    
    return session, error

def databaseConnection(username, password, account):
    if (username and password and account):
        # Create a connection object
        con = snconn.connect(
            user=username,
            password=password,
            account=account,
        )
        # Create a cursor object
        cur = con.cursor()

        # Execute the SQL command to create a warehouse
        cur.execute(f"CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH")
        cur.execute(f"ALTER USER {username} SET DEFAULT_WAREHOUSE = COMPUTE_WH")

        # Close the cursor
        cur.close()

        # Re-establish the connection with the new warehouse
        con = snconn.connect(
            user=username,
            password=password,
            account=account,
            warehouse='COMPUTE_WH',
            role='ACCOUNTADMIN'
        )
        return con