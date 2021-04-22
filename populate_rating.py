import psycopg2
import csv
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

filename = "/Users/xinruzou/Downloads/archive/RAW_interactions.csv"

with open(filename, 'r', encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    num = 0
    for row in csvreader:
        # print("user_id " + row[0])
        # print("recipe_id " + row[1])
        # print("date " + row[2])
        # print("rating " + row[3])
        # print("review " + row[4])
        try:

            cur.execute("SELECT * FROM public.recipe WHERE recipe_id = %s", (row[1],))
            r = cur.fetchall()
            if r is not None and len(r) != 0:
                cur.execute("INSERT INTO public.rating(user_id, recipe_id, rating, rating_date, review_text) "
                            "VALUES( %s, %s, %s, %s, %s)", (row[0], row[1], row[3], row[2], row[4]))
                cur.execute("UPDATE public.recipe SET marked = %s WHERE recipe_id = %s", ('1', row[1]))
                print("success")
                conn.commit()
            else:
                print("recipe of rating not exist")

        except:
            print("Error")
