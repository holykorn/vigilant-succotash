from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Test_1():
    def test_select_product(self):
        path = Path("drivers","chromedriver.exe")
        driver = webdriver.Chrome(executable_path= path)
        base_url = 'https://www.saucedemo.com'
        driver.get(base_url)
        print ('Start test')
        login_standard_user = 'standard_user'
        password_all = 'secret_sauce'
        right_url = 'https://www.saucedemo.com/inventory.html'
        username = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#user-name')))
        username.send_keys(login_standard_user)
        password = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input#password')))
        password.send_keys(password_all)
        password.send_keys(Keys.RETURN)
        time.sleep(10)


test = Test_1()
test.test_select_product()