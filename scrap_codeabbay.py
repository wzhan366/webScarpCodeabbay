import urllib2
from bs4 import BeautifulSoup
import requests
import pdfkit
import time
import datetime
import json
from xhtml2pdf import pisa             # import python module
from PyPDF2 import PdfFileMerger, PdfFileReader

import logging  # this is one and the class below are used to solve a problem of importing xhtml2pdf
class PisaNullHandler(logging.Handler):
    def emit(self, record):
        pass
logging.getLogger("xhtml2pdf").addHandler(PisaNullHandler())

def get_info_list(url):
'''
parse the problems list from thier prolbems posts
save the problems in a dictionary datastructure
'''
	htmlfile = urllib2.urlopen(url)
	soup = BeautifulSoup(htmlfile, "html.parser")
	table = soup.find('table', {'class':'table table-striped table-bordered table-condensed table-hover full-width centered'})
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
	    	problem_dic[int(cols[0].text)] = [cols[1].text, cols[-1].text, domain+sub_url, update_tags(domain+sub_url)]
	return problem_dic, tags

def check_url_validation(index, url):
'''
this one only uses for test purpose
'''
	conn = urllib2.urlopen(url)
	print index, conn.getcode()

def convert_html_to_pdf(source_html, output_filename):
'''
this one uses pisa method of xhtml2pdf to convert html file to pdf file.
input is the html file path
'''
    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result
    result_file.close()                 # close output file
    return pisa_status.err


def down_file(url,file_name):
'''
use beautifulSoup parse the problem html file
the input is the name of each problem name
also recall convert_html_to_pdf method converts html files to pdf files
'''
	pre = 'html/'
	if file_name == 'Sum "A+B"':
		file_name = 'sum a and b'
	output_filename = pre + file_name + 'need.pdf'
	file_name = pre + file_name + '.html'
	try:
		htmlfile = urllib2.urlopen(url)
		soup = BeautifulSoup(htmlfile, "html.parser") #soup is a html format file
		convert_html_to_pdf(str(soup.body), output_filename)
	except Exception as err:
		print err

def update_tags(url):
'''
go through html files and use the BS4 to parse the tag of each page
return tag list
'''
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

def get_fail_tags(faild_num, problems, tags_dic):
'''
count fial_tags
input fail_num, problems and tags_dic info
output is the fail_tags along with the counted tags dictionary
'''
	f_tags = []
	for i in faild_num:
		for item in problems[str(i)][-1]:
			tags_dic[item] += 1
			f_tags.append(item)
	return set(f_tags), tags_dic

def all_tags_info(tags):
'''
from tag file(collect from each problem) to find the unique tag set
return tag set
'''	
	all_tags = []
	for tag in tags:
		for i in tag:
			all_tags.append(i)
	return set(all_tags)

def getSolvedList():
'''
get the index of sloved problem
the solved problem info is from user page and is copied into a .txt file
output is the index list
'''
    infile = open('solved_list.txt','r')
    d = [d.replace('\n', '') for d in infile.readlines()]
    d = [i.split('\t') for i in d[0::2]]
    solved = []
    for i in d:
        solved.append(i[0])
    return solved

def filenameList(file_name):
'''
generate the file_name for pdf merge purpose
the input file_name is parsed from problem list
the output is the formatted file_name
'''
    if file_name == 'Sum "A+B"':
        file_name = 'sum a and b'
    file_name = file_name+ 'need' + '.pdf'
    return file_name


def mergePdfFiles(filenames):
'''
given the html filenames with extention 
go through all html files to merge them to pdf file
the output is a pdf file
'''
    merger = PdfFileMerger()
    for filename in filenames:
        merger.append(PdfFileReader(file(filename, 'rb')))
    merger.write("document-output.pdf")
   
if __name__ == '__main__':
     faild_num = [114, 74, 116, 51, 56, 125] 
     url = "http://www.codeabbey.com/index/task_list" # the domain name
     problems, tags = get_info_list(url) # from domain name to parse the problem and tag info
     json.dump(problems, open("text.txt",'w')) # transform the problem and tag into JSON format
     json.dump(tags, open("text1.txt",'w'))
     tags = json.load(open("text1.txt"))
     all_tags = all_tags_info(tags)
     tags_dic = {}
     for tag in all_tags: # create tag dictionary for counting purpose
     	tags_dic[tag] = 0
# below this can be conducted sperately from previous
    problems = json.load(open("text.txt")) 
    solved = getSolvedList()
    re = []
    cnt = 0
    for key in solved:  # from the sovled problme index go count and produce html files
        name = problems[key][0]
        url = problems[key][2]
        down_file(url,name)
        re.append(filenameList(name))
    mergePdfFiles(re) # from html filename merge pdf file(the script needs to be placed in the same direction)
	f_tags, tags_dic = get_fail_tags(faild_num, problems, tags_dic)
	total = sum(tags_dic.values())
