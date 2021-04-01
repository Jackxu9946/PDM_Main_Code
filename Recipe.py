import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)
cur = conn.cursor()

name = "Test 3"
cook_time = "50"
description = "This is a test"
user_id = 1
steps = "123123131"
creation_date = datetime.today().strftime('%Y-%m-%d')


def create_recipe(name, cook_time, description, difficulty, servings, created_by, creation_date, steps):
    try:
        cur.execute(
            "INSERT INTO public.recipe(name, cook_time, description, created_by, creation_date,steps, difficulty, servings) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (name, cook_time, description, created_by, creation_date, steps, difficulty, servings,)
        )
        conn.commit()
        print("Recipe has been added successfully")
    except:
        print("Can not create new recipe")


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
    cur.execute("SELECT * from public.rating where recipe_id = %s LIMIT 1", (recipe_id))
    if cur.fetchall() is not None:
        delete_recipe(user_id, recipe_id)
    else:
        print("Can not delete recipe because another user has already made it")


def delete_recipe(user_id, recipe_id):
    # No error checking happening here
    try:
        cur.execute("DELETE FROM public.recipe WHERE recipe_id= %s and created_by = %s", (recipe_id, user_id))
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
            cur.execute(
                "SELECT (name, recipe_id, rating, description) from public.recipe where name like '%%{name}%%' ORDER BY creation_date ".format(
                    name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")
    elif search_mode == "rating":
        try:
            cur.execute(
                "SELECT (name, recipe_id, rating, description) from public.recipe where name like '%%{name}%%' ORDER BY rating ".format(
                    name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")
    else:
        try:
            cur.execute(
                "SELECT (name, recipe_id, rating, description) from public.recipe where name like '%%{name}%%' ORDER BY name ".format(
                    name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")


def search_recipe_by_ingredient(ingredient, search_mode):
    # Get the ingredient ID
    # Assuming there is only one ingredient ID per name
    cur.execute("SELECT (id) from public.ingredients where name = %s", (ingredient,))
    ingredient_result = cur.fetchone()
    if ingredient_result is None:
        print("This ingredient does not exist in the database. Please check the name and try again")
    ingredient_id = ingredient_result[0]
    # Find all the recipe_id that contains this ingredient ID
    cur.execute("SELECT (recipe_id) from public.ingredient_to_recipe where ingredient = %s", (ingredient_id))
    # CHECK THIS VALUE MAKE SURE IT IS A TUPLE BEFORE DOING ANYTHING ELSE
    recipe_id_list = cur.fetchall()
    # Now we have all the recipe_id we just need to choose the right value from the database
    result = None
    if search_mode == "recent":
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from public.recipe where recipe_id in %s order by creation_date",
                (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    elif search_mode == "rating":
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from public.recipe where recipe_id in %s order by rating",
                (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    else:
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from public.recipe where recipe_id in %s order by name",
                (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    if result is not None:
        return result
    else:
        print("Can not retrieve recipe")


def search_recipe_by_category(category, search_mode):
    # Get all the category id with category name = category
    cur.execute(
        "SELECT (id) from public.category where name = %s", (category,)
    )
    conn.commit()
    temp = tuple(cur.fetchall())
    tuple_category_id = []
    for n in temp:
        tuple_category_id.append(n[0])
    tuple_category_id = tuple(tuple_category_id)
    # Now we have a tuple of category id
    # Use it to find recipe_id
    cur.execute(
        "SELECT (recipe_id) from public.recipe_to_category where category_id in %s", (tuple_category_id,)
    )

    recipe_id_list = tuple(cur.fetchall())
    recipe_tuple = []
    for id in recipe_id_list:
        recipe_tuple.append(id[0])
    recipe_id_list = tuple(recipe_tuple)
    result = None
    print(recipe_id_list)
    if search_mode == "recent":
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from public.recipe where recipe_id in %s order by creation_date",
                (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    elif search_mode == "rating":
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from public.recipe where recipe_id in %s order by rating",
                (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    else:
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from public.recipe where recipe_id in %s order by name",
                (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    if result is not None:
        return result
    else:
        print("Can not retrieve recipe")


#CATEGORY TEST SET UP
#User1 have category = Chinese User_id = 0 cateogory_id for chinese = 56
#User2 have category = Chinese User_id = 1 category_id for chinese = 57
#Recipe_id = 5289, created by user1
#Recipe_id = 8559, created by user2

# print(search_recipe_by_category("Chinese", ""))

def find_my_recipes(user_id):
    try:
        cur.execute("SELECT (name, recipe_id, description) from public.recipe where created_by = %s", (user_id,))
        results = cur.fetchall()
        return results
    except:
        print("Can not retrieve recipe")

def print_my_recipe(results):
    # results = find_my_recipes(user_id)
    recipe_name_header = "Name                             |"
    recipe_ID_header = "ID        |"
    recipe_description = "Description"
    recipe_header = recipe_name_header + recipe_ID_header + recipe_description
    print(recipe_header)
    for result in results:
        result_string = ""
        cur_recipe = ast.literal_eval(result[0])
        cur_recipe_name = cur_recipe[0]
        cur_recipe_ID = str(cur_recipe[1])
        cur_recipe_description = cur_recipe[2]
        #Format the result string
        if (len(cur_recipe_name) < len(recipe_name_header)):
            cur_recipe_name += (" " * (len(recipe_name_header) - len(cur_recipe_name)))
            result_string += cur_recipe_name
        if (len(cur_recipe_ID) < len(recipe_ID_header)):
            cur_recipe_ID += (" " * (len(recipe_ID_header) - len(cur_recipe_ID)))
            result_string += cur_recipe_ID
        result_string += cur_recipe_description
        print(result_string)


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
