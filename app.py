from modules import tdmsql
import pyodbc

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-5B4BMPN;DATABASE=master;UID=tms;PWD=tms')

whole = tdmsql.tdm_get_list_tuple_test_db(cnxn)
print(whole)
whole_new = []
for toople in whole:
    print(toople[0])
    tit = (toople[0], toople[1], toople[2])
    print(tit)
    whole_new.append(tit)

print(False is False)

stri = "palec"
dick = ""
for i, char in enumerate(stri):
    if i < len(stri) - 1:
        dick = dick + char
print(dick)