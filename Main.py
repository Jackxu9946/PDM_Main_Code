import login
import register
import Recipe
from datetime import datetime

global_username = ""
user_id = -1


def main():
    action_value = 0
    recipe_value = 0
    signed_in = 0

    # SIGN IN/REGISTER LOOP
    while True:
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

        # User input test clause
        try:
            action_value = int(input(": "))
        except ValueError:
            print("Invalid input. Try again.")

        # Valid user input - Checking to exit loop or calling function
        if action_value == 3 & signed_in == 1:
            break
        elif action_value == 3:
            print("Sign in before moving on.")
        else:
            func = reg_switcher.get(action_value, lambda: "Invalid input")
            if func() == 1:
                break

    # MAIN USER ACTION LOOP
    while True:
        print("\nPlease select ONLY the number to start an action!\n"
              "1. Create Recipe\n"
              "2. Edit Recipe\n"
              "3. Delete Recipe\n"
              "4. View my recipes\n"
              "5. Search for a recipe\n"
              "6. Cook a recipe\n"
              "7. Add to pantry\n"
              "8. Update pantry\n"
              "9. Quit\n")

        recipe_switcher = {
            1: create_recipe,
            2: edit_recipe,
            3: delete_recipe,
            4: print_my_recipes,
            5: search_recipe,
            6: cook_recipe,
            7: add_pantry,
            8: update_pantry,
            9: 9
        }

        try:
            recipe_value = int(input(": "))
        except ValueError:
            print("Invalid input. Try again.")

        if recipe_value == 9:
            print("Session finished.")
            break
        else:
            func = recipe_switcher.get(recipe_value, lambda: "Invalid input")
            func()


# REGISTER
def main_register():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    print("\n")

    register.register(username, password)
    return 1.1


# LOGIN
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


# CREATE RECIPE
def create_recipe():
    name = str(input("\nEnter recipe name: "))
    cook_time = input("Enter the cook time(minutes): ")
    description = input("Enter the recipes description: ")
    difficulty = input("Enter the recipes difficulty: ")
    servings = input("Enter the number of servings: ")
    creation_date = datetime.today().strftime('%Y-%m-%d')
    steps = input("Enter recipes steps: ")

    Recipe.create_recipe(name, cook_time, description, difficulty, servings, int(user_id), creation_date, steps)
    return 2.1


# EDIT RECIPE
def edit_recipe():
    leave = 0
    recipe_id = 0
    change_recipe_val = 0
    change_recipe_val_input = 0

    print("\nIf you don't know the recipe's id you can look up your recipes on the home screen.")

    while recipe_id is 0:
        try:
            recipe_id = int(input("Enter recipe's id(or '-1' to quit): "))
        except ValueError:
            print("Invalid input. Try again.")
            return -1

        if recipe_id == -1:
            return -1

    print("\nPlease select ONLY the number of the element you'd like to change\n"
          "1. Recipes name\n"
          "2. Cook time\n"
          "3. Description\n"
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

    try:
        change_recipe_val_input = int(input(": "))
    except ValueError:
        print("Invalid input. Try again.")
        return -1

    change_recipe_val = recipe_switcher.get(change_recipe_val_input, lambda: "Invalid input")

    if int(change_recipe_val) == 1:
        while leave_loop(leave) is False:
            recipe_name = input("\nEnter recipes name: ")
            try:
                leave = Recipe.edit_recipe(recipe_name, None, None, None, None, None, recipe_id)
                if leave == -1:
                    print("Recipe name was changed to", recipe_name)
                else:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or enter to retry.\n")
            except ValueError:
                print("Invalid input. \n")
                leave = input("Type '-1' to exit or enter to retry.\n")
            if leave == -1:
                print("Exiting change recipe.")

    elif change_recipe_val == 2:
        while leave_loop(leave) is False:
            cook_time = input("\nEnter recipes cook time: ")
            try:
                Recipe.edit_recipe(None, cook_time, None, None, None, None, recipe_id)
                if leave == -1:
                    print("Recipe cook time was changed to", cook_time)
                else:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or enter to retry.\n")
            except ValueError:
                print("Invalid input. \n")
                leave = input("Type '-1' to exit or enter to retry.\n")
            if leave == -1:
                print("Exiting change recipe cook time.")

    elif change_recipe_val == 3:
        while leave_loop(leave) is False:
            description = input("\nEnter recipes description: ")
            try:
                Recipe.edit_recipe(None, None, description, None, None, None, recipe_id)
                if leave == -1:
                    print("Recipe description was changed to", description)
                else:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or enter to retry.\n")
            except ValueError:
                print("Invalid input. \n")
                leave = input("Type '-1' to exit or enter to retry.\n")
            if leave == -1:
                print("Exiting change recipe description.")

    elif change_recipe_val == 4:
        while leave_loop(leave) is False:
            difficulty = input("\nEnter recipes difficulty: ")
            try:
                Recipe.edit_recipe(None, None, None, difficulty, None, None, recipe_id)
                if leave == -1:
                    print("Recipe difficulty was changed to", difficulty)
                else:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or enter to retry.\n")
            except ValueError:
                print("Invalid input. \n")
                leave = input("Type '-1' to exit or enter to retry.\n")
            if leave == -1:
                print("Exiting change difficulty.")

    elif change_recipe_val == 5:
        while leave_loop(leave) is False:
            serving = input("\nEnter recipes serving size: ")
            try:
                Recipe.edit_recipe(None, None, None, None, serving, None, recipe_id)
                if leave == -1:
                    print("Recipe serving size was changed to", serving)
                else:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or enter to retry.\n")
            except ValueError:
                print("Invalid input. \n")
                leave = input("Type '-1' to exit or enter to retry.\n")
            if leave == -1:
                print("Exiting change serving size.")

    elif change_recipe_val == 6:
        while leave_loop(leave) is False:
            steps = input("\nEnter recipes steps: ")
            try:
                Recipe.edit_recipe(None, None, None, None, None, steps, recipe_id)
                if leave == -1:
                    print("Recipe steps was changed to", steps)
                else:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or enter to retry.\n")
            except ValueError:
                print("Invalid input. \n")
                leave = input("Type '-1' to exit or enter to retry.\n")
            if leave == -1:
                print("Exiting change recipe steps.")

    elif change_recipe_val == 7:
        return -1
    else:
        print("Invalid input.")

    return 2.2


def delete_recipe():
    del_recipe = input("Enter the recipe's ID you would like to delete: \n")
    Recipe.delete_recipe(int(user_id), int(del_recipe))
    return 2.3


def print_my_recipes():
    result = Recipe.find_my_recipes(int(user_id))
    Recipe.print_my_recipe(result)
    return 2.4


def search_recipe():
    print("search_recipe is not yet coded")
    return 2.5


def cook_recipe():
    print("cook_recipe is not yet coded")
    return 2.5


def add_pantry():
    print("add_pantry is not yet coded")
    return 2.5


def update_pantry():
    print("update_pantry is not yet coded")
    return 2.5


def leave_loop(leave):
    if leave == -1:
        return True
    return False


# Driver program
if __name__ == "__main__":
    main()
