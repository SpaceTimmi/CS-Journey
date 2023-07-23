# Problem Set 2, hangman.py
# Name: SpaceTimmi
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    if len(secret_word) == 1:
        return secret_word in letters_guessed
    else:
        return (secret_word[0] in letters_guessed) and is_word_guessed(secret_word[1::], letters_guessed)



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    secret_letters = list(secret_word)
    res = list(map(lambda char: "_" if char not in letters_guessed else char, secret_letters))
    return "".join(res)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    all_letters = list(string.ascii_lowercase)
    for index, char in enumerate(string.ascii_lowercase):
        if char in letters_guessed:
            all_letters[index] = ''
    return "".join(all_letters)



def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses, warnings = 6, 3
    letters_guessed = []
    vowels = ['a','e','i','o','u',]

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings} warnings left.")

    while guesses > 0:
        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            total_score = guesses * len(list(set(secret_word)))
            print("Congratulations! You've won!")
            print(f"Your total score for this game is: {total_score}")
            break

        print(f"You have {guesses} guesses left.")
        print(f"Avaialable letters: {get_available_letters(letters_guessed)}")
        guess = input("Please guess a letter: ")

        if (not str.isalpha(guess)) or (str.lower(guess) in letters_guessed):
            # If 'guess' is not an alphabet or 'guess' has already been guessed
            if warnings > 0: warnings -= 1
            if warnings <= 0: guesses -= 1

            guessed_word = get_guessed_word(secret_word, letters_guessed)
            warnings_str = f"You now have {warnings} warnings left"
            if str.lower(guess) in letters_guessed:
                print(f"Opps! You've already guessed that letter. {warnings_str}: {guessed_word}  ")
            else:
                print(f"Opps! That is not a valid letter. {warnings_str}: {guessed_word}")
        else:
            # If 'guess' is an alphabet not previously guessed
            guess = str.lower(guess)
            letters_guessed.append(guess)
            guessed_word = get_guessed_word(secret_word, letters_guessed)

            if guess in secret_word:
                print(f"Good guess: {guessed_word}")
                continue

            if guess in vowels: guesses -= 2
            if guess not in vowels: guesses -= 1
            print(f"Oops! That letter is not in my word: {guessed_word}")

    # Player fails to guess the word.
    if guesses == 0: print(f"Sorry you ran out of guesses. The word was {secret_word}.")



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    x, y = my_word.strip(), other_word.strip()
    if len(x) != len(y): return False

    my_word, other_word = list(x), list(y)
    my_word_unique = list(set(my_word[::]))
    my_word_unique.remove('_')
    for char in my_word_unique:
        if my_word.count(char) != other_word.count(char): return False
    for index, char in enumerate(other_word):
        if (my_word[index] != '_') and (my_word[index] != char): return False
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matches = list()
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word): matches.append(other_word)

    if len(matches) < 1:
        print("No matches found")
    else:
        print(" ".join(matches))


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guesses, warnings = 6, 3
    letters_guessed = []
    vowels = ['a','e','i','o','u',]

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings} warnings left.")

    while guesses > 0:
        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            total_score = guesses * len(list(set(secret_word)))
            print("Congratulations! You've won!")
            print(f"Your total score for this game is: {total_score}")
            break

        print(f"You have {guesses} guesses left.")
        print(f"Avaialable letters: {get_available_letters(letters_guessed)}")
        guess = input("Please guess a letter: ")


        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if guess == "*":
            print("Possible word matches are:")
            show_possible_matches(guessed_word)
        elif (not str.isalpha(guess)) or (str.lower(guess) in letters_guessed):
            # If 'guess' is not an alphabet or 'guess' has already been guessed
            if warnings > 0: warnings -= 1
            if warnings <= 0: guesses -= 1

            warnings_str = f"You now have {warnings} warnings left"
            if str.lower(guess) in letters_guessed:
                print(f"Opps! You've already guessed that letter. {warnings_str}: {guessed_word}  ")
            else:
                print(f"Opps! That is not a valid letter. {warnings_str}: {guessed_word}")
        else:
            # If 'guess' is an alphabet not previously guessed
            guess = str.lower(guess)
            letters_guessed.append(guess)
            guessed_word = get_guessed_word(secret_word, letters_guessed)

            if guess in secret_word:
                print(f"Good guess: {guessed_word}")
                continue

            if guess in vowels: guesses -= 2
            if guess not in vowels: guesses -= 1
            print(f"Oops! That letter is not in my word: {guessed_word}")

    # Player fails to guess the word.
    if guesses == 0: print(f"Sorry you ran out of guesses. The word was {secret_word}.")




# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
