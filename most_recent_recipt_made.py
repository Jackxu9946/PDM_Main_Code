import psycopg2

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()


def most_recent_recipe():
    """
    Get the 50 most recent recipes made order by creation date.
    """

    cur.execute("SELECT  recipe_id FROM public.rating "
                "GROUP BY recipe_id ORDER BY MAX(rating_date) DESC LIMIT 50 ")
    result = cur.fetchall()
    list1 = []
    for i in result:
        i = str(i)
        i = str(i[1:-2])
        list1.append(i)

    num = 1
    print("--------------------------------")
    print("|     50 Most Recent Recipes     |")
    print("---------------------------------\n")
    print("  %-45s %-15s" % ("Recipe Name", "Recipe_id\n"))
    for i in list1:
        cur.execute("SELECT name FROM public.recipe WHERE recipe_id = %s", (i,))
        name = cur.fetchone()
        name = str(name)
        name = name[1:-2]
        print(" %-2s %-45s %-15s" % (str(num) + ".", name, i))
        num += 1


