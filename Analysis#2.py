import psycopg2
from datetime import datetime
import ast
import json
from matplotlib import pyplot as plt
import csv
import numpy as np

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)
cur = conn.cursor()
#Find a relationship between rating and cooktime possibly
#Find all recipe with rating > 0
valid_recipe_id = []

def find_all_rating_greater_than_zero():
    cur.execute("SELECT recipe_id,cook_time,rating from public.recipe where rating > 0")
    all_selected = cur.fetchall()
    rating_to_cooktime_average = {1:0, 2:0, 3:0, 4:0, 5:0}
    counter_dict = {1:0,2:0,3:0,4:0,5:0}
    for value in all_selected:
        recipe_id = value[0]
        cook_time = value[1]
        rating = value[2]
        cook_time = int(cook_time)
        rating = int(rating)
        rating_to_cooktime_average[rating] += cook_time
        counter_dict[rating] += 1
    for key in rating_to_cooktime_average:
        rating_to_cooktime_average[key] = rating_to_cooktime_average[key] / counter_dict[key]
    print(rating_to_cooktime_average)

cook_time_average_dict = {1: 72.5, 2: 193.0, 3: 42.833333333333336, 4: 33.69230769230769, 5: 67.625}
cook_time_ar = [72.5,193,43,34,68]
rating_ar = [1,2,3,4,5]

fig = plt.figure()
plt.bar(rating_ar, cook_time_ar, width=0.4)
plt.xlabel("Rating")
plt.ylabel("Average Cooktime(Minute)")
plt.title("Relationship between cooktime and rating")
plt.show()




# find_all_rating_greater_than_zero()
#def put_everything_into_category:

# m,b = np.polyfit(rating_ar,cooktime_ar,1)
# plt.plot(rating_ar, cooktime_ar, 'o')
# plt.plot(rating_ar, m*rating_ar + b)
# plt.show()


#find_all_rating_greater_than_zero()