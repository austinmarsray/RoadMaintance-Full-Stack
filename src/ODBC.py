#############################################################################################
import pyodbc
#############################################################################################

#############################################################################################
def connect_to_database(level):
    global conn
    if level == 1:
        conn.close()
        conn = pyodbc.connect(DSN='SQL',UID='sa',pwd='5202020l')
    elif level == 2:
        conn.close()
        conn = pyodbc.connect(DSN='SQL',UID='admin',pwd='admin')
    elif level == 3:
        conn.close()
        conn = pyodbc.connect(DSN='SQL',UID='',pwd='')
#############################################################################################