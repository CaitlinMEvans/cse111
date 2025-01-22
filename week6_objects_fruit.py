# Added Creativity:
# Added user input a fruit to append, remove, or find its index in the list.
# Created a history log that shows the state of the list after each modification.
# I also made the fruit case-insensitively during operations like searching or removing.

def main():
    # Create and print the original list
    fruit_list = ["pear", "banana", "apple", "mango"]
    print(f"original: {fruit_list}")

    # Initialize a history log to track changes
    history = [fruit_list.copy()]

    # Reverse and print the list
    fruit_list.reverse()
    print(f"reversed: {fruit_list}")
    history.append(fruit_list.copy())

    # Append "orange" and print the list
    fruit_list.append("orange")
    print(f"append orange: {fruit_list}")
    history.append(fruit_list.copy())

    # Find "apple" and insert "cherry" before it
    apple_index = fruit_list.index("apple")
    fruit_list.insert(apple_index, "cherry")
    print(f"insert cherry: {fruit_list}")
    history.append(fruit_list.copy())

    # Remove "banana" and print the list
    fruit_list.remove("banana")
    print(f"remove banana: {fruit_list}")
    history.append(fruit_list.copy())

    # Pop the last element and print the result
    last_element = fruit_list.pop()
    print(f"pop {last_element}: {fruit_list}")
    history.append(fruit_list.copy())

    # Sort the list and print it
    fruit_list.sort()
    print(f"sorted: {fruit_list}")
    history.append(fruit_list.copy())

    # Clear the list and print it
    fruit_list.clear()
    print(f"cleared: {fruit_list}")
    history.append(fruit_list.copy())

    # Allow user interaction
    print("\nUser Interaction Section:")
    fruit_list = ["pear", "banana", "apple", "mango"]  # Reset the list for user interaction
    while True:
        print(f"Current list: {fruit_list}")
        print("Choose an operation:")
        print("1. Append a fruit")
        print("2. Remove a fruit")
        print("3. Find the index of a fruit")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            fruit = input("Enter a fruit to append: ").strip()
            fruit_list.append(fruit)
            print(f"append {fruit}: {fruit_list}")
            history.append(fruit_list.copy())
        elif choice == "2":
            fruit = input("Enter a fruit to remove: ").strip().lower()
            for f in fruit_list:
                if f.lower() == fruit:
                    fruit_list.remove(f)
                    print(f"remove {f}: {fruit_list}")
                    history.append(fruit_list.copy())
                    break
            else:
                print(f"{fruit} not found in the list.")
        elif choice == "3":
            fruit = input("Enter a fruit to find its index: ").strip().lower()
            for i, f in enumerate(fruit_list):
                if f.lower() == fruit:
                    print(f"{f} is at index {i}")
                    break
            else:
                print(f"{fruit} not found in the list.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    # Print the history log at the end
    print("\nHistory of Changes:")
    for step, state in enumerate(history):
        print(f"Step {step + 1}: {state}")


# Call the main function
if __name__ == "__main__":
    main()