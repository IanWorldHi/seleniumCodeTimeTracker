import json
import time
import argparse
#Built in python module for running command line args

from bs4 import BeautifulSoup

from datetime import datetime
from typing import Optional

from dataclasses import dataclass, field, asdict
#Let's declaring dataclasses by just writing fields so no need for init func

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#Allows configuring how chrome launches like invisible no gui

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Allows waiting in certain scenarios vs implicitly_wait wait runs after every find element i think


#not using rn
opts = Options()
opts.add_argument("--headless=new")


#Error is because Pylance's type stubs for Selenium is outdated (confused typechcker)
#Doesn't recognize webdriver has callable attribute - works at runtime

#driver = webdriver.Chrome(options=opts) 
#^breaks the click()
driver = webdriver.Chrome()
driver.get("https://uwaterloo.ca/daily-bulletin/")

driver.implicitly_wait(0.5)

linkToLatestPost = driver.find_element(By.CLASS_NAME, "card__title")
linkToLatestPost2 = linkToLatestPost.find_element(By.TAG_NAME, "a")

#For later backend use - date of latest post so only run for new posts
datenow = linkToLatestPost2.text

#print(linkToLatestPost2.get_attribute("outerHTML"))
linkToLatestPost2.click()

class subTopic:
    id: str
    title: str
    paragraphs: list[str] = field(default_factory=list)
    #basically calling list constructor to make empty list for each instance of subTopic - if i did = [] would be same list for all instances
    images: list[dict] = field(default_factory=list) #{src, alt}
    links: list[dict] = field(default_factory=list) #{text, href}
    subtopics: list[dict] = field(default_factory=list) #{uhhh we'll see}
    

#def textCollector - 

#line 568 & 569 - all the important content is in there
#end 1289 (for 668) till 1292 so should be chill up to 566

#"." instead of spaces for css selector to indicate compound classes
subHeadings = driver.find_elements(By.CSS_SELECTOR, ".layout__region.layout__region--first .uw-text-align--left.block.block-layout-builder.block-inline-blockuw-cbl-copy-text .uw-copy-text .uw-copy-text__wrapper")
mainContent = subHeadings[2].get_attribute("outerHTML")

headings = []
n = mainContent.find("<h2>")
i = 0
while n != -1:
    m = mainContent.find("<h2>", n+1)
    if m == -1:
        headings.append(mainContent[n:])
        #headings[0] = {"title": "Bulletin"}
    else:
        headings.append(mainContent[n:m])
    n = m
    i+=1
print(headings[1])



#print(subHeadings.get_attribute("outerHTML"))

""" html = mainContent
with open("htmlOrg.html", "w", encoding="utf-8") as f:
    f.write(html) """



