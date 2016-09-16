#downloads an IMAGE to the provided path. 
#this fails on .WEBM or other media
def downloadImage(url,path):
    import requests
    from PIL import Image
    img = requests.get(url)
    i = Image.open(StringIO(img.content))
    i.save(path)

#Checks if input folder exists in the current directory. If not, create it.
def checkFolderExists(folder, verbose):
    import os
    if not os.path.exists('./' + folder):
        os.makedirs('./'+folder)
        if verbose:
            print('created folder '+ folder)
    else:
        if verbose:
            print('folder already exists')

#uses re to normalize spaces for generating a folder name.
def normalize_whitespace(str):
	import re
	str = str.strip()
	str = re.sub(r'\s+', ' ', str)
	return str

#given an ugly full name, create a trimmed and formatted shortened folder name.
def createFolderName(webpageTitle):
    splitString = webpageTitle.split('-')
    outputString = splitString[0].strip().upper() + ' - ' + normalize_whitespace(splitString[1]).lower().title()
    return outputString

def validateUrl(url):
    pattern = r'^(https?://)?(www\.)?4chan'
    if( re.match(pattern, url, re.I)):
        return url
    else:
        msg = "URLs must be for a 4chan domain!"
        raise argparse.ArgumentTypeError(msg)

if __name__ == '__main__':
    import argparse
    import re

    parser = argparse.ArgumentParser(description='Process a 4chan thread to scrape all images from.')
    parser.add_argument('url',nargs='+', type=validateUrl, help='a list, separated by spaces, of web addresses to be parsed')
    parser.add_argument('-v', help='verbose. Turn on debug output.', action='store_true', dest='verbose')
    args = parser.parse_args()
    exit(0)

    from BeautifulSoup import BeautifulSoup
    import requests
    from StringIO import StringIO

    for link in args.url:
        if args.verbose:
            print('Processing ' + link)

        response = requests.get(link)
        html = response.content

        soup = BeautifulSoup(html)

        folderName = createFolderName(soup.title.string.replace('/',''))

        checkFolderExists(folderName, args.verbose)
        if args.verbose:
            print('Capturing ' + folderName)
        
        for link in soup.findAll('a', 'fileThumb'):
            imageName = link.get('href')
            if args.verbose:
                print('Getting ' + imageName)
            fileName = re.search('\d+\.\w+$',imageName)
            savePath = './'+ folderName +'/' + fileName.group(0)
            if args.verbose:
                print('saving:' + savePath)
            downloadImage('http:'+imageName,savePath)
