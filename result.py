#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2
import urllib
import json
import re
import sys

def customPrint(data):
	print str(data)
	sys.stdout.flush()

actor_name = sys.argv[1]

#print("Content-Type: text/html\n\n")  # html markup follows
reload(sys)  
sys.setdefaultencoding('utf8')

html_header = """ 
<html>
<head>
<title>Top 3 Movies</title>
<style>body{background-color: lightgrey;
text-align:center;}
</style>
</head>
<body>"""

customPrint(html_header)

file_actor_list = open("actorList.txt","r")
actor_id = ""
flag = 0

for line_a in file_actor_list:
	if actor_name.lower() in line_a.lower():
                actor_id = line_a[line_a.index(":")+1:len(line_a)-1]
                actor_id = actor_id.strip()
                flag=1
		#print """ <h3>Actor ID: %s</h3>"""%actor_id
		break
file_actor_list.close()		
if(flag==0):
	customPrint(""" <h1 style="text-align:center"> Please Go Back </h1>""")		#done for only limited actors
else:
	no_of_movies = 3
	url = 'http://www.imdb.com/filmosearch?explore=title_type&role='+actor_id+'&ref_=filmo_ref_typ&sort=user_rating,desc&mode=detail&page=1&title_type=movie'
	response = urllib2.urlopen(url)
	html_doc = response.read()
	soup = BeautifulSoup(html_doc, "html5lib")
	#print soup.title.string
	links = soup.findAll('a')
	counter = 0
	for link in links:
		if '?ref_=filmo_li_tt' in link['href']: 
			counter = counter + 1
			#print link.get_text()
			movie_id = link['href'][0:link['href'].find('?')-1]
			#print movie_id
			movie_link = "http://www.imdb.com"+movie_id
			#print movie_link
			if counter == no_of_movies+1:
				break
			#print movie_id
			#Fetching Movie Details
			#print movie_id[7:len(movie_id)]
			ur = 'http://www.omdbapi.com/?i='+movie_id[7:len(movie_id)]+'&plot=full&r=json'
			json_response = urllib2.urlopen(ur)
			json_data = json.load(json_response)
			movie_title = json_data['Title']
			movie_year = json_data['Year']
			movie_rating = json_data['Rated']
			movie_released = json_data['Released']
			movie_runtime = json_data['Runtime']
			movie_genre = json_data['Genre']
			movie_poster = json_data['Poster']
			movie_imdbrating = json_data['imdbRating']
			movie_imdbvotes = json_data['imdbVotes']
			
			customPrint( """<div><img src="%s" alt="no image available" style="float:left" height="130" width="150"/></div>"""%movie_poster)
			customPrint( """ <h2><a href="%s" target="_blank">%s</a></h2>"""%(movie_link,movie_title))
			customPrint( movie_year)
			customPrint( '|')
			customPrint( 'Rating:')
			customPrint( movie_rating)
			customPrint( '|')
			customPrint( movie_released)
			customPrint( '|')
			customPrint( 'Runtime:')
			customPrint( movie_runtime)
			customPrint( '|')
			customPrint( movie_genre)
			customPrint( """<br>""")
			customPrint( 'Ratings:')
			customPrint( """<b>%s/10</b>"""%movie_imdbrating)
			customPrint( 'from')
			customPrint( movie_imdbvotes)
			customPrint( 'users')
			customPrint( """<br> <br>""")
			customPrint( """<b>Top Reviews:<br><br></b>""")

			#Fetching reviews	
			num_of_reviews = 3
			reviewURL = "http://www.imdb.com"+movie_id+"/reviews?filter=best"
			response = urllib2.urlopen(reviewURL)
			html_doc = response.read()
			soup = BeautifulSoup(html_doc, "html.parser")
			division = soup.find('div', id = "tn15content")
			#print division.name
			counter1 = 0
			movie_review = ""
			if division is not None:
				divisions = division.findAll("div")
				for child in divisions:
					if(counter1%2==0):
						movie_review = child.h2.get_text()
						customPrint( """<i style="display:inline">%s</i>"""%movie_review)
						customPrint( """<br>""")
					counter1+=1
					if(counter1==5):
						break
				customPrint("""<hr style="margin-top:1.5em; margin-bottom:1.5em; border-width:1.2px;">""")
customPrint("""</body></html>""")
