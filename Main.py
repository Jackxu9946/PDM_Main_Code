import login
import register
import Recipe
from datetime import datetime
import mark_recipe
import category
import most_recent_recipe
import recommended_recipes
import recipe_based_on_pantry

# GLOBAL ATTRIBUTES
global_username = ""
user_id = -1


# MAIN
def main():
    action_value = 0
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
        recipe_value = 0
        print("\nPlease select ONLY the number to start an action!\n"
              "1.  Create Recipe\n"
              "2.  Edit Recipe\n"
              "3.  Delete Recipe\n"
              "4.  View my recipes\n"
              "5.  Show recipes you have made\n"
              "6.  Search for a recipe\n"
              "7.  Cook a recipe\n"
              "8.  Add to pantry\n"
              "9.  Update pantry\n"
              "10. Add category\n"
              "11. Add recipe to a category\n"
              "12. Display my personal categories\n"
              "13. Show my current pantry\n"
              "14. Show Top 50 Most Recommended Recipes\n"
              "15. Show 50 Most Recent Recipes\n"
              "16. Show Recommended Recipes Made by Other Users Who Make the Same Recipes\n"
              "17. Show Possible Recipe to Make Based on Ingredients in the Pantry\n"
              "18. Quit\n")

        recipe_switcher = {
            1: create_recipe,
            2: edit_recipe,
            3: delete_recipe,
            4: print_my_recipes,
            5: show_recipe_made_by_you,
            6: search_recipe,
            7: cook_recipe,
            8: add_pantry,
            9: update_pantry,
            10: add_category,
            11: add_recipe_to_category,
            12: display_my_category,
            13: show_pantry,
            14: show_50_most_recommended_recipe,
            15: show_50_most_recent_recipe,
            16: show_recommended_to_you,
            17: show_recipe_based_on_pantry,
            18: 18
        }

        try:
            recipe_value = int(input(": "))
        except ValueError:
            print("Invalid input. Try again.")

        if recipe_value == 18:
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

    press_to_continue()

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
        if cook_time == "" or not cook_time.isnumeric() or int(cook_time) < 1:
            print("Invalid cook_time. Try again.")
        else:
            break

    # DESCRIPTION
    while True:
        description = input("Enter the recipes description: ")
        if description == "":
            print("Invalid description. Try again.")
        else:
            break

    # DIFFICULTY
    while True:
        dic = {'1': 'Easy', '2': 'Easy-Medium', '3': 'Medium', '4': 'Medium-Hard', '5': 'Hard'}
        difficulty = input("1. Easy \n2. Easy-Medium\n3. Medium \n4. Medium-Hard \n5. Hard\n"
                           "Enter a number corresponding to the recipe difficulty: ")
        if difficulty == "" or not difficulty.isnumeric() or int(difficulty) not in range(1, 6):
            print("Invalid difficulty. Try again.")
        else:
            difficulty = dic[difficulty]
            break

    # SERVING SIZE
    while True:
        servings = input("Enter the number of servings: ")
        if servings == "" or not servings.isnumeric() or int(servings) < 1:
            print("Invalid servings. Try again.")
        else:
            break

    # STEPS
    while True:
        steps = input("Enter recipes steps: ")
        if steps == "":
            print("Invalid steps. Try again.")
        else:
            break

    # INGREDIENTS - QUANTITY
    while True:
        # Get ingredient name
        temp_list = []
        while True:
            new_ingredient = input("Enter a new ingredient: ")
            if new_ingredient == "":
                print("Invalid ingredient Name. Try again.")
            else:
                new_ingredient.lower()
                break

        # Get ingredient quantity
        while True:
            new_quantity = input("Enter the ingredient quantity for the recipe: ")
            if new_quantity == "" or not new_quantity.isnumeric() or int(new_quantity) < 1:
                print("Invalid quantity. Try again.")
            else:
                new_quantity = int(new_quantity)
                break

        temp_list.append(new_ingredient.lower())
        temp_list.append(new_quantity)
        ingredient.append(temp_list)

        exit_val = input("Type Quit to quit or Press enter to add another ingredient: ")
        if exit_val == "Quit":
            break

    # print(ingredient)
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Recipe.create_recipe(name, cook_time, description, difficulty,
                         servings, int(user_id), creation_date, steps, ingredient)
    press_to_continue()
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
                    if leave != -1:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or enter to retry.\n")
                except ValueError:
                    print("Invalid input. Try again.\n")
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 2:
        # if cook_time == "" or not cook_time.isnumeric() or int(cook_time) < 1:
        while leave_loop(leave) is False:
            cook_time = input("\nCook Time: ")
            if cook_time != "" and cook_time.isnumeric() and int(cook_time) > 0:
                try:
                    leave = Recipe.edit_recipe(None, cook_time, None, None, None, None, recipe_id)
                    if leave != -1:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or enter to retry.\n")
                except ValueError:
                    print("Invalid input. \n")
            else:
                print("Value is not allowed. Try again.")

    elif change_recipe_val == 3:
        while leave_loop(leave) is False:
            description = input("\nDescription: ")
            if description != "":
                try:
                    leave = Recipe.edit_recipe(None, None, description, None, None, None, recipe_id)
                    if leave != -1:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or enter to retry.\n")
                except ValueError:
                    print("Invalid input. \n")
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 4:
        dic = {'1': 'Easy', '2': 'Easy-Medium', '3': 'Medium', '4': 'Medium-Hard', '5': 'Hard'}
        while leave_loop(leave) is False:
            difficulty = input("1. Easy \n2. Easy-Medium\n3. Medium \n4. Medium-Hard \n5. Hard\n"
                               "Enter a number corresponding to the recipe difficulty: ")
            if difficulty != "" and difficulty.isnumeric() and int(difficulty) in range(1,6):
                try:
                    difficulty = dic[difficulty]
                    leave = Recipe.edit_recipe(None, None, None, difficulty, None, None, recipe_id)
                    if leave != -1:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or enter to retry.\n")
                except ValueError:
                    print("Invalid input. \n")
            else:
                print("Value is not allowed. Try again.")

    elif change_recipe_val == 5:
        # servings = input("Enter the number of servings: ")
        # if servings == "" or not servings.isnumeric() or int(servings) < 1:

        while leave_loop(leave) is False:
            serving = input("\nServing Size: ")
            if serving != "" and serving.isnumeric() and int(serving) > 0:
                try:
                    leave = Recipe.edit_recipe(None, None, None, None, serving, None, recipe_id)
                    if leave != -1:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or enter to retry.\n")
                except ValueError:
                    print("Invalid input. \n")
            else:
                print("Value is not allowed. Try again.")

    elif change_recipe_val == 6:
        while leave_loop(leave) is False:
            steps = input("\nSteps: ")
            if steps != "":
                try:
                    leave = Recipe.edit_recipe(None, None, None, None, None, steps, recipe_id)
                    if leave != -1:
                        print("Invalid input. \n")
                        leave = input("Type '-1' to exit or press enter to retry.\n")
                except ValueError:
                    print("Invalid input. \n")
            else:
                print("'Empty' value is not allowed. Try again.")

    elif change_recipe_val == 7:
        return -1
    else:
        print("Invalid input.")
    press_to_continue()
    return 2.2


