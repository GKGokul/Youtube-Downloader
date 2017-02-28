from bs4 import BeautifulSoup
import urllib2
import itertools
import subprocess
import os
import webbrowser
import string 
import glob
import re
import requests
import cookielib
import tkFileDialog
import json
from selenium import webdriver


def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


print("Enter the song you want to download: ")
textToSearch=raw_input()
query = urllib2.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib2.urlopen(url)
html=response.read()
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

print('Choose the directory for saving the file.')
dir1 = tkFileDialog.askdirectory()  
os.chdir(dir1)

x=int(raw_input("Enter your choice of link to download: "))
os.system('youtube-dl --extract-audio --format m4a --audio-quality 0 ' + urls[x-1])

list_of_files = glob.glob(dir1+'/*') # * means alame(src, dst) to rename or move a file or a directory. Here's a script based on your newest comment. The following code should work. It takes every filename in the current directory, if the filename contains the pattern CHEESE_CHEESE_ then it is renl if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
os.rename(latest_file,titles[x-1]+'.m4a')
latest_file=titles[x-1]+'.m4a'

image_type="ActiOn"
query=titles[x-1]+'album art'
query=query.split()
query='+'.join(query)
url_image="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"

header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url_image,header)

ActualImages=[]# contains the link for Large original images, type of  image
for a,num in itertools.izip(soup.find_all("div",{"class":"rg_meta"}),range(7)):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(dir1) if image_type in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(os.path.join(dir1 , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(dir1 , image_type + "_"+ str(cntr)+"."+Type), 'wb')

        f.write(raw_img)
        f.close()
    except Exception as e:
        print "Could not download the image : "


print("Choose the album art for the downloaded music:")
dir_art=tkFileDialog.askopenfilename()
dir_art=dir_art[len(dir1)+1:]

print(dir_art)
pattern1=r' '
latest_file2=re.sub(pattern1,'\ ',latest_file)
pattern2=r'\('
latest_file3=re.sub(pattern2,'\(',latest_file2)
pattern3=r'\)'
final_file=re.sub(pattern3,'\)',latest_file3)

print(latest_file3)
final_command="mp4art --add "+dir_art+" "+final_file
os.system(final_command)
