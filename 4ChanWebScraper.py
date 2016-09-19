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
    pattern = r'^(https?://)?(www\.)?(boards\.)?4chan\.'
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
    parser.add_argument('-ns', help='No saving. This disables actually modifying the filesystem.', action='store_false', dest='save')
    args = parser.parse_args()

    from BeautifulSoup import BeautifulSoup
    import requests
    from StringIO import StringIO
    import os

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
        
        for link in soup.findAll('div','fileText'): 
            imageName = link.a.get('href')
            if args.verbose:
                print('Processing ' + imageName)
            title = link.a.get('title')
            #save the title as the filename
            if title is not None:
                savePath = './'+folderName+'/'+title
                if args.verbose:
                    print('Title is found. Using it as filename; ' + title)
                if not os.path.isfile(savePath):
                    if args.verbose:
                        print('Saving from http:' + imageName)
                        print('No previous file exists. Saving to ' + savePath)
                        print('Saving files: ' + str(args.nosave) )
                    if args.save:
                        downloadImage('http:'+imageName,savePath)
                else:
                    print('File exists. Skipping it.')

            #save the filename as the filename 
            else:
                fileName = re.search('\d+\.\w+$',imageName).group(0)
                if args.verbose:
                    print('Title not found. Using filepath as filename;  ' + fileName)
                savePath = './'+ folderName +'/' + fileName
                if args.verbose:
                    print('saving:' + savePath)
                if not os.path.isfile(savePath):
                    if args.save:
                        downloadImage('http:'+imageName,savePath)
                else:
                    if args.verbose:
                        print(fileName+ ' found. Skipping.')
        
        print('Finished processing thread!')
