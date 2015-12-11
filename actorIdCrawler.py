from bs4 import BeautifulSoup
import urllib2
import re



actor_id = 1

file_a = open("actorList.txt", 'w')
for actor_id in range(1, 1000):
	url = 'http://www.imdb.com/name/nm'+str(actor_id)
	response = urllib2.urlopen(url)
	html_doc = response.read()
	soup = BeautifulSoup(html_doc, 'html.parser')
	print soup.title.string
	actor_name = soup.title.string
	actor_name = actor_name[0:actor_name.find("-")-1]
	file_a.write(actor_name.encode("UTF-8"))
	line=":nm"
	digits = len(str(actor_id))
	numZeroes = 7 - digits
	for i in range(0,numZeroes):
		line = line+'0'
	line = line+str(actor_id)+"\n"
	file_a.write(line)

file_a.close()	