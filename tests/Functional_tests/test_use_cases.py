from selenium import webdriver
from selenium.webdriver.common.by import By
import time


browser = webdriver.Firefox()


def test_loadBoard_loginKO_loginOK(browser):
    # USE CASE 1:
    # Visit the points board page
    # Login with incorrect email
    # Login with a valid email
    # Welcome Page

    # Load the BOARD page
    browser.get('http://127.0.0.1:5000/pointsBoard')
    assert 'Clubs Board' in browser.title
    link = browser.find_element(By.ID, 'index_link')
    link.click()
    time.sleep(3)

    # Load the login page
    # browser.get('http://127.0.0.1:5000/')
    assert 'GUDLFT Registration' in browser.title
    time.sleep(2)

    # Find the email input field
    elem = browser.find_element(By.NAME, 'email')
    elem.send_keys('johnsimplylift.co')  # write a invalid email

    # Find the validation button and click on
    button = browser.find_element(By.ID, 'email_validation')
    button.click()
    time.sleep(3)

    # check the flash error message
    flash_info = browser.find_element(By.ID, 'flash_mess')
    flash_info_content = flash_info.text
    assert "Login error" in flash_info_content
    time.sleep(3)

    # write a valid email
    elem.send_keys('john@simplylift.co')
    button.click()
    time.sleep(3)

    # welcome page
    assert 'Summary' in browser.title
    browser.quit()
    return True
