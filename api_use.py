
import urllib2
import urllib
from bs4 import BeautifulSoup
import json


location="hyderabad"
location=urllib.quote(location)

#link="http://samples.openweathermap.org/data/2.5/weather?q="+location+",india&appid=b6907d289e10d714a6e88b30761fae22"
link="https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"+location+"%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
#print(link)
linktoparse=urllib2.urlopen(link)
soup=BeautifulSoup(linktoparse,"html.parser")

#print(str(soup))

array=json.loads(str(soup))

print("WIND")
print((str)(array["query"]["results"]["channel"]["wind"]))
print("ATMOSPHERE")
print(array["query"]["results"]["channel"]["atmosphere"])
print("ASTRONOMY")
print(array["query"]["results"]["channel"]["astronomy"])
print("CONDITION")
#print(array["query"]["results"]["channel"]["image"])
print(array["query"]["results"]["channel"]["item"]["condition"])
