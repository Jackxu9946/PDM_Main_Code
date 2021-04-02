import psycopg2
import ast

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from public.users")


def create_categories(name, username):
    """ @name category name from user input
        @username username entered by user

        return a list storing both user_id and new category_id.
    """
    cur.execute("SELECT user_id FROM public.users WHERE username = %s", (username,))
    user_id = cur.fetchone()
    # print(user_id[0]) to check user_id

    cur.execute("select * from public.category")
    cur.execute("INSERT INTO public.category(user_id,name) VALUES(%s, %s)", (user_id[0], name))
    conn.commit()

    cur.execute("SELECT id FROM public.category WHERE user_id= %s", user_id)
    category_id = cur.fetchall()
    # print(category_id[-1]) to check new category_id

    cur.execute("SELECT * FROM public.category WHERE user_id= %s", user_id)
    # print(cur.fetchall())
    return user_id, category_id[-1]


# create_categories("Chinese", "SPBSP")
# create_categories("Chinese", "SA4HY")


def list_of_recipes(user_id):
    """Return a list of recipes (name and id) owned by the user_id for user to view and insert into a category."""

    cur.execute("SELECT name, recipe_id FROM public.recipe WHERE created_by = %s", user_id)
    recipe_list = cur.fetchall()
    print("Your recipes:")
    for val in recipe_list:
        print("Recipe name:", val[0], "(recipe id: ", val[1], ")")


def add_recipes(category_id, input_recipes):
    """Return False when the recipe_id entered by user does not exist or already exist in the category.
       Otherwise insert the recipe_id and category_id into the recipe_to_category.
    """

    # input_recipes = input("\nEnter a recipe id to add recipe into category named" + name + ": ")

    cur.execute("SELECT recipe_id FROM public.recipe WHERE recipe_id = %s", (input_recipes,))

    exist = cur.fetchone()

    cur.execute("SELECT recipe_id, category_id FROM public.recipe_to_category WHERE recipe_id = %s and "
                "category_id = %s", (input_recipes, category_id))
    already_exist = cur.fetchone()
    # print(already_exist) to check the existing recipe_id

    if not exist:
        print("\nFail to add recipe to category. Recipe id does not exist.")
        return False
    elif already_exist:
        print("\nFail to add recipe to category. Recipe id already exist.")
        return False
    else:
        cur.execute("select * from public.recipe_to_category")
        cur.execute("INSERT INTO public.recipe_to_category(recipe_id, category_id) VALUES(%s, %s)",
                    (input_recipes, category_id))
        print("Successfully added!")

        conn.commit()


def open_category(category_id, name):
    """Print a list of recipes in the category"""

    cur.execute("SELECT recipe_id FROM public.recipe_to_category WHERE category_id = %s", (category_id,))
    lists = cur.fetchall()

    print("Category-->", name, ":")
    for val in lists:
        cur.execute("SELECT name FROM public.recipe WHERE recipe_id = %s", val)
        recipe_name = cur.fetchall()
        for names in recipe_name:
            print("     Recipe name:", names[0], "(recipe id:", val[0], ")")


def display_category(user_id):
    cur.execute("SELECT * FROM public.category where user_id = %s", (user_id,))
    results = cur.fetchall()
    if results is not None and len(results) > 0:
        for result in results:
            result_string = str(result[0]) + "     " + result[2]
            print(result_string)
    else:
        print("No personal categories yet")
# display_category(7706)

# username: V79QX
# def main():
# user = "V79QX"
# name = input("Name your new category: ")
#
# ids = create_categories(name, user)  # ids store both user_id and category_id
# user_id = ids[0]
# category_id = ids[1]
# print("check category", category_id)
#
# list_of_recipes(user_id)  # show a list of recipes owned by the user_id
#
# check = add_recipes(name, category_id)
#
# while not check:
#     cmd1 = input("\nDo you want to enter another recipe id (N or Y): ")
#     if cmd1 == "N":
#         break
#     elif cmd1 == "Y":
#         check = add_recipes(name, category_id)
#     else:
#         print("Cannot recognize your input.")

#     category_id = "55"
#     name = "chicken"
#     open_category(category_id, name)
#
#
# main()
