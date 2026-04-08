import json
import time
import argparse
#Built in python module for running command line args

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

#Error is because Pylance's type stubs for Selenium is outdated (confused typechcker)
#Doesn't recognize webdriver has callable attribute - works at runtime
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
    

subHeadings = driver.find_elements(By.CLASS_NAME, "uw-copy-text__wrapper ")
#for sub in subHeadings:
#    print(sub.get_attribute("outerHTML"))
#print(subHeadings.get_attribute("outerHTML"))

html = driver.page_source
with open("htmlOrg.html", "w", encoding="utf-8") as f:
    f.write(html)



