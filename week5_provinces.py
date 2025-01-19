def main():
    # Open the file containing the provinces and read its contents.
    # We'll ensure each line becomes an element in a list.
    with open("week5_provinces.txt", "r") as file:
        provinces = [line.strip() for line in file.readlines()]

    # This is the original list of provinces
    print(provinces)

    # Removing the first element in the list—it’s not needed for our analysis.
    provinces.pop(0)

    # Removing the last element since it's extra information.
    provinces.pop(-1)

    # Replace every occurrence of "AB" with "Alberta".
    # This ensures consistency in the list.
    provinces = ["Alberta" if province == "AB" else province for province in provinces]

    # Count how many times "Alberta" appears in the modified list.
    alberta_count = provinces.count("Alberta")

    # Result: the total number of "Alberta" occurrences.
    print(f"Alberta occurs {alberta_count} times in the modified list.")

if __name__ == "__main__":
    main()
