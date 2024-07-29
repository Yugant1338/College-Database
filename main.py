import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from connect import connect_to_db
from student import extract_student_data
from faculty import extract_faculty_data
from department import extract_department_data
from course import extract_course_data

def connect_and_query(username, password, domain):
    try:
        # Connect to the database
        connection = connect_to_db(username, password)

        if connection:
            print("Connected to the database.")
            time.sleep(3)
            if domain == 'Student':
                extract_student_data(connection)
            elif domain == 'Faculty':
                extract_faculty_data(connection)
            elif domain == 'Department':
                extract_department_data(connection)
            elif domain == 'Courses':
                extract_course_data(connection)
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        else:
            print("Failed to connect to the database.")

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        if connection:
            connection.close()

def on_submit():
    username = username_entry.get()
    password = password_entry.get()
    domain = domain_var.get()

    if not (username and password and domain):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    connect_and_query(username, password, domain)

# Create the main window
root = tk.Tk()
root.title("DBMS Query Tool")

# Create labels and entries for user inputs
tk.Label(root, text="Username:").grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Domain:").grid(row=2, column=0, padx=5, pady=5)
domain_var = tk.StringVar(root)
domain_var.set("Student")
domain_menu = tk.OptionMenu(root, domain_var, "Student", "Faculty", "Department", "Courses")
domain_menu.grid(row=2, column=1, padx=5, pady=5)

# Create submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Run the Tkinter event loop
root.mainloop()
