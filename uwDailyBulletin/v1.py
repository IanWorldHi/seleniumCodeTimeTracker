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

def _parse_sections(html):
    sections = []
    n = html.find("<h2>")
    while n != -1:
        m = html.find("<h2>", n+1)
        end = m if m != -1 else len(html)
        soup = BeautifulSoup(html[n:end], "html.parser")

        parts = []
        title = soup.find("h2")
        if title is not None:
            parts.append(title.get_text(strip=True))
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                parts.append(text)
        for img in soup.find_all("img"):
            alt = img.get("alt")
            if alt:
                parts.append(alt)
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            href = link.get("href")
            if href:
                parts.append(f"{text}: {href}" if text else href)

        sections.append("\n".join(parts))
        n = m
    return sections

def get_latest_post():
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

    linkToLatestPost2.click()

    #"." instead of spaces for css selector to indicate compound classes
    subHeadings = driver.find_elements(By.CSS_SELECTOR, ".layout__region.layout__region--first .uw-text-align--left.block.block-layout-builder.block-inline-blockuw-cbl-copy-text .uw-copy-text .uw-copy-text__wrapper")
    mainContent = subHeadings[2].get_attribute("outerHTML")

    sections = _parse_sections(mainContent)

    #sidebar with "When and Where" and "Upcoming service interruptions", lives in region--second not --first
    sidebarWrappers = driver.find_elements(By.CSS_SELECTOR, ".layout__region.layout__region--second .uw-text-align--left.block.block-layout-builder.block-inline-blockuw-cbl-copy-text .uw-copy-text .uw-copy-text__wrapper")
    if sidebarWrappers:
        whenAndWhere = sidebarWrappers[-1].get_attribute("outerHTML")
        sections.extend(_parse_sections(whenAndWhere))

    return "\n\n".join(sections)

print(get_latest_post())

#print(subHeadings.get_attribute("outerHTML"))

""" html = mainContent
with open("htmlOrg.html", "w", encoding="utf-8") as f:
    f.write(html) """



