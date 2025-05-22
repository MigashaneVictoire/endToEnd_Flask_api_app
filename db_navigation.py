import psycopg2 # for working with postgres database
import secret
import pandas as pd

host, bd_name, bd_user, db_password = secret.db_connection()

# Initialize placeholders
connection = None
curr = None

try:
    connection = psycopg2.connect(host=host, dbname=bd_name, user=bd_user, password=db_password) # Start a db connection
    curr = connection.cursor() #used for command execution
    print("Connection successful!")

    #########################################################
    ##############------ Queries Start Here _____############
    #########################################################

    # Create these table if they do not exist
    curr.execute("""
        CREATE TABLE IF NOT EXISTS students(
        student_id INT PRIMARY KEY,
        first_name VARCHAR(32),
        last_name VARCHAR(32),
        age INT,
        gender CHAR
        );
        """)

    curr.execute("""
        CREATE TABLE IF NOT EXISTS courses(
        course_id INT PRIMARY KEY,
        course_name VARCHAR(32),
        instructor VARCHAR(32)
        );
        """)

    curr.execute("""
        CREATE TABLE IF NOT EXISTS enrollments(
        enrollment_id INT PRIMARY KEY,
        student_id INT,
        course_id INT,
        enrollment_date TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES studentS(student_id),
        FOREIGN KEY (course_id) REFERENCES courseS(course_id)
        );
        """)

    curr.execute("""
        CREATE TABLE IF NOT EXISTS credentials(
        student_id INT,
        email VARCHAR(64),
        password VARCHAR(255),
        FOREIGN KEY (student_id) REFERENCES studentS(student_id)
        )
    """)
    # --------------------- load data -----------------------
    # load the data from the csv files
    with open('data/students.csv', 'r') as f:
        next(f)  # Skip the header row
        curr.copy_from(f, 'students', sep=',', columns=('student_id','first_name', 'last_name', 'age','gender'))

    with open('data/courses.csv', 'r') as f:
        next(f)  # Skip the header row
        curr.copy_from(f, 'courses', sep=',', columns=('course_id','course_name', 'instructor'))

    with open('data/enrollments.csv', 'r') as f:
        next(f)  # Skip the header row
        curr.copy_from(f, 'enrollments', sep=',', columns=('enrollment_id','student_id', 'course_id', 'enrollment_date'))

    with open('data/credentials.csv', 'r') as f:
        next(f)  # Skip the header row
        curr.copy_from(f, 'credentials', sep=',', columns=('student_id','email', 'password'))

    #########################################################
    ###############______ Queries end Here ______############
    #########################################################
    connection.commit() #commit connection
    print("Query commited successful!")
except Exception as e:
    print("Error:", e)
finally:
    # end the cursor and connection
    if curr: curr.close()
    if connection: connection.close()

