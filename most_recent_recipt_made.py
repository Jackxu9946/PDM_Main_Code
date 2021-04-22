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

        
def update_rating():
    """
    Update the average rating in the recipe table for the newly populated data into the rating table
    :return:
    """
    cur.execute("SELECT DISTINCT recipe_id FROM public.rating")
    result = cur.fetchall()

    for i in result:
        i = str(i)
        i = i[1:-2]
        cur.execute("SELECT rating from public.rating WHERE recipe_id = %s", (i,))
        r = cur.fetchall()
        sum1 = 0
        count = 0
        for a in r:
            a = str(a)
            a = a[10:11]
            a = int(a)
            sum1 += a
            count += 1
        rating = int(round(sum1 / count, 0))
        cur.execute("UPDATE public.recipe SET rating = %s WHERE recipe_id = %s", (rating, i))
        conn.commit()
