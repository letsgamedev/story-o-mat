from data_set import DataSet
from nltk.tokenize.regexp import RegexpTokenizer
import random

tokenizer = RegexpTokenizer(r'\w+')


def load_data_from_file(file_path):
    super_dic = {}

    f = open(file_path, "r")
    lines_count = sum(1 for line in open(file_path))
    print(lines_count)
    current_line_count  = 0
    while True:
        line = f.readline()
        if line == "":
            break

        base_split = line.split("|")
        new_tupel = base_split[0]

        words_data_raw = base_split[1].split(",")
        word_data = []
        for word_set in words_data_raw:
            word = word_set.split(";")
            word_data.append( [word[0], int(word[1])] )
        
        super_dic[new_tupel] = word_data
        
        current_line_count += 1
    
        print(f" {round((current_line_count / lines_count)*100)} % loaded.", end = "\r")

    return super_dic


def get_possible_words(tupel, data):
    word_list = []
    
    sub_tupel = ",".join(tupel)
    if sub_tupel in data:
        words = data[sub_tupel]
        for word in words:
            word_list.append(word)
    
    return word_list


def get_a_random_word(data):
    return ["Tom", 1]
    all_single_words = []
    for d in data:
        if len(d.tupel) == 1:
            all_single_words.append(d.tupel[0])
    
    return random.choice(all_single_words)

def flatten_and_sort_words(words):
    result = []
    sorted_words = sorted(words, key=lambda x: x[1], reverse=True)
    for d in sorted_words:
        result.append(d[0])
    return result


def get_next_words(story, data):
    result = []
    story = story.lower()
    last_x_count = min(len(story), 200)
    words = tokenizer.tokenize(story[-last_x_count:])
    last_x_words = min(len(words), 5)
    for i in range(5 - last_x_words):
        result.append([])
    for i in range(last_x_words, 0, -1):
        possible_word_sets = get_possible_words(words[-i:], data)
        #while len(possible_word_sets) < 5:
        #    possible_word_sets.append(get_a_random_word(data))

        flatten = flatten_and_sort_words(possible_word_sets)
        result.append(flatten)
    
    
    return result


def init():
    data = load_data_from_file("data_kafka_verwandlung")


    story = "da ist"
    for i in range(10):
        story += " " + random.choice(get_next_words(story, data))

    print(story)