import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cx_Oracle
from tabulate import tabulate

def extract_course_data(connection):
    def on_submit():
        course_id = entry_course_id.get()
        choice = combobox_choice.get()

        if not (course_id and choice):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        sql_query = ""

        if choice == 'Course Details':
            # Course Details
            sql_query = f"SELECT * FROM Course WHERE Course_ID = '{course_id}'"
            table_name = "Course"
        elif choice == 'Faculties Teaching It':
            sql_query = f"""SELECT Faculty.Faculty_ID, Faculty.Faculty_Name, Faculty.Phone_Number 
                           FROM Faculty 
                           INNER JOIN Teaches ON Faculty.Faculty_ID = Teaches.Faculty_ID 
                           WHERE Teaches.Course_ID  = '{course_id}'"""
            table_name = "Faculty"
        elif choice == 'Fees Details':
            sql_query = f"""SELECT Course.Course_ID, Course.Course_Name, Fees.Fees_Paying_Amount 
                           FROM Course
                           INNER JOIN Fees ON Course.Course_ID = Fees.Course_ID
                           WHERE Course.Course_ID = '{course_id}'"""
            table_name = "Fees"
        else:
            messagebox.showerror("Error", "Invalid choice!")
            return

        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            course_data = cursor.fetchall()

            headers = []
            if choice == 'Course Details':
                headers = ["Course ID", "Course Name", "Availability"]
            elif choice == 'Faculties Teaching It':
                headers = ["Faculty ID", "Faculty Name", "Phone Number"]
            elif choice == 'Fees Details':
                headers = ["Course ID", "Course Name", "Fees"]

            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Data from {table_name} table:\n")
            result_text.insert(tk.END, tabulate(course_data, headers=headers, tablefmt="grid"))
            result_text.config(state="disabled")

            cursor.close()

        except cx_Oracle.Error as error:
            messagebox.showerror("Error", str(error))
            return

    # Create a new window for course data extraction
    course_window = tk.Toplevel()
    course_window.title("Course Data Extraction")

    # Course ID label and entry
    label_course_id = ttk.Label(course_window, text="Enter Course ID:")
    label_course_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_course_id = ttk.Entry(course_window)
    entry_course_id.grid(row=0, column=1, padx=5, pady=5)

    # Choice label and combobox
    label_choice = ttk.Label(course_window, text="Choose an option:")
    label_choice.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    choices = ["Course Details", "Faculties Teaching It", "Fees Details"]
    combobox_choice = ttk.Combobox(course_window, values=choices, state="readonly")
    combobox_choice.grid(row=1, column=1, padx=5, pady=5)
    combobox_choice.current(0)

    # Submit button
    submit_button = ttk.Button(course_window, text="Submit", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Text widget for displaying result
    result_text = tk.Text(course_window, wrap="word", height=15, width=60)
    result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    result_text.config(state="disabled")

    course_window.mainloop()
