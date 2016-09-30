#downloads an IMAGE to the provided path. 
def downloadImage(url,path):
    import requests
    #from PIL import Image
    with open(path,"wb") as file:
        response = requests.get(url)
        logging.info('Writing '+ path)
        file.write(response.content)

#data validation for directory output argument
def validateFolder(string):
    name = str(string)
    if len(name) == 0:
        msg = 'Empty directory path supplied. Please supply a directory.'
        raise argparse.ArgumentTypeError(msg)
    return name

#Checks if input folder exists in the appropriate directory. If not, create it.
def getFolder(folder, verbose, dest):
    output = ' '
    if dest is not None:
        if dest[0] == '~':
            output = os.path.join(os.path.expanduser(dest), folder)
        else:
            output = os.path.join(os.path.abspath(dest),folder)
    else:
        output = os.path.join(os.getcwd(), folder)
    if not os.path.exists(output):
        os.makedirs(output)
        logging.info('Created ' + output)
    return output

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
    import os

    parser = argparse.ArgumentParser(description='Process a 4chan thread to scrape all images from.')
    parser.add_argument('url',nargs='+', type=validateUrl, help='a list, separated by spaces, of web addresses to be parsed')
    parser.add_argument('-d', type=validateFolder, help='Specify a directory to output files to.', dest='dest')
    parser.add_argument('-v', help='verbose. Turn on debug output.', action='store_true', dest='verbose')
    parser.add_argument('-ns', help='No saving. This disables actually modifying the filesystem.', action='store_false', dest='save')
    args = parser.parse_args()

    from BeautifulSoup import BeautifulSoup
    import requests
    from StringIO import StringIO
    import os
    import logging
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

    for link in args.url:
        logging.info('Processing '+link)

        response = requests.get(link)
        html = response.content

        soup = BeautifulSoup(html)

        folderName = createFolderName(soup.title.string.replace('/',''))

        folder = getFolder(folderName, args.verbose, args.dest)
        logging.info('Capturing ' + folderName)
        
        for link in soup.findAll('div','fileText'): 
            imageName = link.a.get('href')
            logging.info('Processing ' + imageName)
            title = link.a.get('title')
            #save the title as the filename
            if title is not None:
                #savePath = './'+folderName+'/'+title
                savePath = os.path.join(folder,title)
                logging.info('Title is found. Using it as filename; ' + title)
                if not os.path.isfile(savePath):
                    if args.verbose:
                        logging.info('Saving from http:' + imageName)
                        logging.info('No previous file exists. Saving to ' + savePath)
                        logging.info('Saving files: ' + str(args.save) )
                    if args.save:
                        downloadImage('http:'+imageName,savePath)
                else:
                    logging.info('File exists. Skipping it.')

            #save the filename as the filename 
            else:
                fileName = re.search('\d+\.\w+$',imageName).group(0)
                logging.info('Title not found. Using filepath as filename;  ' + fileName)
                savePath = os.path.join(folder,fileName)
                logging.info('saving:' + savePath)
                if not os.path.isfile(savePath):
                    if args.save:
                        downloadImage('http:'+imageName,savePath)
                else:
                    logging.info(savePath+ ' found. Skipping.')
        logging.info('Finished processing thread!')
            
        
