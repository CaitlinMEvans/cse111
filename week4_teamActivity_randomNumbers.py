import random

def append_random_numbers(numbers_list, quantity=1):
    """
    Appends a specified quantity of random numbers to the given list.

    Parameters:
        numbers_list (list): The list to which random numbers will be appended.
        quantity (int): The number of random numbers to append. Default is 1.
    """
    for _ in range(quantity):
        random_number = round(random.uniform(0, 100), 1)
        numbers_list.append(random_number)

def append_random_words(words_list, quantity=1):
    """
    Appends a specified quantity of random words to the given list.

    Parameters:
        words_list (list): The list to which random words will be appended.
        quantity (int): The number of random words to append. Default is 1.
    """
    word_pool = ["join", "love", "smile", "cloud", "head"]
    for _ in range(quantity):
        random_word = random.choice(word_pool)
        words_list.append(random_word)

def main():
    """
    Main function to demonstrate appending random numbers and words to lists.
    """
    # Core Requirement: Random Numbers
    numbers = [16.2, 75.1, 52.3]
    print("numbers", numbers)

    # Append one random number
    append_random_numbers(numbers)
    print("numbers", numbers)

    # Append three random numbers
    append_random_numbers(numbers, 3)
    print("numbers", numbers)

    # Stretch Challenge: Random Words
    words = ["join", "love", "smile"]
    print("words", words)

    # Append two random words
    append_random_words(words, 2)
    print("words", words)

# Call the main function
if __name__ == "__main__":
    main()