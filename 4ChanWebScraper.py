import requests
import os
import sys
import re
from BeautifulSoup import BeautifulSoup
from PIL import Image
from StringIO import StringIO

# try:                                
#     opts, args = getopt.getopt(argv, "u:", ["url="]) 
# except getopt.GetoptError:           
#     print('usage: python 4ChanWebScraper.py -u=<url>')                         
#     sys.exit(2)  

url = sys.argv[1]
print('Attempting to capture ' + url)
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

folderName = soup.title.string.replace('/','')

print('Capturing ' + folderName)

if not os.path.exists('./' + folderName):
    os.makedirs('./'+folderName)
    print('created folder '+ folderName)
else:
    print('folder already exists')

for link in soup.findAll('a', 'fileThumb'):
    imageName = link.get('href')
    print('Getting ' + imageName)
    fileName = re.search('\d+\.\w+$',imageName)
    savePath = './'+ folderName +'/' + fileName.group(0)
    print('saving:' + savePath)
    img = requests.get('http:' + imageName)
    i = Image.open(StringIO(img.content))
    i.save(savePath)


# for thumb in table.findAll('fileThumb'):
#     print row.text