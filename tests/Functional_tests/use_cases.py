import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


@pytest.fixture(scope="class")
def browser_init(request):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(path=r"drivers").install()))
    request.cls.driver = driver
    driver.implicitly_wait(20)
    driver.maximize_window()
    yield
    driver.close()
    driver.quit()


@pytest.mark.usefixtures("browser_init")
class TestBoardLogin:

    def test_loadBoard_loginKO_loginOK(self):
        # USE CASE 1:
        # Visit the points board page
        # Login with incorrect email
        # Login with a valid email
        # Welcome Page

        # Load the BOARD page
        self.driver.get('http://127.0.0.1:5000/pointsBoard')
        assert 'Clubs Board' in self.driver.title
        self.driver.find_element(By.ID, 'index_link').click()
        time.sleep(1)

        # Load the login page
        assert 'GUDLFT Registration' in self.driver.title

        # Find the email input field and write an invalid email
        self.driver.find_element(By.NAME, 'email').send_keys('johnsimply@lift')

        # Find the validation button and click on
        self.driver.find_element(By.ID, 'email_validation').click()

        # check the flash error message
        # flash_info = self.driver.find_element(By.ID, 'flash_mess').text
        assert "Login error" in self.driver.find_element(By.ID, 'flash_mess').text
        # assert "Login error" in self.driver.find_element(By.TAG_NAME, "li").text

        # write a valid email and click on validation button
        self.driver.find_element(By.NAME, 'email').send_keys('john@simplylift.co')
        self.driver.find_element(By.ID, 'email_validation').click()
        time.sleep(1)

        # welcome page
        assert 'Summary' in self.driver.title

    def test_loadSummary_bookCompetition(self):
        # USE CASE 2:
        # Login with valid email
        # Book 2 places on a future competition
        # Logout

        # Login
        self.driver.get('http://127.0.0.1:5000/')
        self.driver.find_element(By.NAME, 'email').send_keys('john@simplylift.co')
        self.driver.find_element(By.ID, 'email_validation').click()
        time.sleep(1)

        # Load Summary page
        assert 'Summary' in self.driver.title
        init_points = int(self.driver.find_element(By.ID, 'Nb_avail_points').text[-2:])
        self.driver.find_element(By.LINK_TEXT, 'Book Places').click()
        time.sleep(1)

        # Load booking page
        assert 'Booking' in self.driver.title
        nb_places = 2
        self.driver.find_element(By.NAME, 'places').send_keys(nb_places)
        self.driver.find_element(By.ID, 'Book_validation').click()
        time.sleep(1)

        # Check redirection to summary and check points update
        assert 'Summary' in self.driver.title
        avail_pts = int(self.driver.find_element(By.ID, 'Nb_avail_points').text[-2:])
        assert avail_pts == (init_points - nb_places)

        # check the flash message
        assert "booking complete" in self.driver.find_element(By.ID, 'flash_mess').text

        # logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # check index redirection
        assert 'GUDLFT Registration' in self.driver.title
