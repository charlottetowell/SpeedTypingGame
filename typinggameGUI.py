import random as rand
import PySimpleGUI as sg
from wonderwords import RandomWord
import pandas as pd

sg.theme("DarkBlue6")
r = RandomWord()

difficulty_factors = {'Easy': 400,
                        'Normal': 200,
                        'Hard': 50}

highscores = pd.read_csv("highscores.txt", sep="|")

def starting_screen():
    global difficulty
        #define window layout
    layout = [ [sg.Text("Speed Typing Game", justification = "center")],
            [sg.Text("Choose difficulty to start")],
            [sg.Button('Easy'), sg.Button('Normal'), sg.Button('Hard')],
            [sg.Button('View High Scores'), sg.Button('Quit')] ]
    window = sg.Window('Typing Game', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
                break
        elif event in ('Easy', 'Normal', 'Hard'):
            window.close()
            difficulty = event
            gameplay()
            break
        elif event == 'View High Scores':
            view_high_scores()
        elif event == 'Quit':
            window.close()
            break

    window.close()

def gameplay():
    global level

    running = True
    level = 1
    
    #define level layout
    layout = [ [sg.Text(f"LEVEL {level}", key = "level_counter")],
            [sg.Text("", key="string_to_type")],
            [sg.Input("",     key='Input1')],
        #    [sg.Text("", key="stopwatch")],
            [sg.ProgressBar(100, orientation='h',size=(24.5,20), key='countdown')]
            ]
    window = sg.Window('Typing Game', layout, finalize=True)
    window['Input1'].bind("<Return>", "_Enter") #set enter key to be submit


    while running:
        #gameplay

        #generate string to type for level
        if level < 15:
            word_min_length = max(3, level - 3)
            word_max_length = max(3, level)
            string_to_type = r.word(word_min_length=word_min_length, word_max_length=word_max_length)
        else:
            words_to_generate = max(3, level-15)
            words_to_generate = words_to_generate - rand.randint(1, words_to_generate-1)
            string_to_type = " ".join(r.random_words(words_to_generate)).lower()

        #ms allocated to type word in
        time_allowed = len(string_to_type)*100*(1/ max(level, level-3) ) + difficulty_factors[difficulty]

        window['Input1'].bind("<Return>", "_Enter") #set enter key to be submit
        window["level_counter"].update(f"LEVEL {level}")
        window["string_to_type"].update(f"Type the following characters:\n{string_to_type}")
        window['Input1'].update("")

        counter = 0
        while True:
            event, values = window.read(timeout=10)

            #timer
            time_left = time_allowed - counter
            percent = round((time_left / time_allowed) * 100)
            window['countdown'].update(percent)
        #    window['stopwatch'].update('{:02f}:{:02f}.{:02f}'.format((time_left // 100) // 60, (time_left // 100) % 60, time_left % 100))
            counter += 1
        
            if event == sg.WINDOW_CLOSED:
                break
            elif time_left <= 0:
                running = False
                break

            elif event == "Input1" + "_Enter":
                attempt = values["Input1"].lower()

                if attempt != string_to_type:
                    running = False
                    break
                else:
                    level +=1
                break
    window.close()
    game_over()

def game_over():
    global level

    layout = [ [sg.Text("GAME OVER")],
    [sg.Text(f"You reached level {level}")],
    [sg.Button('Quit'), sg.Button('Save Score'), sg.Button('Play Again')]
    ]
    window = sg.Window('Game Over', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Quit":
            break
        elif event == "Play Again":
            window.close()
            starting_screen()
            break
        elif event == 'Save Score':
            save_score()
    window.close()

def save_score():
    global level
    global difficulty
    global highscores

    layout= [
        [sg.Text(f"You reached level {level} at {difficulty} difficulty")],
        [sg.Text("Enter Name: "), sg.Input("", key='name')],
        [sg.Button("Save Score"), sg.Button("Cancel")]
    ]
    window = sg.Window('Save Score', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Save Score':
            highscores.loc[-1] = [values['name'], difficulty, level]
            highscores = highscores.groupby(["Name","Difficulty"], as_index=False).max()
            window.close()
            break
        elif event == 'Cancel':
            break;
    window.close()

def view_high_scores():
    #convert df to list
    headings = ['Name', 'Level']

    easy_scores = highscores[highscores['Difficulty']=="Easy"]
    easy_scores = easy_scores[['Name', 'Level']].sort_values(by='Level', ascending = False)
    easy_values = easy_scores.values.tolist()

    normal_scores = highscores[highscores['Difficulty']=="Normal"]
    normal_scores = normal_scores[['Name', 'Level']].sort_values(by='Level', ascending = False)
    normal_values = normal_scores.values.tolist()

    high_scores = highscores[highscores['Difficulty']=="Hard"]
    high_scores = high_scores[['Name', 'Level']].sort_values(by='Level', ascending = False)
    hard_values = high_scores.values.tolist()


    layout_tab1 = [[sg.Table(values = easy_values, headings = headings,
        auto_size_columns=True,
        col_widths=list(map(lambda x:len(x)+1, headings)))]
        ]
    layout_tab2 = [[sg.Table(values = normal_values, headings = headings,
        auto_size_columns=True,
        col_widths=list(map(lambda x:len(x)+1, headings)))]
        ]
    layout_tab3 = [[sg.Table(values = hard_values, headings = headings,
        auto_size_columns=True,
        col_widths=list(map(lambda x:len(x)+1, headings)))]
        ]

    layout = [[sg.TabGroup([[
            sg.Tab('Easy', layout_tab1),
            sg.Tab('Normal', layout_tab2),
            sg.Tab('Hard', layout_tab3)
            ]], tab_location='centertop'),
   sg.Button("Close")]]

    window = sg.Window('High Scores', layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Close':
            window.close()
            break

#start game
starting_screen()
#save highscores
highscores.to_csv(r'highscores.txt', header=True, index=None, sep='|', mode='w')

    

    
