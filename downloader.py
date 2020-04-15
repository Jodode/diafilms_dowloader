import argparse
import re
import requests
from bs4 import BeautifulSoup

def createParser():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('--url', action='store', type=str, default="https://google.com", help='url for download')
    parser.add_argument('--path', action='store', type=str, default=".", help='out directory')
    
    return parser


def main():
    parser = createParser()
    namespace = parser.parse_args()

    valid_url_re = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

    if valid_url_re.match(namespace.url) is None:
    	print("""usage: downloader.py [-h] [--url URL] [--path PATH]
downloader.py: error: argument --url: bad URL""")
    else:
    	url = namespace.url
    	path = namespace.path
    	r = requests.get(url)
    	if r.status_code == 200:

    		soup = BeautifulSoup(r.text, 'html.parser')
    		tags = soup.find_all(class_="fullscreen")[0]
    		descr = soup.find_all(class_="diafulltable")[0]

    		for tag in tags:
    			try:
    				data = tag.find_all("img")
    				break
    			except:
    				pass
    		name = data[0]["alt"]
    		urls = []
    		for u in data:
    			urls.append(u["src"])
    		print("Preparation for download...")
    		download_link_host = url.split('/')[0] + '//' + url.split('/')[2]

    		for i, content in enumerate(urls):
    			open(f'{path}/{name} ({i}).jpg', 'wb').write(requests.get(download_link_host + content).content)
    		print("Downloading...")
    		open(f'{path}/description.txt', 'w').write(descr.text)
    		print("Saving...")

    		print(f"{len(urls)} saved pictures and 1 description")
    		print("-"*50)
    		print(descr.text)

if __name__ == "__main__":
    main()
