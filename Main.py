import login
import register
import Recipe
from datetime import datetime
import mark_recipe
import category

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
              "9. Add category\n"
              "10. Add recipe to a category\n"
              "11. Display my personal categories\n"
              "12. Show my current pantry\n"
              "13. Quit\n")

        recipe_switcher = {
            1: create_recipe,
            2: edit_recipe,
            3: delete_recipe,
            4: print_my_recipes,
            5: search_recipe,
            6: cook_recipe,
            7: add_pantry,
            8: update_pantry,
            9: add_category,
            10: add_recipe_to_category,
            11: display_my_category,
            12: show_pantry,
            13: 13
        }

        try:
            recipe_value = int(input(": "))
        except ValueError:
            print("Invalid input. Try again.")

        if recipe_value == 13:
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
    new_quantity = -1
    ingredient = []

    # RECIPE NAME
    while True:
        name = str(input("\nEnter recipe name: "))
        if name == "":
            print("Invalid name. Try again.")
        else:
            break

    # COOK TIME
    while True:
        cook_time = input("Enter the cook time(minutes): ")
        if name == "":
            print("Invalid name. Try again.")
        else:
            break

    # DESCRIPTION
    while True:
        description = input("Enter the recipes description: ")
        if name == "":
            print("Invalid name. Try again.")
        else:
            break

    # DIFFICULTY
    while True:
        difficulty = input("Enter the recipes difficulty: ")
        if name == "":
            print("Invalid name. Try again.")
        else:
            break

    # SERVING SIZE
    while True:
        servings = input("Enter the number of servings: ")
        if name == "":
            print("Invalid name. Try again.")
        else:
            break

    # STEPS
    while True:
        steps = input("Enter recipes steps: ")
        if name == "":
            print("Invalid name. Try again.")
        else:
            break

    # INGREDIENTS - QUANTITY
    while True:
        # Get ingredient name
        temp_list = []
        new_ingredient = input("Enter a new ingredient: ")
        if new_ingredient == "":
            pass
        new_ingredient.lower()

        # Get ingredient quantity
        try:
            new_quantity = int(input("Enter the ingredient quantity for the recipe: "))
        except ValueError:
            print("Invalid quantity. Try again.")
            pass

        temp_list.append(new_ingredient)
        temp_list.append(new_quantity)
        ingredient.append(temp_list)

        exit_val = input("Type Quit to quit or Press enter to add another ingredient: ")
        if exit_val == "Quit":
            break

    print(ingredient)
    creation_date = datetime.today().strftime('%Y-%m-%d')
    Recipe.create_recipe(name, cook_time, description, difficulty,
                         servings, int(user_id), creation_date, steps, ingredient)
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
    if type(change_recipe_val) is not int:
        print("Invalid input.")
        return -1

    if int(change_recipe_val) == 1:
        while leave_loop(leave) is False:
            recipe_name = input("\nRecipes Name: ")
            if recipe_name != "":
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
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 2:
        while leave_loop(leave) is False:
            cook_time = input("\nCook Time: ")
            if cook_time != "":
                try:
                    leave = Recipe.edit_recipe(None, cook_time, None, None, None, None, recipe_id)
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
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 3:
        while leave_loop(leave) is False:
            description = input("\nDescription: ")
            if description != "":
                try:
                    leave = Recipe.edit_recipe(None, None, description, None, None, None, recipe_id)
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
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 4:
        while leave_loop(leave) is False:
            difficulty = input("\nDifficulty: ")
            if difficulty != "":
                try:
                    leave = Recipe.edit_recipe(None, None, None, difficulty, None, None, recipe_id)
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
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 5:
        while leave_loop(leave) is False:
            serving = input("\nServing Size: ")
            if serving != "":
                try:
                    leave = Recipe.edit_recipe(None, None, None, None, serving, None, recipe_id)
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
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 6:
        while leave_loop(leave) is False:
            steps = input("\nSteps: ")
            if steps != "":
                try:
                    leave = Recipe.edit_recipe(None, None, None, None, None, steps, recipe_id)
                    if leave == -1:
                        print("Recipe steps was changed to", steps)
                    else:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or press enter to retry.\n")
                except ValueError:
                    print("Invalid input. \n")
                    leave = input("Type '-1' to exit or press enter to retry.\n")
                if leave == -1:
                    print("Exiting change recipe steps.")
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 7:
        return -1
    else:
        print("Invalid input.")

    return 2.2


def delete_recipe():
    del_recipe = 0
    while True:
        try:
            del_recipe = int(input("Recipe ID: "))
        except ValueError:
            print("Invalid input. Try again.")
            pass

        Recipe.delete_recipe(int(user_id), int(del_recipe))

        if del_recipe == -1:
            return -1


