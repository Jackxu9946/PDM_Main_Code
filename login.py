import pandas as pd
import psycopg2
import csv
from datetime import datetime
from datetime import date
conn = psycopg2.connect(
    host="reddwarf.cs.rit.edu",
    database="p320_02a",
    user="p320_02a",
    password="mdzpxSyGJSvn",
)

cur = conn.cursor()

cur.execute("select * from recipe_manager.users")

#comment

# username: SPBSP
# password: Y52A9
def login(username, password):
    cur.execute("SELECT username FROM recipe_manager.users WHERE username = %s", (username,))
    check_name = cur.fetchone()

    if not check_name:
        print("Username does not exist")
        return False
    else:
        print("Username: ", check_name[0])
        cur.execute("SELECT password FROM recipe_manager.users WHERE username = %s", (username,))
        check_psw = cur.fetchone()

        if check_psw[0] != password:
            print("Password is wrong")
        else:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("UPDATE recipe_manager.users SET last_access_date = %s WHERE username = %s", (time, username))

            print("Successfully log in ", time)

            return True


def main():

    username = input("Enter username: ")
    password = input("Psw: ")

    log = login(username, password)

    while not log:
        username = input("Enter username: ")
        password = input("Psw: ")
        login(username, password)

    cur.execute("SELECT last_access_date FROM recipe_manager.users WHERE username = %s", (username,))

    check_time = cur.fetchone()
    print(check_time)

    cur.execute("SELECT last_access_date FROM recipe_manager.users")
    x = cur.fetchall()

    for row in x:
        print(row[0])

main()
