import psycopg2
from datetime import datetime
from datetime import timedelta
import ast

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()


# Tested as follows:
# Enter a review for this recipe: This is testing
# Enter a rating for this recipe: 3
# Output: [(123, 345, Decimal('3'), datetime.datetime(2021, 3, 28, 0, 26, 2), 'This is testing')]
def rate_recipe(user_id, recipe_id):
    review_text = input("Enter a review for this recipe: ")
    rating = int(input("Enter a rating for this recipe: "))
    creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO public.rating(user_id, recipe_id, rating, rating_date, review_text ) "
                "VALUES(%s, %s, %s, %s, %s)", (user_id, recipe_id, rating, creation_datetime, review_text))
    # Update the current rating average after inserting new rating for recipe
    # Get the current average rating
    cur.execute("select (rating) from public.recipe where recipe_id = %s", (recipe_id,))
    current_average_rating = cur.fetchone()[0]
    if (current_average_rating == None):
        current_average_rating = 0
    # print(current_average_rating)
    # Get the current rating count
    cur.execute("select count(*) from public.rating where recipe_id = %s", (recipe_id,))
    current_rating_count = cur.fetchone()[0]
    # print(current_rating_count)
    # New average rating
    new_average_rating = ((current_average_rating * current_rating_count) + rating) / (current_average_rating + 1)

    # Update the recipe table
    cur.execute("UPDATE public.recipe SET rating = %s where recipe_id = %s", (new_average_rating, recipe_id,))

    print("Rated and made recipe successfully")
    conn.commit()


def mark_recipe(user_id, recipe_id, scale):
    cur.execute("SELECT * FROM public.recipe WHERE recipe_id = %s", (recipe_id,))
    exist = cur.fetchone()
    if exist is None or len(exist) == 0:
        # recipe_id does not correspond to any recipe
        print("Recipe does not exist")
        return
    else:
        cur.execute("SELECT ingredient FROM public.ingredient_to_recipe WHERE recipe_id = %s", (recipe_id,))
        # get the results of the recipe (probably)
        ingredients = cur.fetchall()

        for i in ingredients:
            # each i is the id of individual ingredient in the ingredient list
            # get the quantity of this ingredient needed in recipe
            cur.execute("SELECT ingredient_quantity FROM public.ingredient_to_recipe WHERE recipe_id = %s"
                        "AND ingredient = %s ", (recipe_id, i[0]))
            quantity_need = cur.fetchone()[0]
            # print("quantity_need: ", quantity_need)
            scaled_quantity = quantity_need * scale
            # get the quantity of the needed ingredient in the pantry
            cur.execute("SELECT current_quantity FROM public.pantry WHERE user_id = %s "
                        "AND ingredient_id = %s ", (user_id, i[0]))
            quantity_have = cur.fetchone()
            if quantity_have is None or len(quantity_have) == 0:
                # print("Not enough ingredients to make this recipe")
                print("Not enough quantity to make recipe.")
                return False
            quantity_have = int(quantity_have[0])
            quantity_remained = quantity_have - scaled_quantity
            # have enough quantity for this ingredient.
            if quantity_remained >= 0:
                # update the current quantity of this ingredient after some quantity is used to make the recipe
                cur.execute("UPDATE public.pantry SET current_quantity = %s "
                            "WHERE user_id = %s AND ingredient_id = %s", (quantity_remained, user_id, i))
            # not enough quantity for this ingredient
            else:
                print("Not enough quantity to make recipe.")
                return False
    conn.commit()

    # Rate recipe after successfully making it
    rate_recipe(user_id, recipe_id)
    return True


# Tested
def update_item(user_id, ingredient_id, quantity_updated):
    cur.execute("UPDATE public.pantry SET current_quantity = %s "
                "WHERE user_id = %s AND ingredient_id = %s", (quantity_updated, user_id, ingredient_id))
    conn.commit()


