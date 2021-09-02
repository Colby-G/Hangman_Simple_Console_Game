import datetime
import requests
from bs4 import BeautifulSoup


def get_info():
    info_list = []
    example_list = []
    fact_list = []
    date = str(datetime.date.today())
    url = "https://www.merriam-webster.com/word-of-the-day/thesaurus-" + date
    website_call = requests.get(url)
    html_get = website_call.text
    html_form = BeautifulSoup(html_get, "html.parser")
    word = html_form.h1.get_text()
    for info_text in html_form.find_all("p"):
        info_list.append(info_text.get_text())
    definition = info_list[0]
    for examples in info_list:
        if examples.startswith("//"):
            sentence = examples.replace("// ", "")
            example_list.append(sentence)
    example = ', '.join(map(str, example_list))
    for fact_text in html_form.find_all("div", class_="did-you-know-wrapper"):
        fact_list.append(fact_text.get_text())
    fact_name = ' '.join(map(str, fact_list))
    fact_names = fact_name.splitlines()
    fact = fact_names[2]
    return word.upper(), definition, example, fact


def play(info):
    word = info[0]
    definition = str(info[1])
    example = str(info[2])
    fact = str(info[3])
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    print("Let's play Hangman: Word of the Day Edition!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")
    while not guessed and tries > 0:
        guess = input("Please guess a letter or the word of the day: ").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word of the day.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word of the day!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word of the day.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Not a valid guess.")
        print(display_hangman(tries))
        print(word_completion)
        print("\n")
    if guessed:
        print("Congrats, you guessed the word of the day (" + word + ")! You win!")
    else:
        print("Sorry, you ran out of tries. The word of the day was " + word + ". Better luck next time!")
    print("The definition of " + word + " is: " + definition)
    print("An example of " + word + " is: " + example)
    print("Did you know? Here is a fun fact about " + word + ": " + fact)


def display_hangman(tries):
    stages = [
                """
                   ________
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                 _____
                """,
                """
                   ________
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                 _____
                """,
                """
                   ________
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                 _____
                """,
                """
                   ________
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                 _____
                """,
                """
                   ________
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                 _____
                """,
                """
                   ________
                   |      |
                   |      O
                   |    
                   |      
                   |     
                 _____
                """,
                """
                   ________
                   |      |
                   |      
                   |    
                   |      
                   |     
                 _____
                """
    ]
    return stages[tries]


def main():
    info = get_info()
    play(info)


if __name__ == "__main__":
    main()
