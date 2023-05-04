import random
import datetime
import sqlite3 
from sqlite3 import Error

NAMES = ['Jerin Thomas', 'User 1', 'User 2', 'User 3', 'User 4', 'User 5', 'User 6', 'User 7', 'User 8', 'User 9', 'User 10', 'User 11', 'User 12', 'User 13', 'User 14', 'User 15', 'User 16', 'User 17', 'User 18', 'User 19', 'User 20']
DEPARTMENTS = ['Management', 'Marketing', 'Finance','SDE I', 'SDE II', 'HR', 'BA']
DATABASE = "database.db"
TABLE_NAME = "employee"

def sql_connection():
	try:
		conn = sqlite3.connect(DATABASE)
		return conn
	except Exception as e:
		print(f"Error while connecting to DB : {e}")
		return None
 
def create_table(conn):
	cur = conn.cursor()
	query = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name CHAR(50) NOT NULL, 
		department CHAR(50), 
		salary decimal(7,2), 
		hire_date CHAR(20) )"""
	cur.execute(query)
	conn.commit()

def insert_data(conn):
	process_records = True
	cur = conn.cursor()
	data = sql_read(conn)
	for i in data:
		if 'Jerin Thomas' in i:
			print(f"Table and data exists > {TABLE_NAME}")
			process_records = False
			break
	if process_records:
		for index, name in enumerate(NAMES, 1):
			id = 1000 + index
			department = random.choice(DEPARTMENTS)
			salary = round(random.uniform(0, 1000000), 2)
			hire_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365*3))
			query = f"INSERT INTO {TABLE_NAME} VALUES('{id}','{name}','{department}','{salary}','{hire_date}')"
			cur.execute(query)
			conn.commit()	
		print(f"Table and data inserted > {TABLE_NAME}")

def sql_read(conn):  
	cursor = conn.execute(f"SELECT * from {TABLE_NAME}")
	data = cursor.fetchall()
	return data

def initialize():
	conn = sql_connection()
	if conn:
		create_table(conn)
		insert_data(conn)
		data = sql_read(conn)
		# print(f"{data = }")
	conn.close()