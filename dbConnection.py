from snowflake.snowpark import Session

def connection(account, username, password):
    # intialize new session and error
    new_session = None
    error = None
    connection_parameters = {
        "account": account,
        "user": username,
        "password": password,
    }  
    try:
        if account and username and password:
            new_session = Session.builder.configs(connection_parameters).create()
            print("New session created successfully!")
            print(new_session)
    except Exception as e:
        error = str(e)
    
    return new_session, error