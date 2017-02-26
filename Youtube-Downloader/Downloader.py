from bs4 import BeautifulSoup
import urllib2
import itertools
import subprocess
import os

print("Enter the song you want to download: ")
textToSearch=raw_input()

query = urllib2.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib2.urlopen(url)
html=response.read()
response.close

soup=BeautifulSoup(html,"lxml")
allurls = soup.find_all("a")

titles = []
urls = []
for vid,i in itertools.izip(soup.findAll(attrs={'class':'yt-uix-tile-link'}),range(10)):
	titles.append(vid['title'])
	urls.append('https://www.youtube.com' + vid['href'])
print("\t\t\t\tSEARCH RESULTS:")
for utitle,url2,i in itertools.izip(titles,urls,range(10)):
	print(str(i+1)+'. ' + utitle)
print('')

x=int(raw_input("Enter your choice of link to download: "))

os.system('youtube-dl --extract-audio --format m4a ' + urls[x-1])



