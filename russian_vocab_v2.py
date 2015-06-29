# -*- coding: UTF-8 -*-

# Generate 5 random words from a CSV file of 10,000 most common Russian words with translations, submit to reddit
# Copyright (C) 2014  Trevor Arjeski

import praw
import csv
import random
import codecs
import time


csvfile_name = "20000_freq_final.csv"
words = 25

# Indexes CSV file, generates random numbers and looks up words
def grabWords():
    indexed_csv = []
    final_word_list = []
    rand_set = set()
    csvfile = open(csvfile_name, 'rb')
    word_db = csv.reader(csvfile)

    for row in word_db:
        indexed_csv.append(row)

    output_file = open('words.txt', 'w')
    rand_set.add(-1)
    rand = -1
    for y in range(0, words):
        while rand in rand_set:
            rand = random.randint(0, len(indexed_csv) - 1)
        rand_set.add(rand)
        final_word_list.append(indexed_csv[rand])
        output_file.write(indexed_csv[rand][0] + ' -> ' + indexed_csv[rand][1] + '\n')

    output_file.flush()
    output_file.close()
    return final_word_list


def link_to_word(word):
    return str('[' + word + '](https://slovari.yandex.ru/' + word + ')')


# formats the words for a Reddit post
def formatPostString(word_list):
    # first element in a word_list element is RU, second is EN
    postString = "***This week's words:***\n\n\n"

    # build the post text
    for x in range(len(word_list)):
        postString += str(link_to_word(word_list[x][0]) + " -> " + word_list[x][1] + "\n\n")

    postString += "[all the words](https://github.com/trevorarjeski/russian_tools/blob/master/20000_freq_final.csv)"
    return postString

# check if user only wants to run locally
localOnly = raw_input("do you want to post these words? (y/N)")
if localOnly.lower() != 'y':
    print "saving locally only..."
    grabWords()
    exit()

# connect to reddit
user_agent = ("Russian vocab robot v0.1 by /u/trevorma91")
r = praw.Reddit(user_agent=user_agent)

# login
un = raw_input('username --> ')
pword = raw_input('password --> ')
r.login(username=un, password=pword)
if r.is_logged_in():
    print "logged in"
else:
    print "login failed"
    exit()


# generate post
weekly_words = grabWords()
self_post_text = formatPostString(weekly_words)

# submit self post
title = "Weekly Vocabulary Words " + time.strftime("%d/%m/%Y")
r.submit("organicboys", title, self_post_text)

print "Post successful!"


