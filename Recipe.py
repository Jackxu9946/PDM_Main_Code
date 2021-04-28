import psycopg2
from datetime import datetime
import most_recent_recipe

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)
cur = conn.cursor()

name = "davagagfa 12"
cook_time = "50"
description = "This is a test"
user_id = 1
steps = "123123131"
creation_date = datetime.today().strftime('%Y-%m-%d')


def create_recipe(name, cook_time, description, difficulty, servings, created_by, creation_date, steps, ingredients):
    try:
        cur.execute(
            "INSERT INTO public.recipe(name, cook_time, description, created_by, creation_date,steps, difficulty, "
            "servings) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, cook_time, description, created_by, creation_date, steps, difficulty, servings)
        )

        conn.commit()

        # Get the recipe_id and send it into an underlying function
        cur.execute(
            "Select (recipe_id) from public.recipe where created_by = %s and name = %s", (created_by, name)
        )

        recipe_id = int(cur.fetchone()[0])
        recipe_to_ingredient(recipe_id, ingredients)
        print("\nRecipe has been added successfully")
    except:
        print("Can not create new recipe")


def edit_recipe(name, cook_time, description, difficulty, servings, steps, recipe_id):
    try:
        if name is not None:
            cur.execute("UPDATE public.recipe SET name = %s WHERE recipe_id = %s", (name, recipe_id))

        if cook_time is not None:
            cur.execute("UPDATE public.recipe SET cook_time = %s WHERE recipe_id = %s", (cook_time, recipe_id))

        if description is not None:
            cur.execute("UPDATE public.recipe SET description = %s WHERE recipe_id = %s", (description, recipe_id))

        if difficulty is not None:
            cur.execute("UPDATE public.recipe SET difficulty = %s WHERE recipe_id = %s", (difficulty, recipe_id))

        if servings is not None:
            cur.execute("UPDATE public.recipe SET servings = %s WHERE recipe_id = %s", (servings, recipe_id))

        if steps is not None:
            cur.execute("UPDATE public.recipe SET steps = %s WHERE recipe_id = %s", (steps, recipe_id))

        conn.commit()
        print("\nRecipe has been updated successfully")
        return -1
    except:
        print("Unable to save recipe")
        return 1


def delete_recipe_with_error_checking(user_id, recipe_id):
    # Check if the recipe has been made
    cur.execute("SELECT * FROM public.rating WHERE recipe_id = %s LIMIT 1", (recipe_id,))
    result = cur.fetchall()
    if result is None or len(result) == 0:
        delete_recipe(user_id, recipe_id)
    else:
        print("Can not delete recipe because another user has already made it")


def delete_recipe(user_id, recipe_id):
    # No error checking happening here
    try:
        cur.execute("DELETE FROM public.recipe WHERE recipe_id= %s and created_by = %s", (recipe_id, user_id))
        cur.execute("DELETE FROM public.ingredient_to_recipe WHERE recipe_id = %s", (recipe_id,))
        cur.execute("DELETE FROM public.recipe_to_category WHERE recipe_id = %s", (recipe_id,))
        print("\nRecipe has been deleted successfully.")
        conn.commit()
    except:
        print("Can not delete entry in database")


