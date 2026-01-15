import pyautogui as pag
import time as t
import socket
import subprocess
import json
from selenium.common import NoSuchElementException
from configClass import TestConfig
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Constants:
PORT: int = 9222
MONKEYTYPE_URL: str = "https://monkeytype.com/"
MONKEYTYPE_LOGIN_URL: str= "https://monkeytype.com/login"
SIZE_PIXEL_BUFFER: int = 50
POSITION_PIXEL_BUFFER: int = 12
CENTER_X = (pag.size().width / 2)
CENTER_Y = (pag.size().height / 2)

# manual debug mode for chrome in Terminal
# C:\Program Files\Google\Chrome\Application\chrome.exe = Dir Address
# .\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\chrome-profile"

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

def is_maximised(driver_instance: WebDriver) -> bool:
    # retrieve screen capacity (w pag) and browser dimensions (w selenium)
    screen_size = pag.size()
    driver_size = driver_instance.get_window_size()
    driver_position = driver.get_window_position()

    # Driver and Screen Dimensions - (d) and (s) variables
    d_width = driver_size.get("width")
    d_height = driver_size.get("height")
    s_width = screen_size.width
    s_height = screen_size.height
    x_pos = driver_position.get("x")
    y_pos = driver_position.get("y")

    # Absolute values for size checks
    abs_width_diff= abs(s_width - d_width) # absolute difference so that it's not a negative number
    abs_height_diff= abs(s_height - d_height)
    home_pos = (abs(x_pos), abs(y_pos)) # need absolute for Primary Monitor

    if ((abs_width_diff <= SIZE_PIXEL_BUFFER and abs_height_diff <= SIZE_PIXEL_BUFFER)
            and (home_pos[0] <= POSITION_PIXEL_BUFFER and home_pos[1] <= POSITION_PIXEL_BUFFER)):
        return True
    else:
        return False

# all the credential handling logic and automation goes in here - used later for logins
def auth():
    pass

# checking logic for authentification
def is_logged_in(driver_instance) -> bool:
    try:
        btn_element = driver_instance.find_element(By.CSS_SELECTOR, '.textButton.view-account')
        return btn_element.is_displayed()
    except NoSuchElementException as e:
        print(f"error element not found")
        return False

# login logic with credentials goes in here:
def monkey_login(driver_instance):
    # login with my account on monkeytype.com website

    # this has to be done using auth() later
    # which will handle all the credential logic
    with open('creds.JSON', 'r') as f:
        creds = json.load(f)
    email = creds['email']
    password = creds['password']

    # This is her just for now. will be entering the creds logic:
    pag.click(CENTER_X-130,CENTER_Y)
    restart_test()
    # monkey_login Logic:
    # 1. Locate Fields: Use driver.find_element(By.ID, '...') or By.NAME to find the email and password inputs.
    # 2. Input Data: Use element.send_keys(email) and element.send_keys(password).
    # 3. Submit: Find the "Sign In" button and use .click(), or simply send Keys.ENTER to the password field.


# automatic blur remover from words canvas
def remove_blur():
    pag.click(CENTER_X, CENTER_Y)

# tab + enter keyboard input: resets the test canvas
def restart_test():
    with pag.hold('tab'):
        pag.press('enter')


if __name__ == "__main__":
    # Phase 1: Environment & Session Initialization
    # Port Check and driver instance launch
    session_init()

    # Driver Handshake: debug mode options and webdriver assignment
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{PORT}")
    driver = webdriver.Chrome(options=chrome_options)

    # this is a dynamic safety for element discovery. tells the bot: "If you don't see an element right away, don't crash."
    # Unlike t.sleep(), this will not force a pause if the element is found immediately.
    # It will keep looking for up to 10 seconds.
    # If it finds the element in 1 second, it moves on immediately.
    # It only waits the full 10 seconds if the element is truly missing. (throwing a NoSuchElementException).
    driver.implicitly_wait(10)

    # Window Maximisation Check: is_maximised returns True if size and position pixels are within relevant buffer ranges
    if not is_maximised(driver):
        driver.maximize_window()
        print("invoked maximize_window")
    else:
        print("windows is already maximised")

    # Navigation Check: if the current url is monkeytype or not
    if driver.current_url != MONKEYTYPE_URL:
        driver.get(MONKEYTYPE_URL)
    else:
        pass

    # Phase 2: User Authentication - Log In with my account
    if not is_logged_in(driver):
        monkey_login(driver)
    else:
        print("already logged in")

    # Phase X: Word handler/parser
    # word_container = driver.find_element(By.ID, "words")
    # word_elements = word_container.find_elements(By.CLASS_NAME, "word")
    #
    # for w in word_elements:
    #     print(f"word: {w.text.lower()} + index: {word_elements.index(w)}")