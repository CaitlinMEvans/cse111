# This program generates simple sentences and has been enhanced to include adjectives and adverbs for added creativity.
#updated for missing ruberic items get_preposition / get_prepositional_phrase not explicitly outlined in the instructions for the mid week
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

def get_adjective():
    """Return a randomly chosen adjective."""
    adjectives = ["red", "happy", "quick", "bright", "clever", 
                  "kind", "lazy", "brave", "shy", "calm"]
    return random.choice(adjectives)

def get_adverb():
    """Return a randomly chosen adverb."""
    adverbs = ["quickly", "sweetly", "calmly", "happily", "gracefully", 
               "silently", "bravely", "boldly", "sadly", "angrily"]
    return random.choice(adverbs)

def get_preposition():
    """Return a randomly chosen preposition."""
    prepositions = ["about", "above", "across", "after", "along",
                    "around", "at", "before", "behind", "below",
                    "beyond", "by", "despite", "except", "for",
                    "from", "in", "into", "near", "of",
                    "off", "on", "onto", "out", "over",
                    "past", "to", "under", "with", "without"]
    return random.choice(prepositions)

def get_prepositional_phrase(quantity):
    """Build and return a prepositional phrase."""
    preposition = get_preposition()
    determiner = get_determiner(quantity)
    noun = get_noun(quantity)
    return f"{preposition} {determiner} {noun}"

def make_sentence(quantity, tense):
    """Build and return a grammatically correct sentence."""
    # Include a determiner, adjective, noun, adverb, and verb to build a more dynamic sentence.
    determiner = get_determiner(quantity)
    adjective = get_adjective()
    noun = get_noun(quantity)
    verb = get_verb(quantity, tense)
    adverb = get_adverb()
    prepositional_phrase = get_prepositional_phrase(quantity)
    sentence = f"{determiner.capitalize()} {adjective} {noun} {adverb} {verb} {prepositional_phrase}."
    return sentence

def main():
    """Generate and print six sentences with varying quantities and tenses."""
    # Call the make_sentence function with different arguments to create a variety of sentences.
    print(make_sentence(1, "past"))  # Single, Past
    print(make_sentence(1, "present"))  # Single, Present
    print(make_sentence(1, "future"))  # Single, Future
    print(make_sentence(2, "past"))  # Plural, Past
    print(make_sentence(2, "present"))  # Plural, Present
    print(make_sentence(2, "future"))  # Plural, Future

# Call the main function to execute the program
main()
