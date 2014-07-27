# -*- coding: UTF-8 -*-

# Generate 5 random words from a CSV file of 10,000 most common Russian words with translations, submit to reddit
# Copyright (C) 2014  Trevor Arjeski

import praw
import csv
import random
import codecs
import time


csvfile_name 		= "10000_russian.csv"
#				 		beg		   int          adv
difficulty			= [[0,499, "**BEGINNER**"], [500,4999, "**INTERMEDIATE**"], [5000,9207, "**ADVANCED**"]]
words_per_diff		= 8

# Indexes CSV file, generates random numbers within difficult ranges and builts a list of n
# words where n is words_per_diff
def grabWords():
	indexed_csv = []
	final_word_list = []
	num_ranges = [ [0,99],[100,499],[500,1999],[2000,4999],[5000,9999] ]
	csvfile = open(csvfile_name,'rb')
	word_db = csv.reader(csvfile)
	for row in word_db:
		indexed_csv.append(row)

	output_file = open('words.txt','w')

	for x in range(len(difficulty)):
		output_file.write(difficulty[x][2] + '\n')
		for y in range(0,words_per_diff):
			rand = random.randint(difficulty[x][0], difficulty[x][1])
			final_word_list.append(indexed_csv[rand])
			output_file.write(indexed_csv[rand][0] + ' -> ' + indexed_csv[rand][1] + '\n')

	output_file.flush()
	output_file.close()
	return final_word_list

# formats the words for a Reddit post
def formatPostString(word_list):
	#first element in a word_list element is RU, second is EN
	postString = "***This week's words:***\n\n\n"

	#build the post text
	for x in range(len(word_list)):
		if x % words_per_diff == 0:
			postString += difficulty[(x+1)/words_per_diff][2] + '\n\n'
		postString += str(word_list[x][0] + " -> " + word_list[x][1] + "\n\n")

	return postString

# check if user only wants to run locally
localOnly = raw_input("do you want to post these words? (y/N)")
if localOnly.lower() != 'y':
	print "saving locally only..."
	grabWords()
	exit()

#connect to reddit
user_agent = ("Russian vocab robot v0.1 by /u/trevorma91")
r = praw.Reddit(user_agent = user_agent)

#login 
un = raw_input('username --> ')
pword = raw_input('password --> ')
r.login(username = un, password = pword)
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
r.submit("russian", title, self_post_text)

print "Post successful!"


