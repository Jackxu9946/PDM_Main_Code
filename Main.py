import login
import register
import Recipe


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

        action_value = input()

        if int(action_value) == 3 & signed_in == 1:
            break

        elif int(action_value) == 3:
            print("Sign in before moving on.")

        func = reg_switcher.get(int(action_value), lambda: "Invalid input")
        if func() == 1:
            break

    i = 0
    while i != 4:
        print("\nPlease select ONLY the number to start an action!\n"
              "1. Create Recipe\n"
              "2. Edit Recipe\n"
              "3. Delete Recipe\n"
              "4. Quit\n")

        action_switcher = {
            1: create_recipe,
            2: edit_recipe,
            3: delete_recipe,
            4: 4
        }

        action_value = input()

        if int(action_value) == 4:
            print("Session finished.")
            break

        func = action_switcher.get(int(action_value), lambda: "Invalid input")
        print(func())


def main_register():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    print("\n")

    reg = register.register(username, password)
    return 1.1


def main_login():
    username = input("\nEnter username: ")
    password = input("Enter password: ")
    print("\n")

    log = login.login(username, password)

    while not log:
        leave = input("Type 'quit' to exit or enter to retry.\n")
        if leave == "quit":
            break

        username = input("Enter username: ")
        password = input("Enter Password: ")
        print("\n")

        log = login.login(username, password)

    return 1


def create_recipe():
    return 2.1


def edit_recipe():
    return 2.2


def delete_recipe():
    return 2.3


# Driver program
if __name__ == "__main__":
    main()
