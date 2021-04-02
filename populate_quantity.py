import psycopg2
import ast
from datetime import datetime
import random

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

num = random.randint(1, 50)

cur.execute("SELECT * from public.ingredient_to_recipe WHERE ingredient_quantity = %s ", ())
