import os
import sys
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from os import listdir
from os.path import isfile, join

from nltk.tokenize.regexp import RegexpTokenizer

from make_story import get_next_words, load_data_from_file

BUTTONS_PER_COL = 8
DATA_PATH = "./data/"
data = None

tokenizer = RegexpTokenizer(r'\w+')
Path(DATA_PATH).mkdir(parents=True, exist_ok=True)


def getTextInput():
    result=text_field.get("1.0","end-1c")
    return result


def update_word_count():
    words = tokenizer.tokenize(getTextInput())
    word_count["text"] = f"{len(words)} Words"


def file_save():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return

    text2save = getTextInput()
    f.write(text2save)
    f.close()


def on_text_button_click(btn):
    text_field.insert(END, btn["text"] + " ")
    fill_text_buttons()


def add_text_button(col_, row_):
    btn = Button(root,text="", width=14, command=lambda: on_text_button_click(btn))
    btn.configure(font=("Courier", 20), bg="black")
    btn.grid(in_=col5, row=row_,column=col_)
    text_buttons.append(btn)


def add_text_coloumn(n):
    for i in range(BUTTONS_PER_COL):
        add_text_button(n, i)


def fill_text_buttons(event=None):
    update_word_count()
    next_words = get_next_words(getTextInput(), data)
    for i in range(len(text_buttons)):
        tupel_nr = i // BUTTONS_PER_COL
        words = next_words[tupel_nr]

        btn_nr = i - tupel_nr * BUTTONS_PER_COL
        
        if btn_nr <= len(words) - 1:
            text_buttons[i]["text"] = words[btn_nr]
        else:
            text_buttons[i]["text"] = ""


def ask_for_files():
    global data
    nr = 1
    names = [""]
    print("------- chose file -------")
    for file in listdir(DATA_PATH):
        if file[-4:].lower() == ".txt":
            names.append(file[:-4])
            print(f"[{nr}] {file}")
            nr += 1
        
    print("--------------------------")

    
    try:
        val = int(input("Enter number: "))
        print(f"Start analysis of {names[val]}:" )
        data = load_data_from_file(names[val])
    except ValueError:
        print("Wrong input, will exit program.")

    pass


if len(sys.argv) == 1:
    ask_for_files()
elif len(sys.argv) == 2:
    name = DATA_PATH + sys.argv[1] + '.txt'
    if os.path.isfile(name):
        data = load_data_from_file(sys.argv[1])
    else:
        print(f"no file found at {name}")
        



root = Tk()
root.title("Story-o-mat")
root.geometry("1100x1000")
root.configure(background='black')
root.attributes("-topmost", True)


title = Label(root, text="Der Lovecraft-o-mat")
title.pack()
title.configure(font=("Courier", 30), bg="black", fg="red", pady=10, width=50)


frame=Frame(root, width=300, height=160)
frame.pack()

text_field = Text(frame, width=52, height=20, padx=19, wrap="word")
text_field.pack()
text_field.configure(font=("Courier", 30))

text_buttons = []





col5 = Frame(root)
col5.pack(side=TOP)

add_text_coloumn(0)
add_text_coloumn(1)
add_text_coloumn(2)
add_text_coloumn(4)
add_text_coloumn(5)

word_count = Label(root, text="0 Words")
word_count.pack()
word_count.configure(font=("Courier", 20), bg="black", fg="red", pady=10, width=50)

save_btn = Button(root,text="save", command=lambda: file_save())
save_btn.pack()

root.bind("<space>", fill_text_buttons)

root.mainloop()
