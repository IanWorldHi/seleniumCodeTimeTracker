import time
from selenium import webdriver
from selenium.webdriver.common.by import By

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


subHeadings = driver.find_elements(By.CLASS_NAME, "uw-copy-text__wrapper ")
for sub in subHeadings:
    print(sub.get_attribute("outerHTML"))
#print(subHeadings.get_attribute("outerHTML"))



