import pyautogui as pag
import time as t
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# for now manually run chrome instance in debug mode:
# .\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\chrome-profile"
# after some time I will automate this from python or from bat


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)


#driver = webdriver.Chrome()
# driver.get("https://monkeytype.com/") # commented out for now because it refreshes the page
# driver.get("http://www.python.org")
# t.sleep(2) # needs to get sleep after refresh
# heading = driver.find_element(By.TAG_NAME, "h1")
word_container = driver.find_element(By.ID, "words")
word_elements = word_container.find_elements(By.CLASS_NAME, "word")

for w in word_elements:
    print(w.text)

# print(heading.text)
# print(list(words))

# assert "Python" in driver.title
#     if driver.title == "Python":
#
# if names == __name__:
#     try:
#         assert "monkeytype" in driver.title
#         if driver.title == "monkeytype":
#             print("found Monkey Type")
#     except AssertionError:
#         print("No monkeytype found")