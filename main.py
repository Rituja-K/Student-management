import re
import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',         
            database='student_system',
            user='root',      
            password='Password@01'  
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def register():
    print("=== Register ===")
    username = input("Enter username: ")
    
    connection = create_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
    
    if cursor.fetchone():
        print("Username already exists. Please choose another.")
        cursor.close()
        connection.close()
        return

    password = input("Enter password: ")
    name = input("Enter your name: ")
    contact = input("Enter contact details: ")
    email = input("Enter email: ")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format. Please try again.")
        cursor.close()
        connection.close()
        return

    city = input("Enter city: ")
    department = input("Enter department: ")
    student_id = input("Enter student ID: ")

    cursor.execute(
        "INSERT INTO students (username, password, name, contact, email, city, department, student_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (username, password, name, contact, email, city, department, student_id)
    )
    connection.commit()
    print("Registration successful!")
    
    cursor.close()
    connection.close()

def login():
    print("=== Login ===")
    username = input("Enter username: ")
    
    connection = create_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        print("Username does not exist. Please register first.")
        cursor.close()
        connection.close()
        return None

    password = input("Enter password: ")
    
    if user['password'] == password:
        print(f"Login successful! Welcome back, {user['name']}!")
        cursor.close()
        connection.close()
        return username
    else:
        print("Incorrect password. Please try again.")
        cursor.close()
        connection.close()
        return None

def view_profile(username):
    print("=== View Profile ===")
    
    connection = create_connection()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
    profile = cursor.fetchone()

    if profile:
        for key, value in profile.items():
            if key != 'password':  
                print(f"{key.capitalize()}: {value}")
    else:
        print("Profile not found.")

    cursor.close()
    connection.close()

def update_profile(username):
    print("=== Update Profile ===")
    
    connection = create_connection()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
    profile = cursor.fetchone()

    if profile:
        print("Leave blank to keep current value.")
        name = input(f"Name ({profile['name']}): ") or profile['name']
        contact = input(f"Contact ({profile['contact']}): ") or profile['contact']
        email = input(f"Email ({profile['email']}): ") or profile['email']
        city = input(f"City ({profile['city']}): ") or profile['city']
        department = input(f"Department ({profile['department']}): ") or profile['department']
        student_id = input(f"Student ID ({profile['student_id']}): ") or profile['student_id']
        
        cursor.execute(
            """
            UPDATE students
            SET name = %s, contact = %s, email = %s, city = %s, department = %s, student_id = %s
            WHERE username = %s
            """,
            (name, contact, email, city, department, student_id, username)
        )
        connection.commit()
        print("Profile updated successfully!")
    else:
        print("User not found.")

    cursor.close()
    connection.close()

def delete_account(username):
    print("=== Delete Account ===")
    
    connection = create_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
    if confirm == 'yes':
        cursor.execute("DELETE FROM students WHERE username = %s", (username,))
        connection.commit()
        print("Account deleted successfully.")
    else:
        print("Account deletion cancelled.")

    cursor.close()
    connection.close()

def main():
    current_user = None
    while True:
        print("\n=== Student Management System ===")
        print("1. Register")
        print("2. Login")
        print("3. View Profile")
        print("4. Update Profile")
        print("5. Delete Account")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            register()
        elif choice == '2':
            current_user = login()
        elif choice == '3':
            if current_user:
                view_profile(current_user)
            else:
                print("Please log in first.")
        elif choice == '4':
            if current_user:
                update_profile(current_user)
            else:
                print("Please log in first.")
        elif choice == '5':
            if current_user:
                delete_account(current_user)
                current_user = None  
            else:
                print("Please log in first.")
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


