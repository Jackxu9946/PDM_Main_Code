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


# create_recipe(name,cook_time,description, "Hard", 5, 7706, creation_date,steps, None)


# create_recipe(name, cook_time, description, "Hard", 5, user_id, creation_date, steps)


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
                        "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC".format(name=name))

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

    # Find all the recipe_id that contains this ingredient ID
    # cur.execute("SELECT recipe_id from public.ingredient_to_recipe where ingredient = %s", (ingredient_id,))
    # # CHECK THIS VALUE MAKE SURE IT IS A TUPLE BEFORE DOING ANYTHING ELSE
    # recipe_id_list = cur.fetchall()
    # num1=0
    # for i in recipe_id_list:
    #     num1+=1;
    # print(num1)
    # print(recipe_id_list)
    # if (len(recipe_id_list) == 0):
    #     # print("No recipe found with this ingredient")
    #     return
    # # Now we have all the recipe_id we just need to choose the right value from the database
    # result = None
    # print(recipe_id_list)
    # id_list = []
    # for recipe in recipe_id_list:
    #     id_list.append(int(recipe[0]))
    #     # print(id_list)
    # recipe_id_list = tuple(id_list)

    if search_mode == "recent":
        try:
            cur.execute("SELECT name, recipe_id, rating, creation_date, description from public.recipe where recipe_id IN "
                        "(SELECT recipe_id from public.ingredient_to_recipe where ingredient = %s) "
                        "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC", (ingredient_id,))

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
                "(SELECT recipe_id from public.ingredient_to_recipe where ingredient = %s) order by name", (ingredient_id,))
            result = cur.fetchall()
            return result
        except:
            print("Can not retrieve recipe")
    # if result is not None:
    #     return result
    # else:
    #     print("Can not retrieve recipe")


# print(search_recipe_by_ingredient("Chicken Breast", "Rating"))

def search_recipe_by_category(category, search_mode):
    # Get all the category id with category name = category
    # cur.execute(
    #     "SELECT (id) from public.category where name = %s", (category,)
    # )
    # conn.commit()
    # temp = tuple(cur.fetchall())
    # if (len(temp) == 0):
    #     print("No category with this name")
    #     return
    # tuple_category_id = []
    # for n in temp:
    #     tuple_category_id.append(n[0])
    # tuple_category_id = tuple(tuple_category_id)
    # # Now we have a tuple of category id
    # # Use it to find recipe_id
    # cur.execute(
    #     "SELECT recipe_id from public.recipe_to_category where category_id in %s", (tuple_category_id,)
    # )
    #
    # recipe_id_list = tuple(cur.fetchall())
    # if (len(recipe_id_list) == 0):
    #     print("No recipe belongs to this category")
    #     return
    # recipe_tuple = []
    # for id in recipe_id_list:
    #     recipe_tuple.append(id[0])
    # recipe_id_list = tuple(recipe_tuple)
    # result = None
    # print(recipe_id_list)
    if search_mode == "recent":
        try:
            cur.execute(
                "SELECT name, recipe_id, rating, creation_date, description from public.recipe where recipe_id IN "
                "(SELECT recipe_id from public.recipe_to_category WHERE category_id IN "
                "(SELECT id from public.category WHERE name = %s)) "
                "GROUP BY name, recipe_id, rating, creation_date, description ORDER BY MAX(creation_date) DESC ", (category,))

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
    # if result is not None:
    #     return result
    # else:
    #     print("Can not retrieve recipe")


# CATEGORY TEST SET UP
# User1 have category = Chinese User_id = 0 cateogory_id for chinese = 56
# User2 have category = Chinese User_id = 1 category_id for chinese = 57
# Recipe_id = 5289, created by user1
# Recipe_id = 8559, created by user2

# print(search_recipe_by_category("Chinese", ""))

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
        # print("???")
        # recipe_name_header = "Name                               |"
        # recipe_ID_header = "ID      |"
        # recipe_rating_header = "Rating     |"
        # recipe_description = "Description"
        # recipe_header = recipe_name_header + recipe_ID_header + recipe_rating_header + recipe_description
        # print(recipe_header)
        # print("\n")
        # print(results)
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

        # cur_recipe = result[0].split(",")
        # print(cur_recipe)
        # print("\t\t\t", cur_recipe[3])
    #         result_string = ""
    #         cur_recipe = result[0].split(",")
    #         cur_recipe_name = cur_recipe[0]
    #         cur_recipe_name = cur_recipe_name[1:]
    #         cur_recipe_name = cur_recipe_name.replace('"', '')
    #         cur_recipe_ID = str(cur_recipe[1])
    #         cur_recipe_rating = cur_recipe[2]
    #         cur_recipe_description = cur_recipe[3]
    #         cur_recipe_description = cur_recipe_description[:-1]
    #         # Format the result string
    #         if len(cur_recipe_name) < len(recipe_name_header):
    #             cur_recipe_name += (" " * (len(recipe_name_header) - len(cur_recipe_name)))
    #             result_string += cur_recipe_name
    #         if len(cur_recipe_ID) < len(recipe_ID_header):
    #             cur_recipe_ID += (" " * (len(recipe_ID_header) - len(cur_recipe_ID)))
    #             result_string += cur_recipe_ID
    #         if (len(cur_recipe_rating) < len(recipe_rating_header)):
    #             cur_recipe_rating += (" " * (len(recipe_rating_header) - len(cur_recipe_rating)))
    #             result_string += cur_recipe_rating
    #         result_string += cur_recipe_description
    #         print(result_string)
    #


# search_recipe_by_name("apple", "recent")
# search_recipe_by_ingredient("vanilla", "recent")
# print_my_recipe(search_recipe_by_ingredient("vanilla", "rating"))
# print_my_recipe(search_recipe_by_ingredient("vanilla", "default"))
# print_my_recipe(search_recipe_by_category("dinner", "rating"))
# print_my_recipe(search_recipe_by_category("dinner", "default"))
# search_recipe_by_category("dinner", "recent")


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
    #     row = row[0]
    #     row = row[1:-1]
    #     row = row.split(",")
    #     ingredient_id = int(row[0])
    #     ingredient_quantity = str(row[1])
    #     # Get the ingredient name
    #     cur.execute("select name from public.ingredients where id = %s", (ingredient_id,))
    #     ingredient_name = cur.fetchone()
    #     if ingredient_name != None and len(ingredient_name) > 0:
    #         # Print the name and
    #         ingredient_name = ingredient_name[0]
    #         # Format the string and print it
    #         if len(ingredient_name) < ingredient_name_length:
    #             ingredient_name += (" " * (ingredient_name_length - len(ingredient_name)))
    #         ingredient_name += " |"
    #         ingredient_name += ingredient_quantity
    #         print(ingredient_name)


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
    # recipe_info = recipe_info[0]
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

    # header_list = ["Name:", "Cook Time:", "Difficulty:", "Serving Size:", "Steps:", "Rating:", "Description:"]
    # recipe_info = recipe_info[1:-1]
    # recipe_info = recipe_info.split(",")
    # for i in range(len(header_list)):
    #     current_header = header_list[i]
    #     current_value = recipe_info[i]
    #     if current_value == None or len(current_value) == 0:
    #         continue
    #     print(current_header)
    #     print(current_value)
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
