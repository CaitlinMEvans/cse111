# Added Creativity: added better UX - theres a catch for invalid number of digits for I-Number and gave option to enter name or I-Number
import csv

def read_dictionary(filename, key_column_index):
    """
    Read the contents of a CSV file into a compound dictionary.
    Parameters:
        filename: the name of the CSV file to read.
        key_column_index: the index of the column to use as the keys in the dictionary.
    Return: a compound dictionary that contains the contents of the CSV file.
    """
    dictionary = {}
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) > key_column_index:
                key = row[key_column_index].strip()  # Strip spaces from the key
                value = row[1].strip()  # Assume the name is in the second column
                dictionary[key] = value  # Store the name as the value
    return dictionary


def main():
    filename = "students.csv"
    key_column_index = 0
    students_dict = read_dictionary(filename, key_column_index)

    while True:
        print("\nSearch Options:")
        print("1. Search by I-Number")
        print("2. Search by Name")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            search_by_inumber(students_dict)
        elif choice == "2":
            search_by_name(students_dict)
        elif choice == "3":
            print("Thanks for using Caitlin's Student Directory! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def search_by_inumber(students_dict):
    while True:
        inumber = input("Please enter an I-Number (xxxxxxxxx) or 'quit' to exit: ").replace("-", "").strip()

        if inumber.lower() == "quit":
            return

        if not inumber.isdigit():
            print("Invalid I-Number: contains non-numeric characters.")
        elif len(inumber) < 9:
            print("Invalid I-Number: too few digits.")
        elif len(inumber) > 9:
            print("Invalid I-Number: too many digits.")
        elif inumber not in students_dict:
            print("No such student.")
        else:
            print(f"Student Name: {students_dict[inumber]}")
            return


def search_by_name(students_dict):
    name = input("Please enter the student's name: ").strip().lower()
    found_students = {key: value for key, value in students_dict.items() if value.lower() == name}

    if not found_students:
        print("No student found with that name.")
    else:
        print("Search Results:")
        for inumber, student_name in found_students.items():
            print(f"I-Number: {inumber}, Name: {student_name}")


if __name__ == "__main__":
    main()