# Number guessing game with external package usage
import random
import sys

try:
    from colorama import Fore, Style
except ImportError:
    print("The 'colorama' package is required but not installed.")
    print("Installing 'colorama' package...")
    

# Initialize colorama (required for some platforms)
from colorama import init
init()

number = random.randint(1, 100)
guesses_left = 7

print(Fore.CYAN + "I'm thinking of a number between 1 and 100." + Style.RESET_ALL)

while guesses_left > 0:
    print(Fore.YELLOW + f"You have {guesses_left} guesses left." + Style.RESET_ALL)
    try:
        guess = int(input("Take a guess: "))
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter an integer." + Style.RESET_ALL)
        continue

    if guess < number:
        print(Fore.BLUE + "Too low!" + Style.RESET_ALL)
    elif guess > number:
        print(Fore.BLUE + "Too high!" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"You got it! The answer was {number}" + Style.RESET_ALL)
        break

    guesses_left -= 1

if guesses_left == 0:
    print(Fore.RED + f"You ran out of guesses. The answer was {number}" + Style.RESET_ALL)
