import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cx_Oracle
from tabulate import tabulate

def extract_department_data(connection):
    def on_submit():
        department_id = entry_department_id.get()
        choice = combobox_choice.get()

        if not (department_id and choice):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        sql_query = ""

        if choice == 'Department Details':
            sql_query = f"SELECT * FROM Department WHERE Department_Code = '{department_id}'"
        elif choice == 'Faculties Details':
            sql_query = f"""
                        SELECT Faculty.Faculty_ID, Faculty.Faculty_Name, Faculty.Phone_Number
                        FROM Faculty
                        JOIN Teaches ON Faculty.Faculty_ID = Teaches.Faculty_ID
                        WHERE Teaches.Department_Code = '{department_id}'
                        """
        elif choice == 'HOD Details':
            sql_query = f"""
                        SELECT Faculty.Faculty_ID, Faculty.Faculty_Name, Faculty.Phone_Number
                        FROM Faculty
                        JOIN Department ON Faculty.Faculty_ID = Department.HOD
                        WHERE Department.Department_Code = '{department_id}'
                        """
        elif choice == 'Courses Details':
            sql_query = f"""
                        SELECT Course.Course_ID, Course.Course_Name, Course.No_of_Courses
                        FROM Course
                        JOIN Teaches ON Course.Course_ID = Teaches.Course_ID
                        WHERE Teaches.Department_Code = '{department_id}'
                        """
        else:
            messagebox.showerror("Error", "Invalid choice. Please enter a valid choice (1, 2, 3, or 4).")
            return

        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            department_data = cursor.fetchall()

            headers = []
            table_name = ""
            if choice == 'Department Details':
                table_name = "Department"
                headers = ["Department Code", "Department Name", "HOD"]
            elif choice == 'Faculties Details' or choice == 'HOD Details':
                table_name = "Faculty"
                headers = ["Faculty ID", "Faculty Name", "Phone Number"]
            elif choice == 'Courses Details':
                table_name = "Course"
                headers = ["Course ID", "Course Name", "No of Courses"]

            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Data from {table_name} table:\n")
            result_text.insert(tk.END, tabulate(department_data, headers=headers, tablefmt="grid"))
            result_text.config(state="disabled")

            cursor.close()

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return

    # Create a new window for department data extraction
    department_window = tk.Toplevel()
    department_window.title("Department Data Extraction")

    # Department ID label and entry
    label_department_id = ttk.Label(department_window, text="Enter Department ID:")
    label_department_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_department_id = ttk.Entry(department_window)
    entry_department_id.grid(row=0, column=1, padx=5, pady=5)

    # Choice label and combobox
    label_choice = ttk.Label(department_window, text="Choose an option:")
    label_choice.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    choices = ["Department Details", "Faculties Details", "HOD Details", "Courses Details"]
    combobox_choice = ttk.Combobox(department_window, values=choices, state="readonly")
    combobox_choice.grid(row=1, column=1, padx=5, pady=5)
    combobox_choice.current(0)

    # Submit button
    submit_button = ttk.Button(department_window, text="Submit", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Text widget for displaying result
    result_text = tk.Text(department_window, wrap="word", height=15, width=60)
    result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    result_text.config(state="disabled")

    department_window.mainloop()