# DELETE RECIPE
def delete_recipe():
    del_recipe = 0
    while True:
        try:
            del_recipe = int(input("Enter the recipe id of the recipe you'd like to delete: "))
            if del_recipe == "":
                print("Can't be 'empty'. Try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Try again.")
            pass

        if del_recipe == -1:
            return -1

    Recipe.delete_recipe(int(user_id), int(del_recipe))
    press_to_continue()
    return


# PRINT MY RECIPES
def print_my_recipes():
    result = Recipe.find_my_recipes(int(user_id))
    Recipe.print_my_recipe(result)

    press_to_continue()

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
    press_to_continue()
    return 2.4


# SEARCH RECIPE
def search_recipe():
    # print("search_recipe is not yet coded")
    # search_recipe_type = input("")
    # search_recipe_loop_val = True
    while True:
        search_recipe_type = input("Search by either (Ingredient, Name, Category): ")
        if search_recipe_type == "Ingredient":
            ingredient_name = input("Ingredient Name: ")
            # ingredient_name.lower()
            # search_recipe_mode(search_recipe_type, ingredient_name)
            search_recipe_mode(search_recipe_type, ingredient_name.lower())
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
    return 2.5


# SEARCH RECIPE MODE
def search_recipe_mode(search_type, search_val):
    while True:
        search_recipe_mode_input = input("Result sorted by(Rating, Recent, Default): ")
        search_recipe_mode_input2 = search_recipe_mode_input.lower()

        if search_recipe_mode_input2 == "rating":
            if search_type == "Ingredient":
                result = Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode_input2)
                Recipe.print_my_recipe(result)
                get_more_info()
                break
            elif search_type == "Name":
                result = Recipe.search_recipe_by_name(search_val, search_recipe_mode_input2)
                Recipe.print_my_recipe(result)
                get_more_info()
                break

            else:
                result = Recipe.search_recipe_by_category(search_val, search_recipe_mode_input2)
                Recipe.print_my_recipe(result)
                get_more_info()
                break

        elif search_recipe_mode_input2 == "recent":
            if search_type == "Ingredient":
                # result = Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode)
                # Recipe.print_my_recipe(result)
                Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode_input2)
                get_more_info()
                break

            elif search_type == "Name":
                # result = Recipe.search_recipe_by_name(search_val, search_recipe_mode)
                # Recipe.print_my_recipe(result)
                Recipe.search_recipe_by_name(search_val, search_recipe_mode_input2)
                get_more_info()
                break

            else:
                # result = Recipe.search_recipe_by_category(search_val, search_recipe_mode)
                # Recipe.print_my_recipe(result)
                Recipe.search_recipe_by_category(search_val, search_recipe_mode_input2)
                get_more_info()
                break

        elif search_recipe_mode_input2 == "default":
            if search_type == "Ingredient":
                result = Recipe.search_recipe_by_ingredient(search_val, search_recipe_mode_input2)
                Recipe.print_my_recipe(result)
                get_more_info()
                break

            elif search_type == "Name":
                result = Recipe.search_recipe_by_name(search_val, search_recipe_mode_input2)
                Recipe.print_my_recipe(result)
                get_more_info()
                break

            else:
                result = Recipe.search_recipe_by_category(search_val, search_recipe_mode_input2)
                Recipe.print_my_recipe(result)
                get_more_info()
                break

        else:
            quit_val = input("Invalid sort mode, Enter Quit to quit: ")
            if quit_val == "Quit":
                break


