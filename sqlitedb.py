import sqlite3
from sqlite3 import Error

def create_database():
	conn = None
	try:
		conn = sqlite3.connect("data.sqlite")
		return conn
	except Error as e:
		print(e)
	return conn

def create_table(conn):
	try:
		cur = conn.cursor()
		table = """CREATE TABLE IF NOT EXISTS data (
			council_reference VARCHAR(20) PRIMARY KEY,
			address TEXT,
			council TEXT,
			description TEXT,
			info_url TEXT,
			date_scraped DATE,
			on_notice_from DATE,
			on_notice_to DATE
			);"""
		cur.execute(table)
		# print("Table created")
	except Error as e:
		print(e)
		
def update_table(conn):
	try:
		cur = conn.cursor()
		q = """ ALTER TABLE data
				ADD COLUMN on_notice_from DATE;
				"""
		cur.execute(q)
		# print("Column added")
	except Error as e:
		print(e)
	try:
		q = """ ALTER TABLE data
				ADD COLUMN on_notice_to DATE;
				"""
		cur.execute(q)
		# print("Column added")
	except Error as e:
		print(e)

def store_data(data, conn):
	# replace if exists
	sql = """	INSERT OR REPLACE INTO data(council_reference, address, council, description, info_url, date_scraped, on_notice_from, on_notice_to)
				VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

