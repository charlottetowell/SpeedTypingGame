
import random as rand
import string
from timeit import default_timer
import os
import PySimpleGUI as sg

def starboxtext(text, blank_lines = 1):
    n = len(text) + 4
    stars = "*"*n
    space = "\n"*blank_lines
    print(f"{space}{stars}\n* {text} *\n{stars}{space}")


#welcome
starboxtext("Welcome to the Typing Game")

#start game on key press
input('Press enter to start!')
    

running = True
level = 1
start = default_timer()

while running:
    #gameplay
    
    #clear screen
    os.system('cls')

    starboxtext(f"LEVEL {level}")
    string_to_type = ""
    for i in range(level):
        string_to_type += rand.choice(string.ascii_letters[:26])

    attempt = input(f"Type the following characters:\n{string_to_type}\n > ")

    if attempt != string_to_type:
        duration = default_timer() - start
        starboxtext("GAME OVER")
        print(f"You reached level {level} in {duration} ms")
        running = False
    else:
        level +=1
    
    

    





