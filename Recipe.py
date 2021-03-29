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