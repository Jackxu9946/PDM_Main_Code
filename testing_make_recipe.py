import psycopg2

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from public.users")


def test_make_recipe(recipe_id, user_id):
    cur.execute("SELECT ingredient, ingredient_quantity FROM public.ingredient_to_recipe WHERE recipe_id = %s",
                (recipe_id,))
    res1 = cur.fetchall()
    print(res1)

    for x in res1:
        cur.execute("SELECT name, id FROM public.ingredients WHERE id = %s", (x[0],))
        print(cur.fetchall())

        # cur.execute("SELECT user_id FROM public.users WHERE username = %s", (name,))
        # print(cur.fetchall())

    cur.execute("SELECT ingredient_id, current_quantity FROM pantry WHERE user_id = %s", (user_id,))
    print(cur.fetchall())


def check_pantry():
    cur.execute("SELECT ingredient_id FROM public.pantry WHERE user_id = 7715")
    print(cur.fetchall())

    cur.execute("SELECT ingredient_id, current_quantity FROM public.pantry WHERE user_id = 7715")
    print(cur.fetchall())

    # cur.execute("SELECT t1.recipe_id FROM public.pantry AS t1, public.pantry AS t2 WHERE t2.current_quantity IN "
    #             "(SELECT t2.current_quantity FROM public.pantry AS t2 WHERE t1.ingredient IN "
    #             "(SELECT t1.ingredient FROM public.ingredient_to_recipe AS t1 INNER JOIN public.pantry AS t2 ON t1.ingredient = t2.ingredient_id AND t2.user_id = 7715))"
    #             "AND t2.current_quantity >= t1.ingredient_quantity")

    cur.execute("SELECT DISTINCT t1.ingredient, t1.ingredient_quantity, t2.current_quantity "
                "FROM public.ingredient_to_recipe AS t1 INNER JOIN public.pantry AS t2 ON t1.ingredient = t2.ingredient_id "
                "AND t2.user_id = 7715 WHERE t2.current_quantity >= t1.ingredient_quantity")
    print(cur.fetchall())

    cur.execute("SELECT ingredient_id, current_quantity FROM public.pantry WHERE user_id = 7715 AND ingredient_id = 6027")
    print(cur.fetchall())

    cur.execute("SELECT ingredient, ingredient_quantity FROM public.ingredient_to_recipe WHERE ingredient = 6027")
    print(cur.fetchall())
    # cur.execute("SELECT t1.recipe_id FROM public.ingredient_to_recipe AS t1 INNER JOIN public.pantry AS t2 ON t1.ingredient = t2.ingredient_id AND t2.user_id = 7715 WHERE t2.current_quantity >= t1.ingredient_quantity")
    #
    # print(cur.fetchall())


# def main():
#     recipe_id = "21132"
#     user_id = "7715"
#
#     test_make_recipe(recipe_id, user_id)
#
#     check_pantry()
#
#     # cur.execute("SELECT name FROM public.ingredients WHERE id IN (SELECT ingredient_id FROM public.pantry)")
#     # cur.execute("UPDATE public.pantry SET name IN "
#     #             "(SELECT name FROM public.ingredients WHERE id IN "
#     #             "(SELECT ingredient_id FROM public.pantry)) WHERE ingredient_id IN (SELECT id FROM public.ingredients) ")
#     #
#
#     # cur.execute("SELECT ingredient_id FROM public.pantry")
#     # res = cur.fetchall()
#     #
#     # for x in res:
#     #     cur.execute("SELECT name FROM public.ingredients WHERE id = %s", (x[0],))
#     #     name = cur.fetchone()
#     #
#     #     cur.execute("UPDATE public.pantry SET name = %s where ingredient_id = %s", (name, x[0]))
#     #
#     # cur.execute("SELECT ingredient_id, name FROM public.pantry")
#     # print(cur.fetchall())
#     #
#     #
#     # conn.commit()
#
# main()
