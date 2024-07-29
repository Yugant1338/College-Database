import cx_Oracle
from tabulate import tabulate
import time
def extract_faculty_data(connection):
    faculty_id = input('Enter the Faculty ID: ')
    print('1. Faculty Details\n2. Teaches\n3. Department Details\n4. Is HOD')
    choice = input('Enter your choice: ')
    time.sleep(3)
    sql_query = ""

    if choice == '1':
        sql_query = "SELECT * FROM Faculty WHERE Faculty_ID = '{0}'".format(faculty_id)
    elif choice == '2':
        sql_query = """
                    SELECT Course.Course_ID, Course.Course_Name
                    FROM Teaches
                    JOIN Course ON Teaches.Course_ID = Course.Course_ID
                    WHERE Teaches.Faculty_ID = '{0}'
                    """.format(faculty_id)
    elif choice == '3':
        sql_query = """
                    SELECT Department.Department_Code, Department.Department_Name
                    FROM Department
                    JOIN Faculty ON Department.HOD = Faculty.Faculty_ID
                    WHERE Faculty.Faculty_ID = '{0}'
                    """.format(faculty_id)
    elif choice == '4':
        sql_query = "SELECT HOD FROM Department WHERE HOD = '{0}'".format(faculty_id)
    else:
        print("Invalid choice. Please enter a valid choice (1, 2, 3, or 4).")
        return

    print("SQL Query:", sql_query)

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        faculty_data = cursor.fetchall()

        headers = []
        if choice == '1':
            headers = ["Faculty ID", "Faculty Name", "Phone Number"]
        elif choice == '2':
            headers = ["Course ID", "Course Name"]
        elif choice == '3':
            headers = ["Department Code", "Department Name"]
        elif choice == '4':
            headers = ["Is HOD"]

        print(tabulate(faculty_data, headers=headers, tablefmt="grid"))
        cursor.close()

    except cx_Oracle.DatabaseError as e:
        print("Error:", e)
        return None
