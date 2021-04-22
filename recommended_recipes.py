import psycopg2
import ast
from datetime import datetime


conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from public.users")


def recommending_recipes(recipe_id):
    """Recommended to you: Recipes made by other users who make the same recipes.
       The recipes will be sorted by rating (from high to low)"""

    cur.execute("SELECT name, recipe_id, rating, description FROM public.recipe WHERE recipe_id IN "
                "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id IN "
                "(SELECT user_id FROM public.rating WHERE recipe_id = %s)) "
                "GROUP BY name, recipe_id, rating, description ORDER BY MAX(rating) DESC", (recipe_id,))

    recipe_info = cur.fetchall()

    print("\n--------------------------")
    print("|   Recommended to you   |")
    print("--------------------------\n")
    print("   %-64s %-15s %-20s %-5s" % ("Recipe Name", "Recipe ID", "Average Rating", "Description"))
    print("-----------------------------------------------------------------------------------------------"
          "------------------------------------------------------------------------------------------------"
          "------------------------------------------------------------------------------------------------")

    num = 1
    if recipe_info is not None and len(recipe_info) > 0:
        for info in recipe_info:
            print("%-1s %-65s %-20s %-14s %-5s" % (str(num) + ".", info[0], info[1], info[2], info[3]))
            num += 1
    else:
        print(" No recommended recipes yet!")


# def main():
#     recipe_id = "21132"
#     recommending_recipes(recipe_id)
#
#
# main()
