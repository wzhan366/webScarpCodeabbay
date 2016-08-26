import urllib2
from bs4 import BeautifulSoup
import requests

import time 
import datetime

import json

def get_info_list(url):
# parse the problems list
	htmlfile = urllib2.urlopen(url)
	soup = BeautifulSoup(htmlfile, "html.parser")
	table = soup.find('table', {'class':'table table-striped table-bordered table-condensed table-hover full-width centered'})
	# table_body = table.find('tbody')
	problem_dic = {}
	tags = []
	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    if cols:
	    	print 'page', cols[0].text
	    	domain = 'http://www.codeabbey.com/'
	    	sub_url = cols[1].find('a').get('href')
	    	tags.append(update_tags(domain+sub_url))
	    	# print cols[0].text,cols[1].href ,cols[1].text,cols[-1].text
	    	problem_dic[int(cols[0].text)] = [cols[1].text, cols[-1].text, domain+sub_url, update_tags(domain+sub_url)]
	return problem_dic, tags

def check_url_validation(index, url):
# to check if the url link is valid
	conn = urllib2.urlopen(url)
	print index, conn.getcode()

def download_file(url):
	response = urllib2.urlopen(url)
	print response
	file = open('problem1.pdf','w')
	file.write(response.read())
	file.close()
	print("Completed")

def down_file(url):
	pdfkit.from_url(url, 'out.pdf')

def update_tags(url):
# parse tags from problem page
	htmlfile = urllib2.urlopen(url)
	soup = BeautifulSoup(htmlfile, "html.parser")
	t = []
	try:
		tags = soup.find_all('a', {'class':'tag'})
		for tag in tags:
			t.append(tag.text)
		return t
	except:
		return []

def get_fail_tags(l, a, tags_dic):
	f_tags = []
	for i in l:
		for item in a[str(i)][-1]:
			tags_dic[item] += 1
			f_tags.append(item)
	return set(f_tags), tags_dic

def all_tags_info(tags):
	all_tags = []
	for tag in tags:
		for i in tag:
			all_tags.append(i)
	return set(all_tags)

if __name__ == '__main__':
	faild_num = [114, 74, 116, 51, 56, 125]
	# url = "http://www.codeabbey.com/index/task_list"
	# problems, tags = get_info_list(url)
	# json.dump(problems, open("text.txt",'w'))
	# json.dump(tags, open("text1.txt",'w'))
	tags = json.load(open("text1.txt"))
	all_tags = all_tags_info(tags)
	# print all_tags, len(all_tags)
	tags_dic = {}
	for tag in all_tags:
		tags_dic[tag] = 0

	print all_tags, len(all_tags)
	problems = json.load(open("text.txt"))
	f_tags, tags_dic = get_fail_tags(faild_num, problems, tags_dic)
	# print f_tags

	# print tags_dic

	total = sum(tags_dic.values())
	for k, v in tags_dic.items():
		if v != 0:
			print k, v

	

	# get_fail_tags(faild_num, problems)
	# url = 'http://www.codeabbey.com/index/task_view/connect-four'
	# update_tags(url)
	# down_file(url)

