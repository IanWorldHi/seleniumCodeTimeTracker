import time 
from selenium import webdriver
from selenium.webdriver.common.by import By

#It shows an error but works lol
driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

#time.sleep(1) just pauses for 1 sec

title = driver.title

#waiting strats: 
#this one temp - not the greatest
driver.implicitly_wait(0.5) #waits before throwing error if element not found

text_box1 = driver.find_element(by=By.NAME, value="my-text")
submit_button1 = driver.find_element(by=By.CSS_SELECTOR, value="button")  

text_box1.send_keys("Test")
time.sleep(1)
submit_button1.click()
time.sleep(1)
message1 = driver.find_element(by=By.ID, value="message")
text = message1.text

print(title)
print(text)
driver.quit()


