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
                    print("%-4s %-65s %-20s %-14s %-30s %-5s" % (
                    str(num) + ".", result[0], result[1], result[2], result[3], i))
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
    print(" %-92s %-18s %-2s" % ("Recipe Name", "Recipe ID", "Rating"))
    print("---------------------------------------------------------------------------------------------------"
          "-------------------------")
    cur.execute("SELECT name, recipe_id,rating FROM public.recipe "
                "GROUP BY name, recipe_id,rating ORDER BY MAX(rating) DESC LIMIT 50 ")
    result = cur.fetchall()
    num = 1
    for i in result:
        print("%-3s %-90s %-20s %-2s" % (str(num) + ".", i[0], i[1], i[2]))
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
            # print(i[num])
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

    # creation_date = ["1999", "2000", "2001"]
    cur.execute("SELECT creation_date FROM public.recipe WHERE creation_date BETWEEN 1999 AND 2000")
    recipes = cur.fetchall()

    ingredient_dict = {}

    for r in recipes:
        # cur.execute("SELECT name FROM public.ingredient_to_recipe WHERE recipe_id = %s", r)
        # ingredients = cur.fetchall()
        print(r)
        '''
        for i in ingredients:
            num = 0
            # print(i[num])
            if i[num] in ingredient_dict.keys():
                ingredient_dict[i[num]] += 1
            else:
                ingredient_dict[i[num]] = 1
            num += 1
        '''

    '''
    l = list(ingredient_dict.values())
    for key in ingredient_dict:
        print(key, ingredient_dict[key])
    '''


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


# print_most_recent_recipe("apple")


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


def test():
    cur.execute("SELECT ingredient_id, current_quantity FROM public.pantry WHERE user_id = 7706")
    r = cur.fetchall()
    pantry_dic = {}
    for i in r:
        pantry_dic[i[0]] = i[1]

    print("ingredients in pantry:", r, "\n")
    # t1.ingredient, t2.current_quantity, t1.ingredient_quantity
    cur.execute("SELECT DISTINCT t1.recipe_id "
                "FROM public.ingredient_to_recipe AS t1 "
                "INNER JOIN public.pantry AS t2 "
                "ON t1.ingredient = t2.ingredient_id "
                "AND t2.user_id = 7706 WHERE t2.current_quantity >= t1.ingredient_quantity")

    possible_recipes = cur.fetchall()
    print("possible recipes", possible_recipes)

    l = []
    for i in possible_recipes:
        flag = True
        recipe_id = i[0]
        cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = %s",
                    (recipe_id,))
        all_ingredient = cur.fetchall()
        recipe_dic = {}
        for j in all_ingredient:
            recipe_dic[j[0]] = j[1]
        for k in recipe_dic.keys():
            if k not in pantry_dic.keys():
                flag = False
                break
            else:
                if pantry_dic[k] >= recipe_dic[k]:
                    continue
        if flag:
            l.append(i)

    print("l", l)

    cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = 26")
    s = cur.fetchall()
    print("\ningredients needed for recipe 26")
    print(s)

    cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = 35")
    k = cur.fetchall()
    print("\ningredients needed for recipe 35")
    print(k)

    cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = 37")
    j = cur.fetchall()
    print("\ningredients needed for recipe 37")
    print(j)

    cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = 39")
    m = cur.fetchall()
    print("\ningredients needed for recipe 39")
    print(m)

    cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = 41")
    m = cur.fetchall()
    print("\ningredients needed for recipe 41")
    print(m)

    cur.execute("SELECT ingredient, ingredient_quantity from public.ingredient_to_recipe WHERE recipe_id = 37313")
    n = cur.fetchall()
    print("\ningredients needed for recipe 41")
    print(n)
