import sys # Used to add the BeautifulSoup folder the import path
import urllib2 # Used to read the html document
import urllib
import json
from bs4 import BeautifulSoup

if __name__ == "__main__":
  
    #from BeautifulSoup import BeautifulSoup

    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages

    string="=5+5"
    string=urllib.quote(string)

    c=0;

    for start in range(0,1):
        url = "http://www.google.com/search?q="+string+"&start=" + str(start*10)
        page = opener.open(url)
        soup = BeautifulSoup(page)

        ### Parse and find
        ### Looks like google contains URLs in <cite> tags.
        ### So for each cite tag on each page (10), print its contents (url)
        for cite in soup.findAll('cite'):
            print cite.text    

    