def add_ingredient_to_pantry(user_id, ingredient_name, quantity):
    # Check if ingredient is in our database
    # Asssume ingredient_name is already in lower case
    cur.execute("SELECT COUNT(*) from public.ingredients where name = %s", (ingredient_name,))
    result = int(cur.fetchone()[0])
    if result == 0:
        cur.execute("INSERT INTO public.ingredients(name) VALUES (%s)", (ingredient_name,))
        conn.commit()
    # Get the ingredient id
    cur.execute("Select (id) from public.ingredients where name = %s", (ingredient_name,))
    ingredient_id = int(cur.fetchone()[0])

    # Use the ingredient_id to insert into pantry_bought table
    bought_date = datetime.today().strftime('%Y-%m-%d')
    expiration_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')


    cur.execute(
        "INSERT into public.pantry_bought(user_id,quantity_bought,purchase_date,expiration_date,ingredient_id) VALUES (%s, %s, %s, %s, %s)",
        (user_id, quantity, bought_date, expiration_date, ingredient_id)
    )

    # Update the current quantity in pantry
    cur.execute(
        "Select current_quantity from public.pantry where user_id = %s and ingredient_id = %s",
        (user_id, ingredient_id)
    )

    current_quantity = cur.fetchone()
    if current_quantity is None or len(current_quantity) == 0:
        # Doesnt exist yet
        cur.execute("INSERT INTO public.pantry (user_id, ingredient_id, current_quantity) VALUES (%s, %s, %s)",
                    (user_id, ingredient_id, quantity))
    else:
        current_quantity = int(current_quantity[0])
        # Update the current quantity of the ingredient
        cur.execute("UPDATE public.pantry SET current_quantity = %s where user_id = %s and ingredient_id = %s",
                    (current_quantity + quantity, user_id, ingredient_id))
    print("\nAdded to pantry successfully.")
    conn.commit()


def update_pantry(user_id, ingredient_name, quantity):
    # Get the ingredient_id given ingredient_name
    cur.execute("select (id) from public.ingredients where name = %s", (ingredient_name,))

    result = cur.fetchone()
    if (result == None):
        print("This ingredient does not exist")
        return

    ingredient_id = int(result[0])

    # Check if the user has this item in their pantry
    cur.execute("select count(*) from public.pantry where ingredient_id = %s and user_id = %s",
                (ingredient_id, user_id))

    has_item = cur.fetchone()

    if (has_item == None):
        print("This item does not exist in your pantry yet. Please purchase first")
        return

    cur.execute("UPDATE public.pantry SET current_quantity = %s where ingredient_id = %s and user_id = %s",
                (quantity, ingredient_id, user_id))
    print("Pantry updated successfully")
    conn.commit()


def show_pantry(user_id):
    cur.execute("select (ingredient_id, current_quantity) from public.pantry where user_id = %s AND current_quantity "
                "> 0 ORDER BY current_quantity ASC"
                , (user_id,))
    results = cur.fetchall()

    if (results == None or len(results) == 0):
        print("No item currently in pantry")
        return

    print_pantry(results)




def print_pantry(list_of_pantry_items):
    print("--------------------------------")
    print("|           My Pantry          |")
    print("--------------------------------\n")
    print("  %-40s   %-20s"%("Ingredient Name", "Quantity"))
    print("--------------------------------------------------------")
    num = 1
    for result in list_of_pantry_items:
        result = ast.literal_eval(result[0])
        ingredient_id = int(result[0])
        # Get the ingredient name
        cur.execute("select (name) from public.ingredients where id = %s", (ingredient_id,))
        ingredient_name = str(cur.fetchone()[0])

        print("%-4s %-40s %-20s" % (str(num) + ".",ingredient_name,str(result[1])))
        num += 1


# Only for testing
def add_item(user_id, ingredient_id):
    current_quantity = 1
    cur.execute("INSERT INTO public.pantry(user_id, ingredient_id, current_quantity)"
                "VALUES(%s, %s, %s)", (user_id, ingredient_id, current_quantity))
    conn.commit()

