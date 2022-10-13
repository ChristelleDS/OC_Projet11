import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


@pytest.fixture(scope="class")
def browser_init(request):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager(path=r"drivers").install()))
    request.cls.driver = browser
    browser.implicitly_wait(20)
    browser.maximize_window()
    yield
    browser.close()
    browser.quit()


@pytest.mark.usefixtures("browser_init")
class TestBoardLogin:

    def test_loadBoard_loginKO_loginOK(self):
        # USE CASE 1:
        # Visit the points board page
        # Login with incorrect email
        # Login with a valid email
        # Welcome Page

        # Load the BOARD page
        self.browser.get('http://127.0.0.1:5000/pointsBoard')
        assert 'Clubs Board' in self.browser.title
        self.browser.find_element(By.ID, 'index_link').click()
        time.sleep(2)

        # Load the login page
        assert 'GUDLFT Registration' in self.browser.title
        time.sleep(2)

        # Find the email input field and write an invalid email
        self.browser.find_element(By.NAME, 'email').send_keys('johnsimplylift.co')

        # Find the validation button and click on
        self.browser.find_element(By.ID, 'email_validation').click()
        time.sleep(2)

        # check the flash error message
        flash_info = self.browser.find_element(By.ID, 'flash_mess')
        flash_info_content = flash_info.text
        assert "Login error" in flash_info_content

        # write a valid email and click on validation button
        self.browser.find_element(By.NAME, 'email').send_keys('john@simplylift.co')
        self.browser.find_element(By.ID, 'email_validation').click()
        time.sleep(3)

        # welcome page
        assert 'Summary' in self.browser.title

    def test_loadSummary_bookCompetition(self):
        # USE CASE 2:
        # Login with valid email
        # Book 2 places on a future competition
        # Logout

        # Login
        self.browser.get('http://127.0.0.1:5000/')
        self.browser.find_element(By.NAME, 'email').send_keys('john@simplylift.co')
        self.browser.find_element(By.ID, 'email_validation').click()
        time.sleep(3)

        # Load Summary page
        assert 'Summary' in self.browser.title
        init_points = self.browser.find_element(By.ID, 'Nb_avail_points')
        self.browser.find_element(By.LINK_TEXT, 'Book Places').click()
        time.sleep(3)

        # Load booking page
        assert 'Booking' in self.browser.title
        nb_places = 2
        self.browser.find_element(By.NAME, 'places').send_keys(nb_places)
        self.browser.find_element(By.ID, 'Book_validation').click()
        time.sleep(3)

        # Check redirection to summary and check points update
        assert 'Summary' in self.browser.title
        new_points = self.browser.find_element(By.ID, 'Nb_avail_points')
        assert new_points == init_points - nb_places

        # check the flash message
        flash_info = self.browser.find_element(By.ID, 'flash_mess')
        flash_info_content = flash_info.text
        assert "booking complete" in flash_info_content

        # logout
        self.browser.find_element(By.LINK_TEXT, 'Logout').click()

        # check index redirection
        assert 'GUDLFT Registration' in self.browser.title
