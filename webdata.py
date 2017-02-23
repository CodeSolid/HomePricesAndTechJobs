import urllib.parse
import requests 
import socket
import os

class WebData:
	def getDiceCountsForCities(self, locations, keyword):    		
		""" return number of jobs for a given keyword in a given city from dice.com
			locations is a list of city,state tuples, e.g. [('Sacramento', 'CA')]
			keyword is a single keyword word or phrase.  Phrases may be quoted for exact match search (recommended)					
			returns a list with total number of jobs per each keyword, posted in last 7 days
			See http://www.dice.com/common/content/util/apidoc/jobsearch.html for api details
		"""
		# Only return one result because we're interested only in total count, this speeds things up slightly
		base_str = "http://service.dice.com/api/rest/jobsearch/v1/simple.json?text={}&city={}&pgcnt=1&age=7"
		items = []
		for location in locations:    
			place = "{}, {}".format(location[0], location[1])
			quotedKeyword = urllib.parse.quote(self.quoteSpaced(keyword))    
			quotedPlace = urllib.parse.quote(str(place))    
			formatted = base_str.format(quotedKeyword, quotedPlace)        	
			# print(formatted)		
			r = requests.get(formatted)
			count = r.json()['count']    
			items.append(int(count))
		return items


	def getIndeedCountsForCities(self, publisherKey, locations, keyword):    
		""" return number of jobs for a given keyword in a given city from indeed.com
			locations is a list of city,state tuples, e.g. [('Sacramento', 'CA')]
			keyword is a single keyword word or phrase.  
			returns a list with total number of jobs per each keyword, posted in last 7 days
			See http://www.dice.com/common/content/util/apidoc/jobsearch.html for api details
		""" 
				
		base_str = "http://api.indeed.com/ads/apisearch?publisher={}&q={}&l={}%2C+{}&sort=&radius=&st=&jt=&start=&limit=1&fromage=7&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&format=json"
		items = []
		for location in locations:    
			quotedKeyword = urllib.parse.quote(self.quoteSpaced(keyword) )
			quotedCity = urllib.parse.quote(str(location[0]))    

			formatted = base_str.format(publisherKey, quotedKeyword, quotedCity, location[1])        			
		#	print(formatted)
			r = requests.get(formatted)
			count = r.json()['totalResults']    
#			print(r.json())
			items.append(int(count))
		return items
	
	def quoteSpaced(self, input):		
		if ' ' in input:
			return '"{}"'.format(input)
		return input

def testGetDiceCountsForCities(wd):
	keyword = 'java'	
	locations = [('Sacramento', 'CA'), ('Worcester', 'MA'), ('New York', 'NY')]	
	counts = []
	counts = wd.getDiceCountsForCities(locations, keyword)	
	for count in counts:
		print("Count: {}".format(count))

def testGetIndeedCountsForCities(wd):
	publisherKey = os.getenv("INDEED_PUBLISHER")
	keyword = 'java'	
	locations = [('Sacramento', 'CA'), ('Worcester', 'MA'), ('New York', 'NY')]	
	counts = []
	counts = wd.getIndeedCountsForCities(publisherKey, locations, keyword)	
	for count in counts:
		print("Count: {}".format(count))

def main():
	wd = WebData()
	#testGetDiceCountsForCities(wd)
	testGetIndeedCountsForCities(wd)

if __name__ == "__main__": main()