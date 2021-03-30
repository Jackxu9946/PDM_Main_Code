import psycopg2
import csv
import ast
import random

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from public.users")


#filename = "/Users/xinruzou/Downloads/archive/new_pp_recipe.csv"
#filename2 = "/Users/xinruzou/Downloads/archive/new_recipe_raw.csv"


filename = "new_pp_recipe.csv"
filename2 = "new_recipe_raw.csv"

with open(filename, 'r', encoding="utf8") as csvfile:
    with open(filename2, 'r', encoding="utf8") as csvfile2:
        print("1")

        csvreader = csv.reader(csvfile)
        csvreader2 = csv.reader(csvfile2)

        next(csvreader)
        next(csvreader2)
        for rows in csvreader:


            recipe_id = rows[0]
            # print(recipe_id)
            ingredients = ast.literal_eval(rows[7])

            # check if the recipe exist in the recipe table.
            cur.execute("SELECT * FROM public.recipe WHERE recipe_id = %s", (recipe_id,))
            exist = cur.fetchall()
            if not exist:
                continue
            else:
                for position in range(len(ingredients)):

                    cur.execute("SELECT * FROM public.ingredients WHERE id = %s"
                                , (ingredients[position],))

                    ingredients_exist = cur.fetchall()
                    # this ingredient does not exist in ingredient table
                    if not ingredients_exist:
                        # loop over the rows in the second file
                        for rows2 in csvreader2:
                            if rows2[1] == recipe_id:
                                int1 = ast.literal_eval(rows2[10])
                                ingredient_name = int1[position]
                                print(ingredient_name)
                                print("Insert Ingredient")
                                cur.execute("INSERT INTO public.ingredients(id, name, aisle) "
                                            "VALUES( %s, %s, %s)", (ingredients[position], ingredient_name, "1"))
                                conn.commit()
                                break

                    # ingredient already exist

                    cur.execute("SELECT * FROM public.ingredient_to_recipe WHERE recipe_id = %s AND ingredient = %s"
                                "", (recipe_id, ingredients[position]))
                    result = cur.fetchall()
                    if not result:

                        cur.execute("INSERT INTO public.ingredient_to_recipe(recipe_id, ingredient) "
                                "VALUES( %s, %s)", (recipe_id, ingredients[position]))
                        # print("success")
                        conn.commit()
                    else:
                        a = 1
                        # print("already exist")
