# -*- coding: utf-8 -*-
import urllib.request
import re
import time
import os

from selenium import webdriver

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def downloadPinterestImages(link, base_dir):
    with webdriver.Firefox(executable_path=r'/usr/bin/geckodriver') as browser:
        create_dir(base_dir)
        print(link)
        
        browser.get(link)
        
        time.sleep(2)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        #limit=7 #limit of scrolls
        count = 0
        while(not match): #auto scroll till end or till limit
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            is_more_ideas = browser.execute_script("let h2 = document.getElementsByTagName('h2'); for(let i of h2) { if (i.textContent === 'More ideas') { return true; }  }; return false;")
            if is_more_ideas:
                print(f"More ideas found {count}")
                match = True
            #limit = limit-1
            if lastCount==lenOfPage:
                print(f"stop scrolling {count}")
                match=True
            else:
                count = count + 1
                print(f"scrolling... {count}")

        response = browser.page_source#.encode(encoding='UTF-8')

        toDel =[]
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response)

        print(len(urls))
        for i in range(len(urls)):
            if(urls[i][-4:]==".jpg"):
                urls[i]=re.sub('.com/.*?/','.com/originals/',urls[i],flags=re.DOTALL)
            else:
                urls[i]= ""

        urls = list(set(urls))

        #urls = list(filter(None, urls)) # fastest
        #urls = list(filter(bool, urls)) # fastest
        urls = list(filter(len, urls))  # a bit slower
        length = len(urls)
        print(f"links found {length}")

        with open(base_dir +"/raw.txt", 'w') as f:
            for url in urls:
                f.write("%s\n" % url)

        for i in range(len(urls)):
            print(f'Trying {i}/{length}')
            try:
                (path, message) = urllib.request.urlretrieve(urls[i], f"{base_dir}/{str(i)}_img.jpg")
                print(f"{path}")
            except Exception as e:
                print(f"Broken Link {e}")
        
        
user = "shutterstock"
boards = ['inspiring-image-collections', '2020s-monthly-fresh-recap']

for board in boards:
    link=f"https://pinterest.fr/{user}/{board}/"
    downloadPinterestImages(link,f'./{board}')
    