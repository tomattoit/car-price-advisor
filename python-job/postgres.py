import psycopg2
from psycopg2 import sql

db_params = {
    'host': 'postgres',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'password'
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
query = sql.SQL("SELECT * FROM {}").format(sql.Identifier('people'))
cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
