import csv

def read_dictionary(filename):
    """
    Read the contents of a CSV file into a dictionary and return the dictionary.

    Parameters:
        filename: the name of the CSV file to read.

    Return:
        A dictionary where the keys are student I-Numbers (as strings)
        and the values are student names (as strings).
    """
    dictionary = {}
    with open(filename, "rt") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            i_number = row[0].strip()  # Strip whitespace from I-Number
            name = row[1].strip()     # Strip whitespace from Name
            dictionary[i_number] = name
    return dictionary

def main():
    filename = "students.csv"
    # Read the CSV file into a dictionary
    students = read_dictionary(filename)
    
    # Prompt the user for an I-Number
    i_number = input("Please enter an I-Number (xxxxxxxxx): ").strip()
    
    # Look up the I-Number in the dictionary
    if i_number in students:
        print(students[i_number])
    else:
        print("No such student")

if __name__ == "__main__":
    main()
