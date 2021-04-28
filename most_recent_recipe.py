import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()


def most_recent_recipe():
    """
    Get the 50 most recent recipes made order by creation date.
    """

    cur.execute("SELECT name, recipe_id, rating, creation_date, description FROM public.recipe "
                "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC LIMIT 50 ")

    results = cur.fetchall()

    print("--------------------------------")
    print("|     50 Most Recent Recipes     |")
    print("---------------------------------\n")
    print("     %-64s %-15s %-22s %-28s %-5s" % ("Recipe Name", "Recipe ID", "Average Rating", "Creation Date", "Description"))
    print("------------------------------------------------------------------------------------------"
          "----------------------------------------------------------"
          "----------------------------------------------------------------------------------------\n")

    if results is not None and len(results) > 0:
        num = 1

        for result in results:
            r = result[4].split("\n")
            count = 0
            for i in r:
                if count == 0:
                    print("%-4s %-65s %-20s %-14s %-30s %-5s" %
                          (str(num) + ".", result[0], result[1], result[2], result[3], i))
                    count += 1
                else:
                    print("%-4s %-65s %-20s %-14s %-30s %-5s" % ("", "", "", "", "", i))
            num += 1
    else:
        print("No results found")


def update_rating():
    """
    Update the average rating in the recipe table for the newly populated data into the rating table
    :return:
    """
    cur.execute("SELECT DISTINCT recipe_id FROM public.rating")
    result = cur.fetchall()

    for i in result:
        i = str(i)
        i = i[1:-2]
        cur.execute("SELECT rating from public.rating WHERE recipe_id = %s", (i,))
        r = cur.fetchall()
        sum1 = 0
        count = 0
        for a in r:
            a = str(a)
            a = a[10:11]
            a = int(a)
            sum1 += a
            count += 1
        rating = int(round(sum1 / count, 0))
        cur.execute("UPDATE public.recipe SET rating = %s WHERE recipe_id = %s", (rating, i))
        conn.commit()


def top_50_recommended_recipe():
    print("----------------------------------------")
    print("|     Top 50 Most Recommended Recipes     |")
    print("-----------------------------------------\n")
    print(" %-92s %-18s %-17s %2s" % ("Recipe Name", "Recipe ID", "Rating", "Description"))
    print("---------------------------------------------------------------------------------------------------"
          "----------------------------------------------------------------------------------------"
          "--------------------")
    cur.execute("SELECT name, recipe_id,rating,description FROM public.recipe "
                "GROUP BY name, recipe_id,rating, description ORDER BY MAX(rating) DESC LIMIT 50 ")
    results = cur.fetchall()
    num = 1

    for result in results:
        r = result[3].split("\n")
        count = 0
        for j in r:
            if count == 0:
                print("%-3s %-90s %-20s %-13s %-10s" % (str(num) + ".", result[0], result[1], result[2], j))
                count += 1

            else:
                print("%-3s %-90s %-20s %-13s %-10s" % ("" + "", "", "", "",j))
        num += 1


def most_popular_ingredients():
    print("----------------------------------------")
    print("|     Most Popular Ingredients      |")
    print("-----------------------------------------\n")
    print(" %-92s %-18s %-2s" % ("Ingredient Name", "Ingredient ID", "Quantity"))
    print("---------------------------------------------------------------------------------------------------"
          "-------------------------")
    '''
    cur.execute("SELECT recipe_id FROM public.recipe "
                "GROUP BY recipe_id, rating ORDER BY MAX(rating) DESC LIMIT 50 ")
    '''
    cur.execute("SELECT recipe_id FROM public.recipe GROUP BY recipe_id")
    recipes = cur.fetchall()

    ingredient_dict = {}

    for r in recipes:
        cur.execute("SELECT name FROM public.ingredient_to_recipe WHERE recipe_id = %s", r)
        ingredients = cur.fetchall()
        for i in ingredients:
            num = 0
            if i[num] in ingredient_dict.keys():
                ingredient_dict[i[num]] += 1
            else:
                ingredient_dict[i[num]] = 1
            num += 1

    l = list(ingredient_dict.values())
    for key in ingredient_dict:
        print(key, ingredient_dict[key])


def most_popular_ingredients_by_year():
    print("----------------------------------------")
    print("|     Most Popular Ingredients      |")
    print("-----------------------------------------\n")
    print(" %-92s %-18s %-2s" % ("Ingredient Name", "Ingredient ID", "Quantity"))
    print("---------------------------------------------------------------------------------------------------"
          "-------------------------")

    cur.execute("SELECT recipe_id FROM public.rating "
                "WHERE rating_date >= '2019-01-01 00:00:00' AND rating_date < '2020-01-01 00:00:00'")
    recipes = cur.fetchall()

    ingredient_dict = {}

    for r in recipes:
        cur.execute("SELECT name FROM public.ingredient_to_recipe WHERE recipe_id = %s", r)
        ingredients = cur.fetchall()
        for i in ingredients:
            num = 0
            if i[num] in ingredient_dict.keys():
                ingredient_dict[i[num]] += 1
            else:
                ingredient_dict[i[num]] = 1
            num += 1

    for key in ingredient_dict:
        print(key, ingredient_dict[key])



def match_name_to_id():
    cur.execute("SELECT name from public.pantry")
    result = cur.fetchall()
    num = 0
    for i in result:
        name = i[0]
        # get the id from the ingredient table
        cur.execute("SELECT id from public.ingredients WHERE name = %s", (name,))
        id = cur.fetchone()
        id1 = id[0]
        # update the id in the ingredient_to_recipe
        cur.execute("UPDATE public.pantry SET ingredient_id = %s WHERE name = %s", (id1, name))
        print(num)
        num += 1

    conn.commit()
    print("success")


def print_most_recent_recipe(results):
    """
    Get the 50 most recent recipes made order by creation date.
    @result fetchall result of recipes' informations
    """

    print("\n------------------------")
    print("|    Result Recipe     |")
    print("------------------------\n")
    print("     %-64s %-15s %-22s %-28s %-5s" % ("Recipe Name", "Recipe ID", "Average Rating", "Creation Date", "Description"))
    print("------------------------------------------------------------------------------------------"
          "----------------------------------------------------------"
          "----------------------------------------------------------------------------------------\n")

    if results is not None and len(results) > 0:
        num = 1

        for result in results:
            r = result[4].split("\n")

            count = 0
            for i in r:
                if count == 0:
                    print("%-4s %-65s %-20s %-14s %-30s %-5s" % (str(num) + ".", result[0], result[1], result[2], result[3], i))
                    count += 1
                else:
                    print("%-4s %-65s %-20s %-14s %-30s %-5s" % ("", "", "", "", "", i))
            num += 1
    else:
        print("No results found")


def add_name_to_ingredient_to_recipe():
    cur.execute("SELECT ingredient from public.ingredient_to_recipe ")
    result = cur.fetchall()
    for i in result:
        print(i[0])
        id = i[0]
        id = str(id)
        cur.execute("SELECT name from public.ingredients WHERE id = %s", (id,))
        name = cur.fetchone()
        if name is None or len(name) == 0:
            cur.execute("DELETE FROM public.ingredient_to_recipe WHERE ingredient = %s", (id,))
            conn.commit()
        else:
            # print("name ", name[0])
            cur.execute("UPDATE public.ingredient_to_recipe SET name = %s WHERE ingredient = %s", (name[0], id))
            conn.commit()
