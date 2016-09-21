This project is an attempt to craft a clean, easy to understand 
implementation of a scraper for 4chan. 

Requirements:
virtualenv is recommended for this project, to install all the 
dependencies of the project in a virtual environment.

In linux, the command is;

sudo pip install virtualenv

Once there, a quick google of virtualenv grants usage. The requirements file
has been prepared, so run

pip install -r requirements.txt

to get everything in order.


Usage: 
Calling

python 4ChanWebScraper.py <address>

scrapes the target into a new folder in the current working directory of the script.