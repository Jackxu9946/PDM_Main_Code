import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host = "reddwarf.cs.rit.edu",
    database = "p320_02a",
    user = "p320_02a",
    password = "mdzpxSyGJSvn",
)
cur = conn.cursor()

name = "Test"
cook_time = "50"
description = "This is a test"
user_id = 1
steps = "123123131"
creation_date = datetime.today().strftime('%Y-%m-%d')

def create_recipe(name, cook_time, description, difficulty, servings, created_by,creation_date, steps):
    try:
        cur.execute("INSERT INTO recipe_manager.recipe(name, cook_time, description, created_by, creation_date,steps, difficulty, servings) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, cook_time, description, created_by,creation_date, steps, difficulty, servings))
        conn.commit()
    except:
        print("Can not create new recipe")


def edit_recipe(name, cook_time, description, difficulty, servings, steps, recipe_id):
    try:
        if (name != None):
            cur.execute("UPDATE recipe_manager.recipe SET name = %s WHERE recipe_id = %s", (name, recipe_id))

        if (cook_time != None):
            cur.execute("UPDATE recipe_manager.recipe SET cook_time = %s WHERE recipe_id = %s", (cook_time, recipe_id))

        if (description != None):
            cur.execute("UPDATE recipe_manager.recipe SET description = %s WHERE recipe_id = %s", (description, recipe_id))

        if (difficulty != None):
            cur.execute("UPDATE recipe_manager.recipe SET difficulty = %s WHERE recipe_id = %s", (difficulty, recipe_id))

        if (servings != None):
            cur.execute("UPDATE recipe_manager.recipe SET servings = %s WHERE recipe_id = %s", (servings, recipe_id))

        if (steps != None):
            cur.execute("UPDATE recipe_manager.recipe SET steps = %s WHERE recipe_id = %s", (steps, recipe_id))

        conn.commit()
    except:
        print("Unable to save recipe")

def delete_recipe_with_error_checking(user_id, recipe_id):
    #Check if the recipe has been made
    cur.execute("SELECT * from recipe_manager.rating where recipe_id = %s LIMIT 1", (recipe_id))
    if (cur.fetchall() != None):
        delete_recipe(user_id, recipe_id)
    else:
        print("Can not delete receipe because another user has already made it")
def delete_recipe(user_id, recipe_id):
    #No error checking happening here
    try:
        cur.execute("DELETE FROM recipe_manager.recipe WHERE recipe_id= %s and created_by = %s", (recipe_id, user_id))
        conn.commit()
    except:
        print("Can not delete entry in database")


#Return a list of recipe_name along with their ID
#Empty list = no recipe
def search_recipe_by_name(name, search_mode):
    #search_mode = rating
    #most_recent = when it was made
    if (search_mode == "recent"):
        try:
            cur.execute("SELECT (name, recipe_id, rating, description) from recipe_manager.recipe where name like '%%{name}%%' ORDER BY creation_date ".format(name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")
    elif (search_mode == "rating"):
        try:
            cur.execute(
                "SELECT (name, recipe_id, rating, description) from recipe_manager.recipe where name like '%%{name}%%' ORDER BY rating ".format(
                    name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")
    else:
        try:
            cur.execute(
                "SELECT (name, recipe_id, rating, description) from recipe_manager.recipe where name like '%%{name}%%' ORDER BY name ".format(
                    name=name))
            results = cur.fetchall()
            return results
        except:
            print("Can not execute the recipe query")


def search_recipe_by_ingredient(ingredient, search_mode):
    #Get the ingredient ID
    #Assuming there is only one ingredient ID per name
    cur.execute("SELECT (id) from recipe_manager.ingredients where name = %s", (ingredient,))
    ingredient_result = cur.fetchone()
    if (ingredient_result == None):
        print("This ingredient does not exist in the database. Please check the name and try again")
    ingredient_id = ingredient_result[0]
    #Find all the recipe_id that contains this ingredient ID
    cur.execute("SELECT (recipe_id) from recipe_manager.ingredient_to_recipe where ingredient = %s", (ingredient_id))
    #CHECK THIS VALUE MAKE SURE IT IS A TUPLE BEFORE DOING ANYTHING ELSE
    recipe_id_list = cur.fetchall()
    #Now we have all the recipe_id we just need to choose the right value from the database
    result = None
    if (search_mode == "recent"):
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from recipe_manager.recipe where recipe_id in %s order by creation_date", (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    elif (search_mode == "rating"):
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from recipe_manager.recipe where recipe_id in %s order by rating", (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    else:
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from recipe_manager.recipe where recipe_id in %s order by name", (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    if (result != None):
        return result
    else:
        Print("Can not retrieve recipe")


def search_recipe_by_category(category, search_mode):
    #Get all the category id with category name = category
    cur.execute(
        "SELECT (id) from recipe_manager.category where name = %s", (category,)
    )
    temp = tuple(cur.fetchall())
    tuple_category_id = []
    for n in temp:
        tuple_category_id.append(n[0])
    tuple_category_id = tuple(tuple_category_id)
    #Now we have a tuple of category id
    #Use it to find recipe_id

    cur.execute(
        "SELECT (recipe_id) from recipe_manager.recipe_to_category where category_id in %s", (tuple_category_id,)
    )

    recipe_id_list = tuple(cur.fetchall())

    result = None
    if (search_mode == "recent"):
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from recipe_manager.recipe where recipe_id in %s order by creation_date", (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    elif (search_mode == "rating"):
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from recipe_manager.recipe where recipe_id in %s order by rating", (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    else:
        try:
            cur.execute(
                "SELECT (name,recipe_id, rating, description) from recipe_manager.recipe where recipe_id in %s order by name", (recipe_id_list)
            )
            result = cur.fetchall()
        except:
            print("Can not retrieve recipe")
    if (result != None):
        return result
    else:
        print("Can not retrieve recipe")


#CATEGORY TEST SET UP
#User1 have category = Chinese User_id = 0 cateogory_id for chinese = 0
#User2 have category = Chinese User_id = 1 category_id for chinese = 1
#Recipe_id = 5289, created by user1
#Recipe_id = 8559, created by user2

print(search_recipe_by_category("Chinese", "recent"))










# def search_recipe_by_category(name, sort_mode):
    # if (search_mdoe == "recent")

# result = search_recipe_by_name("banana", "a")
# print(result)

#Testing change name
# edit_recipe("New name for test", None, None, None, None, None, 1)
#Testing changing cooktime
# edit_recipe(None, "10000", None, None, None, None, 1)
#Testing chnging description
# edit_recipe(None, None, "Description V2", None, None, None, 1)
#Testing changing difficulty
# edit_recipe(None, None, None, "Very Hard", None, None,1)
#Testing servings
# edit_recipe(None, None, None, None, "10", None, 1)
#Testing steps
# edit_recipe(None, None, None, None, None, "These steps are arbitrary", 1)
#Testing delete_recipe
# delete_recipe(1,1)