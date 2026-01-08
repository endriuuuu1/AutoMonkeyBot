from tkinter.font import names

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Firefox()

driver.get("https://monkeytype.com/")
# driver.get("http://www.python.org")
# if driver.title == "Python":

heading = driver.find_element(By.TAG_NAME, "h1")

print(heading.text)


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