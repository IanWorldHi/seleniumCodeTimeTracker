import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://uwaterloo.ca/daily-bulletin/")

title = driver.title

driver.implicitly_wait(0.5)

print(title)



