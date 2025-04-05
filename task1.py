import mysql.connector
import random
from faker import Faker

fake = Faker()

# Function to connect to MySQL database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Rishi@2005",
            database="college"
        )
        if conn.is_connected():
            print("Connection is successful!")
        return conn
    except mysql.connector.Error as e:
        print("Error while connecting to DB:", e)
        return None

#table creation function
def create_students_table():
    conn = connect_to_db()
    if conn is None:
        return  # Exit if connection fails

    try:
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS student_details (
            roll_no INT PRIMARY KEY,
            name VARCHAR(50),
            age INT,
            branch VARCHAR(50),
            fees DECIMAL(10,2),
            phoneno VARCHAR(15)
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'student_details' created successfully!")

    except mysql.connector.Error as e:
        print("Error creating table:", e)
    finally:
        cursor.close()
        conn.close()

# Function to generate student data
def generate_students(num_students):
    branches = ['CSE', 'IT', 'ME', 'CE', 'EE']
    students = []

    for i in range(1, num_students + 1):
        roll_no = i
        name = fake.name()
        age = random.randint(18, 25)
        branch = random.choice(branches)
        fees = round(random.uniform(10000, 100000), 2)  # Rounded fees
        phoneno = str(fake.random_int(min=1000000000, max=9999999999))

        students.append((roll_no, name, age, branch, fees, phoneno))
    return students

# Function to insert student records into the database
def insert_student_details(num_students):
    conn = connect_to_db()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO student_details (roll_no, name, age, branch, fees, phoneno)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        student_list = generate_students(num_students)

        cursor.executemany(insert_query, student_list)  
        conn.commit()
        print(f"{cursor.rowcount} student records inserted successfully!")

    except mysql.connector.Error as e:
        print("Error inserting data:", e)
    finally:
        cursor.close()
        conn.close()

# Function to fetch and display student records
def fetch_data():
    conn = connect_to_db()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM student_details;"
        cursor.execute(query)
        students = cursor.fetchall()

        print("Roll No | Name       | Age | Branch | Fees    | Phone No")
        print("-------------------------------------------------------------")
        for student in students:
            print(f"{student[0]:<7} | {student[1]:<10} | {student[2]:<3} | {student[3]:<7} | {student[4]:<7.2f} | {student[5]}")

    except mysql.connector.Error as e:
        print("Fetching data error:", e)
    finally:
        cursor.close()
        conn.close()

# Execution
create_students_table()
num_students = int(input("Enter the number of student records to insert: "))
insert_student_details(num_students)
fetch_data()
