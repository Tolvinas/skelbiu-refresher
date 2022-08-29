import os
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def init_web_driver():
    path = os.getcwd() + "\\msedgedriver.exe"

    options = webdriver.EdgeOptions()
    # options.headless = True

    driver = webdriver.Edge(options=options, executable_path=path)
    driver.implicitly_wait(3)
    driver.get('https://www.skelbiu.lt/users/renew')
    return driver


def accept_cookies():
    accept_cookies_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    accept_cookies_button.click()


def login():
    login_name_field = driver.find_element(By.ID, 'nick-input')
    login_name_field.send_keys('REPLACE')

    password_field = driver.find_element(By.ID, 'password-input')
    password_field.send_keys('REPLACE')

    login_button = driver.find_element(By.ID, 'submit-button')
    login_button.click()

def element_exists(selector, text):
    try:
        driver.find_element(selector, text)
    except NoSuchElementException:
        return False
    return True


def renew():
    renew_button_class = 'renew-submit-button'
    if element_exists(By.CLASS_NAME, renew_button_class):
        renew_button = driver.find_element(By.CLASS_NAME, renew_button_class)
        renew_button.click()
        return 'refreshed'
    return 'already-refreshed'


def navigate():
    try:
        accept_cookies()
        login()
        renewed = renew()
    except Exception as e:
        return e
    return renewed


def save_csv_progress():
    date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    with open('refresh-status.csv', 'a', newline='', encoding='utf-8') as csvFile:
        csv_writer = csv.writer(csvFile, delimiter=',')
        csv_writer.writerow([status, date])


driver = init_web_driver()
status = navigate()
save_csv_progress()
driver.quit()
