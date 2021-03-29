
def main():

    i = 0
    while i != 4:
        print("\nPlease select ONLY the number to start an action!\n"
              "1. Register"
              "2. Login"
              "3. Create Recipe\n"
              "4. Edit Recipe\n"
              "5. Delete Recipe\n"
              "6. Quit\n")

        switcher = {
            1: register,
            2: login,
            3: create_recipe,
            4: edit_recipe,
            5: delete_recipe,
            6: 4
        }

        action_value = input()

        if int(action_value) == 6:
            print("Session finished.")
            break

        func = switcher.get(int(action_value), lambda: "Invalid input")
        print(func())


def register():
    return 1


def login():
    return 2


def create_recipe():
    return 3


def edit_recipe():
    return 4


def delete_recipe():
    return 5


# Driver program
if __name__ == "__main__":
    main()
