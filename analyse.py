import os.path
import sys
import time
from os import listdir
from os.path import isfile, join
from pathlib import Path

from nltk.tokenize.regexp import RegexpTokenizer

BOOK_PATH = "./books/"
MAX_LAYER_DEEP = 5

Path("./data/").mkdir(parents=True, exist_ok=True)


def parse_file(file_name):
    start_time = time.time()

    super_dic = {}

    text = open(BOOK_PATH + file_name + '.txt', 'rb').read().decode(encoding='utf-8')
    text = text.lower()

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)

    print(f"{len(words)} Words. {len(text)} characters.")

    for i in range(MAX_LAYER_DEEP + 1):
        words.insert(0, "$$%$")

    word_count = len(words)

    for j in range(word_count - MAX_LAYER_DEEP):
        new_set = words[j:j+MAX_LAYER_DEEP]
        next_word = words[j+MAX_LAYER_DEEP]

        for i in range(1, MAX_LAYER_DEEP + 1, 1):
            sub_set = new_set[-i:]

            if sub_set[0] == "$$%$":
                continue

            sub_tuple = ",".join(sub_set)
            
            # Creates a new dict for key 'sub_tuple' if it does not exist and return it
            words_set = super_dic.setdefault(sub_tuple, dict())
            
            # Set value to 0 if no word hasn't been added yet
            words_set.setdefault(next_word, 0)

            words_set[next_word] += 1
        
        set_progress(j, word_count, start_time)

    make_small_statistics(1, start_time)
    
    with open(f"data/data_{file_name}.txt", "w", encoding="utf-8") as f:
        for key in super_dic:
            words_string = []
            for word_key, word_value in super_dic[key].items():
                words_string.append(f"{word_key};{word_value}")

            f.write(key + "|" + ",".join(words_string) + "\n")
    
    end = time.time()
    print(f"\nAnalysis done in {time.strftime('%H:%M:%S', time.gmtime(end - start_time))}.")



def replace_line(txt):
    sys.stdout.write("\r%s" % txt)
    sys.stdout.flush()


def make_small_statistics(progress, start_time):
    end = time.time()
    times = time.strftime('%H:%M:%S', time.gmtime(end - start_time))
    replace_line(f"{MAX_LAYER_DEEP} Tupels | {round(progress * 100)}% ({times})")


progress = 0

def set_progress(nr, sum, start_time):
    global progress
    new_progress = round(nr / sum, 2)
    if new_progress > progress:
        progress = new_progress
        make_small_statistics(progress, start_time)


def ask_for_files():
    nr = 1
    names = [""]
    print("------- choose file -------")
    for file in listdir(BOOK_PATH):
        if file[-4:].lower() == ".txt":
            names.append(file[:-4])
            print(f"[{nr}] {file}")
            nr += 1
        
    print("--------------------------")

    try:
        val = int(input("Enter number: "))
    except ValueError:
        print("\nInvalid selection!")
        return
    if val < 1 or val >= len(names):
        print("\nInvalid selection!")
        return
    try:
        print(f"Start analysis of {names[val]}:" )
        parse_file(names[val])
    except Exception as e:
        print(f"\nException: {e}")

if len(sys.argv) == 1:
    ask_for_files()
elif len(sys.argv) == 2:
    name = BOOK_PATH + sys.argv[1] + '.txt'
    if os.path.isfile(name):
        parse_file(sys.argv[1])
    else:
        print(f"no file found at {name}")
