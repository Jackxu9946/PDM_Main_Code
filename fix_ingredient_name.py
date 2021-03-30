import psycopg2
import csv
import ast
import random

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSnnyGJSvn",
)

cur = conn.cursor()

aisle = '1'

cur.execute("SELECT id from recipe_manager.ingredients WHERE aisle = %s" ,(aisle,))
result = cur.fetchall()
print(len(result))
print(result)

