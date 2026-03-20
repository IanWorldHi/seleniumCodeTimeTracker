import time 
from selenium import webdriver
from selenium.webdriver.common.by import By

#wakatime extension disabled for now - web should still work though
driver = webdriver.Chrome()
driver.get("https://wakatime.com/dashboard")
driver.implicitly_wait(0.5) 

#dailyTime = driver.find_element(by=By.CSS_SELECTOR, value="span.grand-total")
#test = dailyTime.text

#have to login first.. wait would i have to login every time? cookies or smth? or github is gonna be annoying cuz 2factor
tester = driver.find_element(by=By.CSS_SELECTOR, value="div.nice-title")
test2 = tester.text
print(test2)

#text_box1 = driver.find_element(by=By.NAME, value="my-text")
#submit_button1 = driver.find_element(by=By.CSS_SELECTOR, value="button")  

#text_box1.send_keys("Test")
#submit_button1.click()
#message1 = driver.find_element(by=By.ID, value="message")
#text = message1.text

#print(test)
driver.quit()


