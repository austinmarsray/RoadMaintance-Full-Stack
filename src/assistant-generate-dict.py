import pyodbc

conn = pyodbc.connect(DSN='SQL',UID='sa',pwd='5202020l')
cursor = conn.cursor()
cursor.execute("select * from DamageType")
rows = cursor.fetchall()

for row in rows:
    print("'%s':'%s'"%(row.DamageName,row.DamageType))

for row in rows:
    print("'%s':'%s'"%(row.DamageType,row.DamageName))