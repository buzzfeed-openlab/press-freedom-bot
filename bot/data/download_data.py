import requests
import os

# the doc id of public google doc
DOC_ID = '11K7D2z-mZXzK1Gh2fFeNuz8usNSuwwYUNArvLoK9k4I'

url = "https://docs.google.com/spreadsheets/d/{}/export?format=csv".format(DOC_ID)
r = requests.get(url)
data = r.content

outfile = os.path.dirname(__file__)+'/resources.csv'
with open(outfile, 'wb') as f:
    f.write(data)
