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
TEST = TestConfig('time', 30, 'english 1k',100)
TEST_TEMP = TestConfig('words', 100, 'english',80, True,True )
# manual debug mode for chrome in Terminal
# C:\Program Files\Google\Chrome\Application\chrome.exe = Dir Address
# .\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenium\chrome-profile"

# Initializes a debug-mode chrome instance on provided port
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

# Checks screen and browser Dimensions and returns a boolean
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
def is_logged_in(driver_instance: WebDriver) -> bool:
    # old method which worked but apparently doesn't anymore
    # try:
    #     btn_element = driver_instance.find_element(By.CSS_SELECTOR, '.textButton.view-account')
    #     return btn_element.is_displayed()
    # except NoSuchElementException as e:
    #     print(f"error element not found")
    #     return False

    # New method:
    t.sleep(1)
    try:
        account_btn = driver_instance.find_elements(By.CSS_SELECTOR, '.textButton.view-account')
        if len(account_btn) > 0 and account_btn[0].is_displayed():
            return True
        return False
    except Exception:
        return False

# LogIn logic with credentials goes in here:
def monkey_login(driver_instance: WebDriver):
    # Navigation:
    driver_instance.get(MONKEYTYPE_LOGIN_URL)
    # Wait for the site to process the session
    t.sleep(2)

    login_fields = driver_instance.find_elements(By.NAME, 'current-email')

    # Safety mechanism for redirect
    if len(login_fields) == 0:
        print("Safety Check: Login Fields not found. user already logged in")
        # if driver_instance.current_url == MONKEYTYPE_URL:
        #     driver_instance.get(MONKEYTYPE_URL)
        driver_instance.get(MONKEYTYPE_URL)
        return

    # login with my account on monkeytype.com website
    # this has to be done using auth() later
    # which will handle all the credential logic
    print("Log In Start: Fields Found logging in...")
    with open('creds.JSON', 'r') as f:
        creds = json.load(f)
    email = creds['email']
    password = creds['password']


    # Login action steps/sequence:
    t.sleep(1)
    # 1. Locate Fields:
    email_field = login_fields[0]
    password_field = driver_instance.find_element(By.NAME, 'current-password')
    sign_in_button = driver_instance.find_element(By.CLASS_NAME, 'signIn')

    # 2. Input Data: with send_keys() method
    t.sleep(1)
    email_field.send_keys(email)
    t.sleep(1)
    password_field.send_keys(password)
    t.sleep(1)

    # 3. Submit: send Keys.ENTER from keyboard to the sign in
    sign_in_button.send_keys(Keys.RETURN)
    t.sleep(1)

    # Navigation Check: redirect
    if driver_instance.current_url != MONKEYTYPE_URL:
        driver.get(MONKEYTYPE_URL)
        print("Log In End: log in finished")
    else:
        pass

# automatic blur remover from words canvas
def remove_blur():
    pag.click(CENTER_X, CENTER_Y)

# tab + enter keyboard input: resets the test canvas
def restart_test():
    with pag.hold('tab'):
        pag.press('enter')

# checking for configuration
def is_configured(driver_instance: WebDriver, obj: TestConfig) -> bool:
    # TEST = TestConfig('time', 30, 'english 1k',100)
    try:
        # 1. Check Mode: (time/words)
        current_mode = driver_instance.find_element(By.CSS_SELECTOR, '#config .mode .button.active').get_attribute('mode')
        if current_mode != obj.test_type:
            return False

        # 2. Check Amount (Duration or Word Count)
        if obj.test_type == 'time':
            current_time = driver_instance.find_element(By.CSS_SELECTOR, '#config .time .button.active').get_attribute('timeconfig')
            if current_time != str(obj.amount):
                return False
        elif obj.test_type == 'words':
            current_words = driver_instance.find_element(By.CSS_SELECTOR, '#config .words .button.active').get_attribute('wordcount')
            if current_words != str(obj.amount):
                return False

        # 3. Check Toggles (Only when they aren't None state)
        if obj.punctuation_toggle is not None:
            punc_active = 'active' in driver_instance.find_element(By.CSS_SELECTOR, '#config .punctuation .button').get_attribute('class')
            if punc_active != obj.punctuation_toggle:
                return False

        if obj.numbers_toggle is not None:
            num_active = 'active' in driver_instance.find_element(By.CSS_SELECTOR, '#config .numbers .button').get_attribute('class')
            if num_active != obj.numbers_toggle:
                return False

        current_lang = driver_instance.find_element(By.CSS_SELECTOR, '.group.language .text').text.lower()
        if current_lang != obj.language.lower():
            return False

        return True
    except Exception:
        return False

# test configuration and applying properties logic go in here
def configure_test(driver_instance: WebDriver, obj: TestConfig):
    # TEST = TestConfig('time', 30, 'english 1k',100)
    print("Configuring test Settings...")

    # Set Mode
    mode_btn = driver_instance.find_element(By.CSS_SELECTOR, f'#config .mode .button[mode="{obj.test_type}"]')
    if 'active' not in mode_btn.get_attribute('class'):
        mode_btn.click()
        t.sleep(0.5)

    if obj.test_type == 'time':
        selector = f"#config .time .button[timeconfig='{obj.amount}']"
    else:
        selector = f"#config .words .button[wordcount='{obj.amount}']"

    amount_btn = driver_instance.find_element(By.CSS_SELECTOR, selector)
    if 'active' not in amount_btn.get_attribute('class'):
        amount_btn.click()

    # Set Toggles
    def handle_toggle(selector_element, target_state):
        if target_state is None:
            return
        btn = driver_instance.find_element(By.CSS_SELECTOR, selector_element)
        is_active = 'active' in btn.get_attribute('class')
        if is_active != target_state:
            btn.click()

    handle_toggle('#config .punctuation .button', obj.punctuation_toggle)
    handle_toggle('#config .numbers .button', obj.numbers_toggle)

    # Set Language
    current_lang_element = driver_instance.find_element(By.CSS_SELECTOR, '.group.language .text')
    if current_lang_element.text.lower() != obj.language.lower():
        pag.press('esc')
        t.sleep(0.5)
        search_input = driver_instance.find_element(By.ID, 'languageSearch')
        search_input.send_keys(obj.language)
        t.sleep(0.5)
        search_input.send_keys(Keys.RETURN)
        print(f'Language changed to {obj.language}')

    print('Configuration Finished')


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
    # this is for the is_logged_in element lookup.
    # the login method still needs time.sleep() method to not trigger captcha
    driver.implicitly_wait(5)

    # Window Maximisation Check: is_maximised returns True if size and position pixels are within relevant buffer ranges
    if not is_maximised(driver):
        driver.maximize_window()
        print("invoked maximize_window")
    else:
        print("window is already maximised")

    # Navigation Check: if the current url is monkeytype or not
    if driver.current_url != MONKEYTYPE_URL:
        driver.get(MONKEYTYPE_URL)
    else:
        pass

    # Phase 2: User Authentication - Log In with my account
    if not is_logged_in(driver):
        monkey_login(driver)
    else:
        print("Log In Status: already logged in")

    # Phase 3: Test Configuration
    # if not is_configured(driver, TEST):
    #     configure_test(driver, TEST)
    # else:
    #     print(f'{TEST} is already configured correctly')

    # Phase 4: Word Handling/Processing
    # word_container = driver.find_element(By.ID, "words")
    # word_elements = word_container.find_elements(By.CLASS_NAME, "word")
    # for w in word_elements:
    #     print(f"word: {w.text.lower()} + index: {word_elements.index(w)} + first letter: {w.text[0]}")


    # Phase 5: Execution
    # Phase 6: Results