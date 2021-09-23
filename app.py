import pyodbc, re

try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-5B4BMPN;DATABASE=master;UID=tms;PWD=tms')
    print("nice")
except:
    print("fuck")

cursor = cnxn.cursor()
cursor.execute("SELECT DISTINCT NAME FROM GENERIC1")
result = cursor.fetchall()
print(result)

pattern = re.compile(r'\'\w+\'')

for res in result:
    res = pattern.findall(str(res))
    res = re.sub('[^\w]+', '', res[0])
    print(res)