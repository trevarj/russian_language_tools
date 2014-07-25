# -*- coding: UTF-8 -*-

# Generate 5 random words from a CSV file of 10,000 most common Russian words with translations, submit to reddit
# Copyright (C) 2014  Trevor Arjeski

import praw
import csv
import random
import codecs
import time

un = raw_input('username --> ')
pword = raw_input('password --> ')
csvfile_name = "10000_russian.csv"

# pulls 5 words from csv file ( generate random number 0-99, 100-499, 500-1999, 2000-4999, 5000-9999)
def grabWords():
	indexed_csv = []
	final_word_list = []
	num_ranges = [ [0,99],[100,499],[500,1999],[2000,4999],[5000,9999] ]
	csvfile = open(csvfile_name,'rb')
	word_db = csv.reader(csvfile)
	for row in word_db:
		indexed_csv.append(row)

	output_file = open('words.txt','w')
	for x in range(0,4):
		rand = random.randint(num_ranges[x][0], num_ranges[x][1])
		final_word_list.append(indexed_csv[rand])
		output_file.write(final_word_list[x][0] + '\t\t\t' + final_word_list[x][1] + '\n')

	#output_file.write(u'привет')
	output_file.flush()
	output_file.close()
	return final_word_list

def formatPostString(word_list):
	#first element in a word_list element is RU, second is EN

	postString = "**This week's words:**\n\n\n"

	#build the post text
	for x in range(0,4):
		postString += str(word_list[x][0] + " -> " + word_list[x][1] + "\n\n")

	return postString


#connect to reddit
user_agent = ("Russian vocab robot v0.1 by /u/trevorma91")
r = praw.Reddit(user_agent = user_agent)

#login 

r.login(username = un, password = pword)
if r.is_logged_in():
	print "logged in"
else:
	exit()


# generate post
weekly_words = grabWords()
self_post_text = formatPostString(weekly_words)

# submit self post
title = "Weekly Vocabulary Words " + time.strftime("%d/%m/%Y")
r.submit("russian", title, self_post_text)

print "Post successful!"