# ADD CATEGORY
def add_category():
    # CATEGORY NAME
    while True:
        category_name = input("\nEnter categories name: ")
        if category_name == "":
            print("Invalid name. Try again.")
        else:
            break

    category.create_categories(category_name, global_username)
    category.display_category(user_id)
    press_to_continue()


# DISPLAY CATEGORY
def display_my_category():
    category.display_category(int(user_id))

    while True:
        response1 = input("\nDo you want to open the category? (Yes/No) ")

        if response1.lower() == 'yes':
            response2 = input("Enter category ID: ")
            response3 = input("Enter category name: ")

            if not category.open_category(response2, response3, user_id):
                pass
            else:
                break
        elif response1.lower() == 'no':
            break
        else:
            print("Invalid inputs!")

    press_to_continue()


def show_recipe_made_by_you():
    Recipe.show_past_made_recipe(user_id)
    press_to_continue()

# ADD RECIPE TO CATEGORY
def add_recipe_to_category():
    # INGREDIENT QUANTITY
    while True:
        try:
            category_id = int(input("Enter the category id: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    # INGREDIENT QUANTITY
    while True:
        try:
            recipe_id = int(input("Enter the recipe id: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

    category.add_recipes(category_id, recipe_id)
    press_to_continue()


# COOK RECIPE
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
    press_to_continue()
    return 2.5


# ADD INGREDIENT TO PANTRY
def add_pantry():
    # INGREDIENT NAME
    while True:
        ingredient_name = input("\nEnter ingredient name: ")
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
    ingredient_name.lower()
    mark_recipe.add_ingredient_to_pantry(user_id, ingredient_name, ingredient_quantity)
    press_to_continue()
    return 2.5


# UPDATE PANTRY
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

    mark_recipe.update_pantry(user_id, ingredient_name, ingredient_quantity)
    press_to_continue()
    return 2.5


# SHOW PANTRY
def show_pantry():
    mark_recipe.show_pantry(user_id)
    press_to_continue()


# DISPLAY 50 MOST RECENT RECIPES
def show_50_most_recent_recipe():
    most_recent_recipe.most_recent_recipe()
    press_to_continue()


# DISPLAY 50 MOST RECOMMENDED RECIPES
def show_50_most_recommended_recipe():
    most_recent_recipe.top_50_recommended_recipe()
    press_to_continue()


# DISPLAY MOST POPULAR INGREDIENTS
# def show_most_popular_ingredients():
    # most_recent_recipe.most_popular_ingredients_by_year()
    # press_to_continue()


# DISPLAY RECOMMENDED RECIPES MADE BY OTHER USERS WHO MAKE THE SAME RECIPES
def show_recommended_to_you():
    recommended_recipes.recommending_recipes(user_id)
    press_to_continue()


# DISPLAY RECIPE BASED ON INGREDIENTS IN THE PANTRY
def show_recipe_based_on_pantry():
    recipe_based_on_pantry.find_recipe_based_on_pantry(user_id)
    press_to_continue()


# HELPER METHODS
def leave_loop(leave):
    if leave == -1:
        return True
    return False


def get_more_info():
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
    press_to_continue()


def press_to_continue():
    user_input = input()
    if user_input is not None:
        return


# Driver program
if __name__ == "__main__":
    main()
