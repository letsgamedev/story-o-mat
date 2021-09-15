from make_story import get_next_words, load_data_from_file
from tkinter import *
from nltk.tokenize.regexp import RegexpTokenizer
from tkinter import filedialog

BUTTONS_PER_COL = 8

tokenizer = RegexpTokenizer(r'\w+')

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
    btn = Button(root,text="empty lalala hoch sicher", width=14, command=lambda: on_text_button_click(btn))
    #btn.pack(in_=col, side=BOTTOM)
    btn.configure(font=("Courier", 20), bg="black")
    btn.grid(in_=col5, row=row_,column=col_)
    text_buttons.append(btn)


def add_text_coloumn(n):
    for i in range(BUTTONS_PER_COL):
        add_text_button(n, i)


def fill_text_buttons(event=None):
    update_word_count()
    next_words = get_next_words(getTextInput(), data)
    #print(next_words, len(text_buttons))
    for i in range(len(text_buttons)):
        tupel_nr = i // BUTTONS_PER_COL
        words = next_words[tupel_nr]

        btn_nr = i - tupel_nr * BUTTONS_PER_COL
        
        if btn_nr <= len(words) - 1:
            text_buttons[i]["text"] = words[btn_nr]
        else:
            text_buttons[i]["text"] = ""



file_name = "data_lite"
data = load_data_from_file("data/" + file_name + ".txt")

root = Tk()
root.title = "Penis"
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