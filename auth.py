import psycopg2
import secret

# Johnsonpass
def auth_login(email:str, password:str):
    """
    Goal: check the database for correct email and pass word
    param:
        - email: user email to login
        - password: user password to login
    return:
        - boolean: True, if email and password are correct
                    False, if either is wrong
        - db_username: username of the logged-in user
    """
    query = f"""
        SELECT username, password
        FROM students
        JOIN credentials USING (email)
        WHERE email = '{email}';"""

    try:
        db_username, db_password = retrieve_data_db_with_sql(query)[0]
    except:
        return "Email NOT found!"
    finally:
        # user was found in the database, and password is correct
        if password == db_password:
            return True, db_username
        else:
            # user was found in the database, but password is wrong
            print("Incorrect Password!")
            return False, "Incorrect Password!"



def retrieve_data_db_with_sql(query:str):
    """
    Goal: Retrieve data from amazon aws server database with python
    param:
        - query: string sql query to be executed in the database

    """
    host, bd_name, bd_user, db_password = secret.db_connection()
    # Initialize placeholders
    connection = None
    curr = None
    try:
        connection = psycopg2.connect(host=host, dbname=bd_name, user=bd_user,
                                      password=db_password)  # Start a db connection
        curr = connection.cursor()  # used for command execution
        print("Connection successful!")
        #########################################################
        ##############------ Queries Start Here _____############
        #########################################################

        curr.execute(f"""{query}""")
        query_result = curr.fetchall()

        #########################################################
        ###############______ Queries end Here ______############
        #########################################################
        connection.commit()  # commit connection
        print("Query commited successful!")
    except Exception as e:
        print("Error:", e)
    finally:
        # end the cursor and connection
        if curr: curr.close()
        if connection:
            connection.close()
            return query_result

# if __name__ == "__main__":
    # auth_login("emmajohnson@gmail.com", "Johnsonpass")