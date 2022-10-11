from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()

# Load the login page
browser.get('http://127.0.0.1:5000/')
assert 'GUDLFT Registration' in browser.title

elem = browser.find_element(By.NAME, 'email')  # Find the email input
elem.send_keys('john@simplylift.co')  # write a valid email

browser.quit()