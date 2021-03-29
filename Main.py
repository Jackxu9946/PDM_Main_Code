
def main():

    i = 0
    while i != 4:
        print("\nPlease select ONLY the number to start an action!\n"
              "1. Create_Recipe\n"
              "2. Edit Recipe\n"
              "3. Delete Recipe\n"
              "4. Quit\n")

        switcher = {
            1: Create_Recipe,
            2: Edit_Recipe,
            3: Delete_Recipe,
            4: 4
        }

        action_value = input()

        if int(action_value) == 4:
            print("Session finished.")
            break

        func = switcher.get(int(action_value), lambda: "Invalid input")
        print(func())


def Create_Recipe():
    return 1


def Edit_Recipe():
    return 2


def Delete_Recipe():
    return 3


# Driver program
if __name__ == "__main__":
    main()
