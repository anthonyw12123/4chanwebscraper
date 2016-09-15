# 4chanwebscraper
A primitive web scraper using Python. 

usage: python 4chanwebscraper.py <address of 4chan thread>

This uses some pip packages in order to do its work;
-BeautifulSoup
-Image
-requests

To install these packages, on BSD, run

sudo pip install beautifulsoup
sudo pip install image
sudo pip install requests

This utility crates a new folder in the same folder that it was executed in, setting the name of that
folder to the title of the 4chan thread, and then finds and downloads all higher-res images that
it knows to find.
