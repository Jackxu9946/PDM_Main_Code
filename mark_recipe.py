import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()


def mark_recipe(user_id, recipe_id, scale):
    cur.execute("SELECT * FROM public.recipes WHERE recipe_id = %d")
    exist = cur.fetchone()
    if not exist:
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
                        "AND ingredient_id = %s ", (recipe_id, i))
            quantity_need = cur.fetchone()
            scaled_quantity = quantity_need * scale
            # get the quantity of the needed ingredient in the pantry
            cur.execute("SELECT current_quantity FROM public.pantry WHERE user_id = %s "
                        "AND ingredient_id = %s ", (recipe_id, i))
            quantity_have = cur.fetchone()

            quantity_remained = scaled_quantity - quantity_have
            # have enough quantity for this ingredient.
            if quantity_remained >= 0:
                # update the current quantity of this ingredient after some quantity is used to make the recipe
                cur.execute("UPDATE public.pantry SET current_quantity = %d "
                            "WHERE user_id = %d AND ingredient_id = %d", (quantity_remained, user_id, i))
            # not enough quantity for this ingredient
            else:
                print("Not enough quantity to make recipe.")
                return False


    # Rate recipe after successfully making it
    rate_recipe(user_id, recipe_id)

    #conn.commit()
    return True


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
    #Update the current rating average after inserting new rating for recipe
    #Get the current average rating
    cur.execute("select (rating) from public.recipe where recipe_id = %s", (recipe_id,))
    current_average_rating = cur.fetchone()[0]
    if (current_average_rating == None):
        current_average_rating = 0
    # print(current_average_rating)
    #Get the current rating count
    cur.execute("select count(*) from public.rating where recipe_id = %s", (recipe_id,))
    current_rating_count = cur.fetchone()[0]
    # print(current_rating_count)
    #New average rating
    new_average_rating = ((current_average_rating * current_rating_count ) + rating) / (current_average_rating + 1)

    #Update the recipe table
    cur.execute("UPDATE public.recipe SET rating = %s where recipe_id = %s", (new_average_rating, recipe_id,))
    conn.commit()

# Tested
def update_item(user_id, ingredient_id, quantity_updated):
    cur.execute("UPDATE public.pantry SET current_quantity = %s "
                "WHERE user_id = %s AND ingredient_id = %s", (quantity_updated, user_id, ingredient_id))
    conn.commit()

# def add_ingredient_to_pantry(ingredient_name, quantity):
    #Check if ingredient is in our database


# Only for testing
def add_item(user_id, ingredient_id):
    current_quantity = 1
    cur.execute("INSERT INTO public.pantry(user_id, ingredient_id, current_quantity)"
                "VALUES(%s, %s, %s)", (user_id, ingredient_id, current_quantity))
    conn.commit()


def main():
    print(2, )


main()
