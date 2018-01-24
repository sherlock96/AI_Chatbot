import aiml
import os
import re
import sys
import google_search
import urllib2
from bs4 import BeautifulSoup
import urllib
import json

kernel = aiml.Kernel()
import database

db = database.DatabaseHandler("localhost","root","root","chatbot")

db.setupDatabase()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
kernel.saveBrain("bot_brain.brn")

#kernel.saveBrain("bot_brain.brn")

# kernel now ready for use

def weather(location):
    #print(location)
    location=urllib.quote(location)
    link="https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"+location+"%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    #print(link)
    linktoparse=urllib2.urlopen(link)
    soup=BeautifulSoup(linktoparse,"html.parser")
    #print(str(soup))
    array=json.loads(str(soup))
    print(array["query"]["results"])
    #result=(array["query"]["results"]["description"])


def google_search(string):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages

    #string="bits pilani"
    string=urllib.quote(string)

    c=0;

    for start in range(0,1):
        url = "http://www.google.com/search?q="+string+"&start=" + str(start*10)
        page = opener.open(url)
        soup = BeautifulSoup(page)
        c=c+1
        if(c==5):
            break

        ### Parse and find
        ### Looks like google contains URLs in <cite> tags.
        ### So for each cite tag on each page (10), print its contents (url)
        for cite in soup.findAll('cite'):
            print(cite.text)    



while True:
    message = raw_input("Enter your message to the bot: ")

    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response = kernel.respond(message)
        db.insertPost(message,bot_response)

        wordList = re.sub("[^\w]", " ",  bot_response).split()
        #print(wordList[1])

        qry=" ".join(wordList)

        
        if(wordList[0]=="weather"):
            weather(qry)
        elif(wordList[0]=="google"):
            print("These are the top search results: \n")
            google_search(qry)
        else: 
            print(bot_response)
        # Do something with bot_response