def print_my_recipes():
    result = Recipe.find_my_recipes(int(user_id))
    Recipe.print_my_recipe(result)

    while True:
        more_info = input("\nWould you like to see more information on a recipe?(Yes or No): ")
        if more_info == "":
            print("Can't be 'empty'. Try again.")
        elif more_info == "Yes":
            break
        elif more_info == "No":
            return
        else:
            print("Invalid input. Try again.")

    while True:
        try:
            recipe_id = int(input("Enter the recipe id of the recipe you would like see: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    Recipe.print_additional_info_recipe(recipe_id)
    return 2.4


def search_recipe():
    # print("search_recipe is not yet coded")
    # search_recipe_type = input("")
    # search_recipe_loop_val = True
    while True:
        search_recipe_type = input("Search by either (Ingredient, Name, Category): ")
        if search_recipe_type == "Ingredient":
            ingredient_name = input("Ingredient Name: ")
            search_recipe_mode(search_recipe_type, ingredient_name)
            break
        elif search_recipe_type == "Name":
            recipe_name = input("Recipe Name: ")
            search_recipe_mode(search_recipe_type, recipe_name)
            break
        elif search_recipe_type == "Category":
            category_name = input("Category Name: ")
            search_recipe_mode(search_recipe_type, category_name)
            break
        else:
            quit_val = input("Invalid search type. Enter Quit to quit: ")
            if quit_val == "Quit":
                break

        while True:
            more_info = input("\nWould you like to see more information on a recipe?(Yes or No): ")
            if more_info == "":
                print("Can't be 'empty'. Try again.")
            elif more_info == "Yes":
                break
            elif more_info == "No":
                return
            else:
                print("Invalid input. Try again.")

        while True:
            try:
                recipe_id = int(input("Enter the recipe id of the recipe you would like see: "))
                break
            except ValueError:
                print("Invalid input. Try again.")

        Recipe.print_additional_info_recipe(recipe_id)
    return 2.5


def search_recipe_mode(search_type, search_val):
    while True:
        search_recipe_mode_input = input("Result sorted by(Rating, Recent, Default): ")
        if search_recipe_mode_input == "Rating":
            if search_type == "Ingredient":
                result = Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break
            elif search_type == "Name":
                result = Recipe.search_recipe_by_name(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

            else:
                result = Recipe.search_recipe_by_category(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

        elif search_recipe_mode_input == "Recent":
            if search_type == "Ingredient":
                result = Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

            elif search_type == "Name":
                result = Recipe.search_recipe_by_name(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

            else:
                result = Recipe.search_recipe_by_category(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

        elif search_recipe_mode_input == "Default":
            if search_type == "Ingredient":
                result = Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

            elif search_type == "Name":
                result = Recipe.search_recipe_by_name(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

            else:
                result = Recipe.search_recipe_by_category(search_val, search_recipe_mode)
                Recipe.print_my_recipe(result)
                break

        else:
            quit_val = input("Invalid sort mode, Enter Quit to quit: ")
            if quit_val == "Quit":
                break


def add_category():
    category_name = input("Category Name: ")
    category.create_categories(category_name, global_username)
    category.display_category(user_id)


def display_my_category():
    category.display_category(user_id)


def add_recipe_to_category():
    print("add recipe to category")


def cook_recipe():
    while True:
        try:
            recipe_id = int(input("Enter the recipe id of the recipe you would like to cook: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    while True:
        try:
            scale = int(input("Enter the scale of the current recipe you would like to cook: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    mark_recipe.mark_recipe(user_id, recipe_id, scale)
    return 2.5


def add_pantry():

    # INGREDIENT NAME
    while True:
        ingredient_name = input("\nEnter ingredients name: ")
        ingredient_name.lower()
        if ingredient_name == "":
            print("Invalid name. Try again.")
        else:
            break

    # INGREDIENT QUANTITY
    while True:
        try:
            ingredient_quantity = int(input("Enter ingredients quantity: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    mark_recipe.add_ingredient_to_pantry(user_id, ingredient_name.lower(), ingredient_quantity)
    return 2.5


def update_pantry():

    # INGREDIENT NAME
    while True:
        ingredient_name = input("\nEnter ingredients name: ")
        ingredient_name.lower()
        if ingredient_name == "":
            print("Invalid name. Try again.")
        else:
            break

    # INGREDIENT QUANTITY
    while True:
        try:
            ingredient_quantity = int(input("Enter ingredients new quantity: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    mark_recipe.update_pantry(user_id, ingredient_name.lower(), ingredient_quantity)
    return 2.5


def show_pantry():
    mark_recipe.show_pantry(user_id)


def leave_loop(leave):
    if leave == -1:
        return True
    return False


# Driver program
if __name__ == "__main__":
    main()
    # search_recipe()
