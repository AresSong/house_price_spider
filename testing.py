from sqlalchemy import create_engine
import pymssql
import pyodbc
engine = create_engine('mssql+pymssql://hosxh@song:AR6509749es@song.database.windows.net/housing')

server = dict()

server["hostname"] = 'song.database.windows.net'
server["db_user"] = "hosxh@song"
server["db_password"] = "AR6509749es"

# conn = pymssql.connect(server='song.database.windows.net', port = '1433', tds_version='7.3', user='hosxh@song', password='AR6509749es', database='housing')
# conn = pymssql.connect(server=server["hostname"], user=server["db_user"] , password=server["db_password"] , database='housing')
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER= song.database.windows.net;DATABASE=housing;UID=hosxh@song;PWD=AR6509749es')

cursor = cnxn.cursor()
# cursor.tables()
# cursor.execute('''
#                     CREATE TABLE dbo.load_listings
#                     (
#                     bathroom INT,
#                     bedroom INT,
#                     ensuite INT,
#                     carpark INT,
#                     city    NVARCHAR(50),
#                     floor_area DECIMAL(18,2),
#                     land_area DECIMAL(18,2),
#                     incorrect_address NVARCHAR(500),
#                     listed_datetime DATETIME,
#                     price   DECIMAL(18,2),
#                     property_description nvarchar(max),
#                     property_type NVARCHAR(100),
#                     region  NVARCHAR(50),
#                     sell_type NVARCHAR(50),
#                     seller  NVARCHAR(200),
#                     snapshot_datetime DATETIME,
#                     source  NVARCHAR(50),
#                     street  NVARCHAR(100),
#                     suburb  NVARCHAR(200),
#                     title   NVARCHAR(200),
#                     url     NVARCHAR(500)
#                     )
#             ''')

cursor.execute('''SELECT * FROM SYS.tables''')
for row in cursor.fetchall():
    print(row)
# cursor.close()

# cnxn.commit()
# Driver={ODBC Driver 13 for SQL Server};Server=tcp:song.database.windows.net,1433;Database=housing;Uid=hosxh@song;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;