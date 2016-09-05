'''this one is an example of scarp stock info from yahoo finance'''


from threading import Thread
import urllib
import re
symbolfile = open("symbols.txt",'r')
symbolslist = symbolfile.read().split('\n')


def th(ur):
	base = 'https://ca.finance.yahoo.com/q?s=' 
	url = base + ur
	regex = '<span id="yfs_l84_'+ ur.lower() +'">(.+?)</span>'
	pattern = re.compile(regex)
	htmltext = urllib.urlopen(url).read()
	results = re.findall(pattern, htmltext)
	print ur, results

urls = ["http://www.businessinsider.com/", 
		"http://nytimes.com",
		"http://www.yahoo.com",
		"http://cnn.com"]
threadlist = []


for u in symbolslist:
	t = Thread(target=th, args=(u,))
	t.start()
	threadlist.append(t)

for b in threadlist:
	b.join()
