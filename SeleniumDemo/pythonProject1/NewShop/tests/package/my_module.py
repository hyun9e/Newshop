import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# For chrome config: disable notification and maximize window
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
# For hovering function
from selenium.webdriver.common.action_chains import ActionChains

option = Options()
option.add_argument("--disable-notifications")
option.add_argument("start-maximized")

# Initiate Chrome WebDriver (Open Chrome)
driver = webdriver.Chrome(options=option)
# Define Impliticity wait time
wait = WebDriverWait(driver, 10)
# For Hovering Function
actions = ActionChains(driver)


def quit_driver():
    time.sleep(2)
    global driver
    if driver is not None:
        driver.quit()
        driver = None

# Find an element by XPATH
def find_by_xpath(element_path):
    return driver.find_element(By.XPATH, element_path)


# Find an element by XPATH and Click it
def find_and_click_by_xpath(element_path):
    find_by_xpath(element_path).click()


# Hover cursor to the element by XPATH
def hover_by_xpath(element_path):
    elem = actions.move_to_element(find_by_xpath(element_path))
    elem.perform()


# Wait for an element to be clickable
def wait_until_clickable_xpath(element_path):
    wait.until(ec.element_to_be_clickable(
        (By.XPATH, element_path))).click()


# Wait for the element presence
def wait_for_presence_xpath(element_path):
    return wait.until(ec.presence_of_element_located(
        (By.XPATH, element_path)))


