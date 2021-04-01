import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from public.users")


# select *from DemoTable807 where ClientCountryName='US'


def register(username, password):
    creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("SELECT username FROM public.users WHERE username = %s", (username,))
    row = cur.fetchone()
    if not row:
        # print("Not exist in table")
        cur.execute("select * from public.users")
        cur.execute("INSERT INTO public.users(username, password,creation_date, last_access_date) "
                    "VALUES(%s, %s, %s, %s)", (username, password, creation_datetime, creation_datetime))
        # print("Inserted")
    else:
        print("already exist")

    cur.execute("SELECT username FROM public.users WHERE username = %s", (username,))

    conn.commit()


def main():
    username = "SPBSP"
    register(username, "1111")


main()
