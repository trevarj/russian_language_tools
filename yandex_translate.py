# -*- coding: UTF-8 -*-

from lxml import etree
import lxml
import requests
import codecs
import sys

filename = '20000_freq_russian_no_trans_fix.txt'
out_filename = '20000_freq_russian_no_trans_fix2.txt'
API_key = 'YOUR KEY HERE'
lang = 'ru-en'

def generateFile():
	
	in_file = open(filename, 'r')
	out_file = open(out_filename, 'w')
	count = 0

	for row in in_file:
		count += 1
		if count % 1000 == 0: 
			print count
		out_file.write(row.strip() + ', ' + translate(row))


	out_file.flush()
	out_file.close()
	in_file.close()


def translate(word):
	xml_interface = 'https://translate.yandex.net/api/v1.5/tr/translate?key='+ API_key + '&lang='+ lang + '&text=' + word

	result = requests.get(xml_interface)
	tree = etree.XML(result.text.encode('ascii', 'replace'))
	return tree.findtext('text')

	


generateFile()
#translate('башка')