import psycopg2

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from public.users")


def recommending_recipes(user_id):
    """Recommended to you: Recipes made by other users who make the same recipes.
       The recipes will be sorted by rating (from high to low)"""

    # nested query used to find recipes made by other users who make the same recipe in rating table and sort the
    # recipes by average rating in a descending order (from highest to lowest)
    # 1. find users who make the same recipe in rating table
    # 2. find other distinct recipes made by these users in rating table using recipe_id NOT IN(...) AND user_id IN(...) statements
    # 3. sort these recipes by average rating in recipe table in a descending order
    cur.execute("SELECT name, recipe_id, rating, description FROM public.recipe WHERE recipe_id IN "
                "(SELECT DISTINCT recipe_id FROM public.rating WHERE recipe_id NOT IN "
                "(SELECT recipe_id FROM public.rating WHERE recipe_id IN "
                "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = %s)) AND user_id IN "
                "(SELECT user_id FROM public.rating WHERE recipe_id IN "
                "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = %s))) "
                "GROUP BY name, recipe_id, rating, description ORDER BY MAX(rating) DESC", (user_id, user_id))

    recipe_info = cur.fetchall()

    print("\n--------------------------")
    print("|   Recommended to you   |")
    print("--------------------------\n")
    print("   %-64s %-15s %-20s %-5s" % ("Recipe Name", "Recipe ID", "Average Rating", "Description"))
    print("-----------------------------------------------------------------------------------------------"
          "------------------------------------------------------------------------------------------------"
          "------------------------------------------------------------------------------------------------")

    num = 1
    if recipe_info is not None and len(recipe_info) > 0:
        for info in recipe_info:
            print("%-1s %-65s %-20s %-14s %-5s" % (str(num) + ".", info[0], info[1], info[2], info[3]))
            num += 1
    else:
        print(" No recommended recipes yet!")


# def main():
#     # recipe_id = "21132"
#     # recommending_recipes(recipe_id)
#     cur.execute("SELECT user_id FROM public.rating")
#     print(cur.fetchall())
#     cur.execute("SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = 215898")
#     print("这个人全部的菜单：", cur.fetchall())
#
#     cur.execute("SELECT user_id, recipe_id FROM public.rating WHERE recipe_id IN "
#                 "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = 69066) ")
#     print("\nusers:", cur.fetchall())
#
#     cur.execute("SELECT DISTINCT recipe_id, user_id FROM public.rating WHERE user_id IN "
#                 "(SELECT user_id FROM public.rating WHERE recipe_id IN "
#                 "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = 69066)) ")
#     print("\nall recipe:", cur.fetchall())
#
#     user_id = "215898"
#     cur.execute("SELECT name, recipe_id, rating FROM public.recipe WHERE recipe_id IN "
#                 "(SELECT DISTINCT recipe_id FROM public.rating WHERE recipe_id NOT IN "
#                 "(SELECT recipe_id FROM public.rating WHERE recipe_id IN "
#                 "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = %s)) AND user_id IN "
#                 "(SELECT user_id FROM public.rating WHERE recipe_id IN "
#                 "(SELECT DISTINCT recipe_id FROM public.rating WHERE user_id = %s))) "
#                 "GROUP BY name, recipe_id, rating ORDER BY MAX(rating) DESC", (user_id, user_id))
#     print("\n过滤后：", cur.fetchall())
#
#     recommending_recipes(user_id)
#
#
# main()
