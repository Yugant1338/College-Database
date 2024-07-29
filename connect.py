import cx_Oracle

def connect_to_db(username, password):
    try:
        connection = cx_Oracle.connect(username, password)
        return connection
    except cx_Oracle.DatabaseError as e:
        print("Error:", e)
        return None
