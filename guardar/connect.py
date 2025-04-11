import pyodbc
import pymssql

SERVER = '192.168.1.92'
USER = 'preciouser'
PASSWORD = 'preciouser#'
DATABASE = "DATA_PRECIO_MERCADO"


connection = pymssql.connect(host=SERVER, user=USER, 
                password=PASSWORD, database=DATABASE)

cursor = connection.cursor() # to access field as dictionary use cursor(as_dict=True)
#cursor.execute("SELECT * FROM Farmacias")
#row = cursor.fetchall()
#print(row)

# ######## INSERT DATA IN TABLE ########
#cursor.execute("""
#    INSERT INTO [prm_m_farmacias] (Id, NombFarm) VALUES  ('C', 'Cruz Verde')
#""")
# commit your work to database
#connection.commit()

######## ITERATE THROUGH RESULTS  ########
# cursor.execute("SELECT TOP 10 * FROM posts ORDER BY publish_date DESC")
# for row in cursor:
#     print(row)
#     # if you pass as_dict=True to cursor
#     # print(row["message"])
# connection.close()