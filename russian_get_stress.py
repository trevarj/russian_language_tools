# -*- coding: UTF-8 -*-

from lxml import etree
import lxml
import requests
import csv
import codecs
import sys

# This script is going to scrape Slovari.Yandex.com for stressed
# letters for a given word


def inputFromCSV(csvfile_name):
	indexed_csv 	= []
	csvfile 		= open(csvfile_name,'rb')
	output_file 	= open(csvfile_name[:-4] + '_stress.csv' ,'w')
	word_db 		= csv.reader(csvfile)
	cwriter			= csv.writer(output_file)
	counter 		= 0

	sys.stdout.write('Starting... ')
	for row in word_db:
		# index 0 is russian word
		row[0] = getStress(row[0].split(' ', 1)[0])
		cwriter.writerow(row)
		counter += 1
		if counter % 500 == 0:
			sys.stdout.write('.')
			counter = 0
	
	output_file.close()
	csvfile.close()
	

def singleLookup(word):
	output = open('temp.txt', 'w')
	stressed = getStress(word)
	output.write(stressed)
	output.flush()
	output.close()
	
diacritics = {'а':'а́', 'е':'е́', 'и':'и́', 'о':'о́', 'у':'у́', 'ы':'ы́', 'э':'э́', 'ю':'ю́', 'я':'я́', 'А':'А́', 'Е':'Е́', 'И':'И́', 'О':'О́', 'У':'У́', 'Ы':'Ы́', 'Э':'Э́', 'Ю':'Ю́', 'Я':'Я́',}
def formatVowel(vowel):
	# look up against a table with the tick marks
	return diacritics[vowel]

def getStress(word):
	url = 'http://slovari.yandex.ru/'+word+'/ru-en'
	page = requests.get(url)
	
	tree = etree.HTML(page.text)
	stressed = ''
	translation = tree.xpath('//span[@class="b-translation__text"]/span[@class="b-translation__ac"]/../node()')

	# Logic -- see this http://lxml.de/api/index.html for data type defs
	#
	# loop through translation list
 	# check for type 'lxml.etree._Element' -- means that it's the span with stress
	# if Element is found then format it to be a stressed letter
	# Build the string along the way
	if not translation:
		return word
	else:
		for i in translation:
			if type(i) is lxml.etree._Element:
				stressed += formatVowel(i.text.encode('utf-8'))
			else:
				stressed += i.encode('utf-8')
	
	#fuck unicode and everything about dealing with it in python
	return stressed


#singleLookup('здравствуйте')

inputFromCSV("10000_russian.csv")