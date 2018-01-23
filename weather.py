
#weather api


"""import requests
r = requests.get('http://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b6907d289e10d714a6e88b30761fae22')
r.json()

print(r)
"""

import requests, json
url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
payload = open("request.json")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=payload, headers=headers)



#for i in r:
#	print(r)