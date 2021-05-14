import psycopg2
from termcolor import cprint as prnt

# login
con = psycopg2.connect(dbname='psql_db', user='artem', password='password', host='localhost')
cursor = con.cursor()

def get_all_files():
	cursor.execute("SELECT name FROM files;")
	con.commit()
	try:
		responce = cursor.fetchall()
		rows = []
		for row in responce:
			rows.append(row)
	except:
		pass
	for i, j in enumerate(rows):
		cursor.execute(f"SELECT lo_export(files.file, '/mnt/c/Users/artte/Desktop/FileCloud/user_files/{j}') FROM files WHERE id = {i+1};")
	cursor.close()
	con.close()
