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

message=""

db = database.DatabaseHandler("localhost","root","root","chatbot")

#db.setupDatabase()

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
kernel.saveBrain("bot_brain.brn")

#kernel.saveBrain("bot_brain.brn")

# kernel now ready for use


def weather(location):
    #print(location)
    global chat_log
    location=urllib.quote(location)
    link="https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"+location+"%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    #print(link)
    linktoparse=urllib2.urlopen(link)
    soup=BeautifulSoup(linktoparse,"html.parser")
    #print(str(soup))
    array=json.loads(str(soup))

    #print(array["query"]["results"])
    print("WIND")
    print(array["query"]["results"]["channel"]["wind"])
    print("ATMOSPHERE")
    print(array["query"]["results"]["channel"]["atmosphere"])
    print("ASTRONOMY")
    print(array["query"]["results"]["channel"]["astronomy"])
    print("CONDITION")
    #print(array["query"]["results"]["channel"]["image"])
    print(array["query"]["results"]["channel"]["item"]["condition"])
    weath=str(array["query"]["results"]["channel"]["item"]["condition"])
    chat_log+=weath
    chat_log+="\n"
    #db.insertPost(message,array["query"]["results"]["channel"]["item"]["condition"])


def google_search(string):
    global chat_log
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
        c=0;
        for cite in soup.findAll('cite'):
            if(c==0):
                db.insertPost(message,cite.text)
                chat_log+=cite.text
                chat_log+="\n"
            print(cite.text) 
            c=c+1



chat_log=""

while True:
    message = raw_input("Enter your message to the bot: ")

    if message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    elif message == "log":
        print(chat_log)
    else:
        bot_response = kernel.respond(message)
        #db.insertPost(message,bot_response)

        wordList = re.sub("[^\w]", " ",  bot_response).split()
        #print(wordList[1])

        qry=" ".join(wordList)

        chat_log+="User: "
        chat_log+=message
        chat_log+="\n"
        chat_log+="Bot: "
        

        
        if(wordList[0]=="weather"):
            weather(qry)
        elif(wordList[0]=="google"):
            print("These are the top search results: \n")
            google_search(qry)
        else: 
            print(bot_response)
            chat_log+=bot_response
            chat_log+="\n"
            #db.insertPost(message,bot_response)
        # Do something with bot_response




