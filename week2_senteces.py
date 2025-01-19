import random

def get_determiner(quantity):
    """Return a randomly chosen determiner.
    If quantity is 1, this function will return
    a determiner for a single noun. Otherwise,
    it will return a determiner for a plural noun."""
    if quantity == 1:
        words = ["a", "one", "the"]
    else:
        words = ["some", "many", "the"]
    return random.choice(words)

def get_noun(quantity):
    """Return a randomly chosen noun.
    If quantity is 1, this function will return
    a single noun. Otherwise, it will return a plural noun."""
    if quantity == 1:
        nouns = ["bird", "boy", "car", "cat", "child", 
                 "dog", "girl", "man", "rabbit", "woman"]
    else:
        nouns = ["birds", "boys", "cars", "cats", "children", 
                 "dogs", "girls", "men", "rabbits", "women"]
    return random.choice(nouns)

def get_verb(quantity, tense):
    """Return a randomly chosen verb based on the tense.
    - Past tense verbs are the same for singular and plural.
    - Present tense verbs differ for singular and plural.
    - Future tense verbs are the same for singular and plural."""
    if tense == "past":
        verbs = ["drank", "ate", "grew", "laughed", "thought", 
                 "ran", "slept", "talked", "walked", "wrote"]
    elif tense == "present":
        if quantity == 1:
            verbs = ["drinks", "eats", "grows", "laughs", "thinks", 
                     "runs", "sleeps", "talks", "walks", "writes"]
        else:
            verbs = ["drink", "eat", "grow", "laugh", "think", 
                     "run", "sleep", "talk", "walk", "write"]
    elif tense == "future":
        verbs = ["will drink", "will eat", "will grow", "will laugh", 
                 "will think", "will run", "will sleep", "will talk", 
                 "will walk", "will write"]
    return random.choice(verbs)

def make_sentence(quantity, tense):
    """Build and return a grammatically correct sentence."""
    determiner = get_determiner(quantity)
    noun = get_noun(quantity)
    verb = get_verb(quantity, tense)
    sentence = f"{determiner.capitalize()} {noun} {verb}."
    return sentence

def main():
    """Generate and print six sentences with varying quantities and tenses."""
    print(make_sentence(1, "past"))  # Single, Past
    print(make_sentence(1, "present"))  # Single, Present
    print(make_sentence(1, "future"))  # Single, Future
    print(make_sentence(2, "past"))  # Plural, Past
    print(make_sentence(2, "present"))  # Plural, Present
    print(make_sentence(2, "future"))  # Plural, Future

# Call the main function to execute the program
main()
