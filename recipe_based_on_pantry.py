import psycopg2
from datetime import datetime
import ast
import json
from Recipe import print_my_recipe

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

#Find all the recipe that the user is able to make
def find_recipe_based_on_pantry(user_id):
    cur.execute(
        "select recipe_id, string_agg(ingredient::text ,',' order by ingredient),"
	    "string_agg(ingredient_quantity::text, ',' order by ingredient)"
	    "from public.ingredient_to_recipe where recipe_id in ("
	    "select recipe_id from public.ingredient_to_recipe where ingredient in ("
		"select ingredient_id from public.pantry where user_id = %s)"
	    ") GROUP BY recipe_id;", (user_id,))
    all_recipe_that_matches_user_pantry = cur.fetchall()
    cur.execute("select ingredient_id,current_quantity from public.pantry where user_id = %s", (user_id,))
    user_pantry = cur.fetchall()
    user_pantry_dictionary = {}
    for item in user_pantry:
        user_pantry_dictionary[item[0]] = int(item[1])
    #print(user_pantry_dictionary)
    valid_user_recipe = []
    #Go through each recipe
    for recipe_index in range(len(all_recipe_that_matches_user_pantry)):
        recipe_id = all_recipe_that_matches_user_pantry[recipe_index][0]
        list_of_ingredient_id = all_recipe_that_matches_user_pantry[recipe_index][1]
        list_of_ingredient_quantity = all_recipe_that_matches_user_pantry[recipe_index][2]
        list_of_ingredient_id += ","
        list_of_ingredient_quantity += ","
        list_of_ingredient_id = list_of_ingredient_id.split(",")[:-1]
        list_of_ingredient_quantity = list_of_ingredient_quantity.split(",")[:-1]
        valid_recipe = True
        for ingredient_index in range(len(list_of_ingredient_id)):
            current_ingredient_id = int(list_of_ingredient_id[ingredient_index])
            current_ingredient_quantity = int(list_of_ingredient_quantity[ingredient_index])
            #Check if the ingredient is in the user pantry
            if (not current_ingredient_id in user_pantry_dictionary):
                valid_recipe = False
                break
            else:
                if (current_ingredient_quantity > user_pantry_dictionary[current_ingredient_id]):
                    valid_recipe = False
                    break
        if (valid_recipe):
            valid_user_recipe.append(recipe_id)
    valid_user_recipe = tuple(valid_user_recipe)
    if (len(valid_user_recipe) == 0):
        print("Can not find any recipe that matches your pantry")
        return
    cur.execute("select (name, recipe_id,rating, description) from public.recipe where recipe_id in %s order by rating DESC ", (valid_user_recipe,))
    display_recipe_values = cur.fetchall()
    if (display_recipe_values != None and len(display_recipe_values) > 0):
        print_my_recipe(display_recipe_values)



# find_recipe_based_on_pantry(7706)