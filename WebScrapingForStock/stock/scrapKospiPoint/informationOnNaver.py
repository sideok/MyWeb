'''
Created on 2018. 8. 19.

@author: SIDeok
'''

import urllib.request
from bs4 import BeautifulSoup

def collectInformation() :
    html = urllib.request.urlopen('http://comic.naver.com/webtoon/weekday.nhn')
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("a", "title")

    for title in titles:
        print(title)
        
collectInformation()