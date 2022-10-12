from selenium import webdriver
from selenium.webdriver.common.by import By
import time


browser = webdriver.Firefox(executable_path=r'C:\Users\chris\OneDrive\Documents\OCP11\Projet11\Python_Testing\tests\Functional_tests\geckodriver.exe')


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


def test_loadSummary_bookCompetition(browser):
    # USE CASE 2:
    # Login with valid email
    # Book 2 places on a future competition
    # Logout

    # Login
    browser.get('http://127.0.0.1:5000/')
    elem = browser.find_element(By.NAME, 'email')
    elem.send_keys('john@simplylift.co')
    button = browser.find_element(By.ID, 'email_validation')
    button.click()
    time.sleep(3)

    # Load Summary page
    # browser.get('http://127.0.0.1:5000/showSummary')
    assert 'Summary' in browser.title
    init_points = browser.find_element(By.ID, 'Nb_avail_points')
    link = browser.find_element(By.LINK_TEXT, 'Book Places')
    link.click()
    time.sleep(3)

    # Load booking page
    assert 'Booking' in browser.title
    nbPlaces = browser.find_element(By.NAME, 'places')
    nbPlaces = 2
    nbPlaces.send_keys(nbPlaces)
    valid = browser.find_element(By.ID, 'Book_validation')
    valid.click()
    time.sleep(3)

    # Check redirection to summary and check points update
    assert 'Summary' in browser.title
    new_points = browser.find_element(By.ID, 'Nb_avail_points')
    assert new_points == init_points - nbPlaces

    # check the flash message
    flash_info = browser.find_element(By.ID, 'flash_mess')
    flash_info_content = flash_info.text
    assert "booking complete" in flash_info_content
    time.sleep(3)

    # logout
    logout = browser.find_element(By.LINK_TEXT, 'Logout')
    logout.click()

    # check index redirection
    assert 'GUDLFT Registration' in browser.title
    browser.quit()
