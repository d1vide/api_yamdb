import csv, sqlite3

con = sqlite3.connect(r'C:\Dev\api_yamdb\api_yamdb\db.sqlite3')
cur = con.cursor()

with open(r'..\static\data\category.csv', 'r',
        #   C:\Dev\api_yamdb\api_yamdb\utils\xlsToSqlite.py
          encoding='utf-8-sig') as file:
    contents = csv.reader(file)
    fields = next(contents)
    insert_query = f"INSERT INTO reviews_category ({', '.join(fields)}) VALUES(?, ?, ?)"
    cur.executemany(insert_query, contents)

con.commit()
con.close()
