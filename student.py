import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cx_Oracle
from tabulate import tabulate

def extract_student_data(connection):
    def on_submit():
        reg_no = entry_reg_no.get()
        choice = combobox_choice.get()
        print(reg_no, choice)
        if not (reg_no and choice):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        sql_query = ""

        if choice == 'Student Details':
            sql_query =  f"SELECT * FROM Student WHERE Reg_no  = '{reg_no}'"
        elif choice == 'Department Details':
            sql_query = f"""
                        SELECT Department.Department_Code, Department.Department_Name
                        FROM Student
                        JOIN Studies_in ON Student.Reg_No = Studies_in.Reg_No
                        JOIN Course ON Studies_in.Course_ID = Course.Course_ID
                        JOIN Teaches ON Course.Course_ID = Teaches.Course_ID
                        JOIN Department ON Teaches.Department_Code = Department.Department_Code
                        WHERE Student.Reg_No = '{reg_no}'
                        """
        elif choice == 'Fees Details':
            sql_query = f"""
                        SELECT Fees.Course_ID, Fees.Fees_paying_Amount, Fees.Receipt_ID
                        FROM Student
                        JOIN Pays ON Student.Reg_No = Pays.Reg_No
                        JOIN Fees ON Pays.Receipt_ID = Fees.Receipt_ID
                        WHERE Student.Reg_No  = '{reg_no}'
                        """
        print(sql_query)
        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            student_data = cursor.fetchall()

            headers = []
            if choice == 'Student Details':
                headers = ["Student ID", "Reg No", "Student Name", "Age", "Gender", "Phone Number", "Email"]
            elif choice == 'Department Details':
                headers = ["Department Code", "Department Name"]
            elif choice == 'Fees Details':
                headers = ["Course ID", "Fees Paying Amount", "Receipt ID"]

            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, tabulate(student_data, headers=headers, tablefmt="grid"))
            result_text.config(state="disabled")

            cursor.close()

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return

    # Create a new window for student data extraction
    student_window = tk.Toplevel()
    student_window.title("Student Data Extraction")

    # Reg No label and entry
    label_reg_no = ttk.Label(student_window, text="Enter Registration Number:")
    label_reg_no.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_reg_no = ttk.Entry(student_window)
    entry_reg_no.grid(row=0, column=1, padx=5, pady=5)

    # Choice label and combobox
    label_choice = ttk.Label(student_window, text="Choose an option:")
    label_choice.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    choices = ["Student Details", "Department Details", "Fees Details"]
    combobox_choice = ttk.Combobox(student_window, values=choices, state="readonly")
    combobox_choice.grid(row=1, column=1, padx=5, pady=5)
    combobox_choice.current(0)

    # Submit button
    submit_button = ttk.Button(student_window, text="Submit", command=on_submit)
    submit_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Text widget for displaying result
    result_text = tk.Text(student_window, wrap="word", height=15, width=60)
    result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    result_text.config(state="disabled")

    student_window.mainloop()
