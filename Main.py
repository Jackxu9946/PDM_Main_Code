import login
import register
import Recipe
from datetime import datetime

global_username = ""
user_id = ""


def main():
    signed_in = 0
    i = 0
    while i != 4:
        print("\nSign up or sign in if you already have an account.\n"
              "Please select ONLY the number to start an action!\n"
              "1. Sign up\n"
              "2. Sign in\n"
              "3. Move to the next section\n")

        reg_switcher = {
            1: main_register,
            2: main_login,
            3: 3
        }

        action_value = input(": ")

        if int(action_value) == 3 & signed_in == 1:
            break

        elif int(action_value) == 3:
            print("Sign in before moving on.")
        else:
            func = reg_switcher.get(int(action_value), lambda: "Invalid input")
            if func() == 1:
                break

    i = 0
    while i != 4:
        print("\nPlease select ONLY the number to start an action!\n"
              "1. Create Recipe\n"
              "2. Edit Recipe\n"
              "3. Delete Recipe\n"
              "4. View my recipes\n"
              "5. Quit\n")

        action_switcher = {
            1: create_recipe,
            2: edit_recipe,
            3: delete_recipe,
            4: print_my_recipes,
            5: 5
        }

        action_value = input()

        if int(action_value) == 5:
            print("Session finished.")
            break

        func = action_switcher.get(int(action_value), lambda: "Invalid input")
        func()


def main_register():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    print("\n")

    register.register(username, password)
    return 1.1


def main_login():
    global global_username
    global user_id

    username = input("\nEnter username: ")
    password = input("Enter password: ")
    print("\n")

    a, log = login.login(username, password)

    leave = ""
    while not log:
        leave = input("Type 'quit' to exit or enter to retry.\n")
        if leave == "quit":
            break

        username = input("Enter username: ")
        password = input("Enter Password: ")
        print("\n")

        a, log = login.login(username, password)

    if leave == "quit":
        return 0
    global_username = username

    if log is not None:
        user_id = log

    return 1


def create_recipe():
    name = input("\nEnter recipe name: ")
    cook_time = input("Enter the cook time(minutes): ")
    description = input("Enter the recipes description: ")
    difficulty = input("Enter the recipes difficulty: ")
    servings = input("Enter the number of servings: ")
    creation_date = datetime.today().strftime('%Y-%m-%d')
    steps = input("Enter recipes steps: ")

    Recipe.create_recipe(name, cook_time, description, difficulty, servings, global_username, creation_date, steps)
    return 2.1


def edit_recipe():
    leave = 0
    print("\nIf you don't know the recipe's id you can look up your recipes on the home screen.")
    recipe_id = input("Enter recipe's id(or 'quit' to quit): ")
    if recipe_id == 'quit':
        return -1

    print("\nPlease select ONLY the number of the element you'd like to change\n"
          "1. Recipes name\n"
          "2. Cook time\n"
          "3. Description"
          "4. Difficulty\n"
          "5. Serving size\n"
          "6. Steps\n"
          "7. Quit\n")

    recipe_switcher = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7
    }
    change_recipe_val_input = input(": ")
    change_recipe_val = recipe_switcher.get(int(change_recipe_val_input), lambda: "Invalid input")

    if int(change_recipe_val) == 1:
        while leave_loop(leave) is False:
            recipe_name = input("\nEnter recipes name: ")
            try:
                Recipe.edit_recipe(recipe_name, None, None, None, None, None, recipe_id)
                return 1
            finally:
                print("Invalid input. \n")
                leave = input("Type 'quit' to exit or enter to retry.\n")

    elif change_recipe_val == 2:
        while leave_loop(leave) is False:
            cook_time = input("\nEnter recipes cook time: ")
            try:
                Recipe.edit_recipe(None, cook_time, None, None, None, None, recipe_id)
                return 1
            finally:
                print("Invalid input. \n")
                leave = input("Type 'quit' to exit or enter to retry.\n")

    elif change_recipe_val == 3:
        while leave_loop(leave) is False:
            description = input("\nEnter recipes description: ")
            try:
                Recipe.edit_recipe(None, None, None, description, None, None, recipe_id)
                return 1
            finally:
                print("Invalid input. \n")
                leave = input("Type 'quit' to exit or enter to retry.\n")

    elif change_recipe_val == 4:
        while leave_loop(leave) is False:
            difficulty = input("\nEnter recipes difficulty: ")
            try:
                Recipe.edit_recipe(None, None, None, difficulty, None, None, recipe_id)
                return 1
            finally:
                print("Invalid input. \n")
                leave = input("Type 'quit' to exit or enter to retry.\n")

    elif change_recipe_val == 5:
        while leave_loop(leave) is False:
            serving = input("\nEnter recipes serving size: ")
            try:
                Recipe.edit_recipe(None, None, None, None, serving, None, recipe_id)
                return 1
            finally:
                print("Invalid input. \n")
                leave = input("Type 'quit' to exit or enter to retry.\n")

    elif change_recipe_val == 6:
        while leave_loop(leave) is False:
            steps = input("\nEnter recipes steps: ")
            try:
                Recipe.edit_recipe(None, None, None, None, None, steps, recipe_id)
                return 1
            finally:
                print("Invalid input. \n")
                leave = input("Type 'quit' to exit or enter to retry.\n")

    elif change_recipe_val == 7:
        return -1
    else:
        print("Invalid input.")

    return 2.2


def delete_recipe():
    print("delete_recipe is not yet coded.")
    return 2.3


def print_my_recipes():
    Recipe.print_my_recipes(global_username)
    return 2.4


def leave_loop(leave):
    if leave == "quit":
        return True
    return False


# Driver program
if __name__ == "__main__":
    main()