# Return a list of recipe_name along with their ID
# Empty list = no recipe
def search_recipe_by_name(name, search_mode):
    # search_mode = rating
    # most_recent = when it was made
    if search_mode == "recent":
        try:
            cur.execute("SELECT name, recipe_id, rating, creation_date, description FROM public.recipe "
                        "WHERE name like '%%{name}%%' "
                        "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC".format(
                name=name))

            results = cur.fetchall()
            most_recent_recipe.print_most_recent_recipe(results)
        except:
            print("Can not execute the recipe query")

    elif search_mode == "rating":
        try:
            cur.execute(
                "SELECT name, recipe_id, rating, description FROM public.recipe "
                "WHERE name like '%%{name}%%' GROUP BY name, recipe_id, rating, description ORDER BY MAX(rating) DESC ".format(
                    name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")
    else:
        try:
            cur.execute(
                "SELECT name, recipe_id, rating, description FROM public.recipe "
                "WHERE name like '%%{name}%%' ORDER BY name ".format(name=name))
            results = cur.fetchall()
            return results

        except:
            print("Can not execute the recipe query")
    return None


def search_recipe_by_ingredient(ingredient, search_mode):
    # Get the ingredient ID
    # Assuming there is only one ingredient ID per name

    cur.execute("SELECT id FROM public.ingredients where name = %s", (ingredient,))

    ingredient_result = cur.fetchone()

    if ingredient_result is None:
        print("This ingredient does not exist in the database. Please check the name and try again")
        return
    ingredient_id = ingredient_result[0]

    if search_mode == "recent":
        try:
            cur.execute(
                "SELECT name, recipe_id, rating, creation_date, description from public.recipe where recipe_id IN "
                "(SELECT recipe_id from public.ingredient_to_recipe where ingredient = %s) "
                "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC",
                (ingredient_id,))

            result = cur.fetchall()
            most_recent_recipe.print_most_recent_recipe(result)
        except:
            print("Can not retrieve recipe")
    elif search_mode == "rating":
        try:
            cur.execute("SELECT name, recipe_id, rating, description from public.recipe where recipe_id IN "
                        "(SELECT recipe_id from public.ingredient_to_recipe where ingredient = %s) "
                        "GROUP BY name, recipe_id, rating, description ORDER BY MAX(rating) DESC", (ingredient_id,))
            result = cur.fetchall()
            return result
        except:
            print("Can not retrieve recipe")
    else:
        try:
            cur.execute(
                "SELECT name,recipe_id, rating, description from public.recipe where recipe_id IN "
                "(SELECT recipe_id from public.ingredient_to_recipe where ingredient = %s) order by name",
                (ingredient_id,))
            result = cur.fetchall()
            return result
        except:
            print("Can not retrieve recipe")


def search_recipe_by_category(category, search_mode):
    if search_mode == "recent":
        try:
            cur.execute(
                "SELECT name, recipe_id, rating, creation_date, description from public.recipe where recipe_id IN "
                "(SELECT recipe_id from public.recipe_to_category WHERE category_id IN "
                "(SELECT id from public.category WHERE name = %s)) "
                "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC ",
                (category,))

            result = cur.fetchall()
            most_recent_recipe.print_most_recent_recipe(result)
        except:
            print("Can not retrieve recipe")
    elif search_mode == "rating":
        try:
            cur.execute("SELECT name, recipe_id, rating, description from public.recipe WHERE recipe_id IN "
                        "(SELECT recipe_id from public.recipe_to_category WHERE category_id IN "
                        "(SELECT id from public.category WHERE name = %s)) "
                        "GROUP BY name, recipe_id, rating, description ORDER BY MAX(rating) DESC ", (category,))

            result = cur.fetchall()

            return result
        except:
            print("Can not retrieve recipe")
    else:
        try:
            cur.execute(
                "SELECT name,recipe_id, rating, description from public.recipe where recipe_id IN "
                "(SELECT recipe_id from public.recipe_to_category WHERE category_id IN "
                "(SELECT id from public.category WHERE name = %s)) "
                "GROUP BY name, recipe_id, rating, description ORDER BY name", (category,))
            result = cur.fetchall()
            return result
        except:
            print("Can not retrieve recipe")


# CATEGORY TEST SET UP
# User1 have category = Chinese User_id = 0 cateogory_id for chinese = 56
# User2 have category = Chinese User_id = 1 category_id for chinese = 57
# Recipe_id = 5289, created by user1
# Recipe_id = 8559, created by user2


def find_my_recipes(user_id):
    try:
        cur.execute("SELECT name, recipe_id,rating, description from public.recipe where created_by = %s", (user_id,))
        results = cur.fetchall()
        return results
    except:
        print("Can not retrieve recipe")


def print_my_recipe(results):
    print("\n------------------------")
    print("|    Result Recipe     |")
    print("------------------------\n")
    print("     %-64s %-15s %-20s %-5s" % ("Recipe Name", "Recipe ID", "Average Rating", "Description"))
    print("------------------------------------------------------------------------------------------"
          "----------------------------------------------------------"
          "----------------------------------------------------------------------------------------\n")
    if results is not None and len(results) > 0:
        num = 1

        for result in results:
            r = result[3].split("\n")

            count = 0
            for i in r:
                if count == 0:
                    print("%-4s %-65s %-20s %-14s %-5s" % (str(num) + ".", result[0], result[1], result[2], i))
                    count += 1
                else:
                    print("%-4s %-65s %-20s %-14s %-5s" % ("", "", "", "", i))
            num += 1

    else:
        print("No results found")


def print_ingredient_by_recipe(recipe_id):
    # Display the ingredient with name and quantity in a vertical manner
    cur.execute("select ingredient,ingredient_quantity from public.ingredient_to_recipe where recipe_id = %s",
                (recipe_id,))
    result = cur.fetchall()
    if result == None or len(result) == 0:
        print("Can not find ingredients for this recipe")
        return
    print("\n%-35s %-10s" % ("Ingredient Need", "Quantity"))
    print("---------------------------------------------")
    # ingredient_name_length = 15
    for row in result:
        in_id = row[0]
        quantity = row[1]
        cur.execute("select name from public.ingredients where id = %s", (in_id,))
        in_name = cur.fetchone()[0]
        print("%-37s %-16s" % (in_name, quantity))


def print_additional_info_recipe(recipe_id):
    # Get all the general information about the recipe
    cur.execute(
        "Select name, cook_time, difficulty, servings, steps, rating, description from public.recipe where recipe_id "
        "= %s",
        (recipe_id,))
    recipe_info = cur.fetchone()
    if recipe_info == None or len(recipe_info) == 0:
        print("Can not display more information for this recipe")
        return

    # Get each piece of information
    s = ""
    steps = recipe_info[4].split("',")
    step_str = s.join(steps)
    step_str = step_str.split("'")

    count = 0
    print("\n-------------------------------------------------------------")
    print("      Addition Recipe Information-->  Recipe_id:", recipe_id, "     ")
    print("-------------------------------------------------------------\n")
    print("Recipe Name:\t\t\t", recipe_info[0], "\n")
    print("Cook Time (Minutes):\t", recipe_info[1], "\n")
    print("Difficulty:\t\t\t\t", recipe_info[2], "\n")
    print("Serving Size: \t\t\t", recipe_info[3], "\n")
    for i in step_str:
        if count == 0 or i == ']':
            count += 1
            pass
        elif count == 1:
            print("Steps:\t\t\t\t\t", i)
            count += 1

        else:
            print("      \t\t\t\t\t", i)
    print("\nRating:\t\t\t\t\t", recipe_info[5], "\n")
    print("Description:\t\t\t", recipe_info[6])

    print_ingredient_by_recipe(recipe_id)


# recipe_id = 26
# ingredients = [['Chicken Breast', 10]]
def recipe_to_ingredient(recipe_id, ingredients):
    for i in ingredients:
        cur.execute("SELECT id FROM public.ingredients WHERE name = %s ", (i[0],))
        result = cur.fetchone()
        if result == None or len(result) == 0:
            cur.execute("INSERT INTO public.ingredients(name) VALUES (%s)", (i[0],))
            conn.commit()

        cur.execute("SELECT id FROM public.ingredients WHERE name = %s ", (i[0],))
        ingredient_id = int(cur.fetchone()[0])
        cur.execute("INSERT INTO public.ingredient_to_recipe(recipe_id,ingredient, ingredient_quantity) VALUES"
                    "(%s,%s,%s)", (recipe_id, ingredient_id, i[1]))
        conn.commit()


def show_past_made_recipe(user_id):
    cur.execute("SELECT recipe_id, rating, rating_date, review_text from public.rating WHERE user_id = %s"
                "ORDER BY rating_date DESC", (user_id,))
    results = cur.fetchall()

    print("--------------------------------")
    print("|     Recipes Made by You     |")
    print("---------------------------------\n")
    print("     %-58s %-20s %-18s %-28s %-5s" % (
        "Recipe Name", "Recipe ID", " Rating", "Rating Date", "Review Text"))
    print("------------------------------------------------------------------------------------------"
          "----------------------------------------------------------"
          "----------------------------------------------------------------------------------------\n")
    num = 1
    for r in results:
        cur.execute("SELECT name from public.recipe WHERE recipe_id = %s", (r[0],))
        name = cur.fetchall()
        if name is not None and len(name) != 0:
            name = name[0][0]
            print("%-2s %-62s %-20s %-14s %-30s %-5s" % (str(num) + ".", name, r[0], r[1], r[2], r[3]))
            num += 1


# create_recipe(name, cook_time, description, "Hard", 5, 7706, creation_date, steps)
# result = find_my_recipes(7706)
# print(result)
# print_my_recipe(result)
# print_my_recipe(1)
# CATEGORY TEST SET UP
# User1 have category = Chinese User_id = 0 category_id for chinese = 56
# User2 have category = Chinese User_id = 1 category_id for chinese = 57
# Recipe_id = 5289, created by user1
# Recipe_id = 8559, created by user2

# print(search_recipe_by_category("Chinese", "recent"))

# def search_recipe_by_category(name, sort_mode):
# if (search_mode == "recent")

# result = search_recipe_by_name("banana", "a")
# print(result)

# Testing change name
# edit_recipe("New name for test", None, None, None, None, None, 1)
# Testing changing cook_time
# edit_recipe(None, "10000", None, None, None, None, 1)
# Testing changing description
# edit_recipe(None, None, "Description V2", None, None, None, 1)
# Testing changing difficulty
# edit_recipe(None, None, None, "Very Hard", None, None,1)
# Testing servings
# edit_recipe(None, None, None, None, "10", None, 1)
# Testing steps
# edit_recipe(None, None, None, None, None, "These steps are arbitrary", 1)
# Testing delete_recipe
# delete_recipe(1,1)

# print_my_recipe(search_recipe_by_category("dinner", "rating"))
