import pyautogui as pag
import time as t
import socket
import subprocess
from configClass import TestConfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

PORT: int = 9222
MONKEYTYPE_URL: str = "https://monkeytype.com/"

# manual debug mode for chrome in Terminal
# C:\Program Files\Google\Chrome\Application\chrome.exe = Dir Address
# .\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\chrome-profile"

# automation for chrome debug mode
# def is_port_open(port: int)-> bool:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         return s.connect_ex(("127.0.0.1", port)) == 0

def session_init():
    # automation for chrome debug mode
    def is_port_open(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0

    # check if debug mode port is open or not and launch driver instance with asserted port if it's not
    if not is_port_open(PORT):
        subprocess.Popen([
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            f"--remote-debugging-port={PORT}",
            r"--user-data-dir=C:\selenium\chrome-profile"
        ])




# all the credential handling logic and automation goes in here - used later for logins
def auth():
    pass

# for now my account. for future creds.txt/json to login
def monkey_login():
    # login with my account on monkeytype.com website
    pass

def remove_blur():
    # automatic blur remover from words canvas
    pass

def restart_test():
    # tab + enter keyboard input logic: which resets test canvas
    with pag.hold('tab'):
        pag.press('enter')

# driver.maximize_window() # resizes window to the maximum available screen space
# driver.fullscreen_window() # invokes fullscreen operation (like pressing F11)
# driver.get("https://monkeytype.com/")
# t.sleep(2) # needs to sleep after refresh (driver.get method)
# word_container = driver.find_element(By.ID, "words")
# word_elements = word_container.find_elements(By.CLASS_NAME, "word")
#
# for w in word_elements:
#     print(f"word: {w.text.lower()} + index: {word_elements.index(w)}")


if __name__ == "__main__":
    # Phase 1: Environment & Session Initialization
    # Port Check and driver instance launch
    session_init()

    # Driver Handshake: debug mode options and webdriver assignment
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{PORT}")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigation Check: if the current url is monkeytype or not
    if driver.current_url != MONKEYTYPE_URL:
        driver.get(MONKEYTYPE_URL)
    else:
        pass
