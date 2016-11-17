from sqlalchemy import create_engine
import pyodbc
import pymssql
#engine = create_engine('mssql+pymssql://sa:123@(localhost)\SQLEXPRESS/housing')
#conn = pymssql.connect(server=r'(localhost)\SQLEXPRESS' , user='sa', password='123', database='housing')
cnxn = pyodbc.connect(r'DSN=localhost;UID=sa;PWD=123')

# print(engine)