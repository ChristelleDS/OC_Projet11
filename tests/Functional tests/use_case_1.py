from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()

# USE CASE 1:
# Visit the points board page
# Login
# Welcome Page
# Book a competition with success
# logout



# Load the BOARD page
browser.get('http://127.0.0.1:5000/pointsBoard')
assert 'Clubs Board' in browser.title

# Load the login page
browser.get('http://127.0.0.1:5000/')
assert 'GUDLFT Registration' in browser.title

# Find the email input field
elem = browser.find_element(By.NAME, 'email')
elem.send_keys('john@simplylift.co')  # write a valid email

# Find the validation button and click on
button = browser.find_element(By.ID, 'email_validation')
button.click()

browser

browser.quit()