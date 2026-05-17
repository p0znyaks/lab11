import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_page_loads(driver):
    path = os.path.abspath('index.html').replace('\\', '/')
    driver.get(f'file:///{path}')
    assert 'Регистрация' in driver.title
    assert driver.find_element(By.ID, 'regForm').is_displayed()


def test_successful_submission(driver):
    path = os.path.abspath('index.html').replace('\\', '/')
    driver.get(f'file:///{path}')
    driver.find_element(By.ID, 'name').send_keys('Иван')
    driver.find_element(By.ID, 'email').send_keys('ivan@example.com')
    driver.find_element(By.ID, 'password').send_keys('123456')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    result = driver.find_element(By.ID, 'result')
    assert 'Регистрация успешна' in result.text


def test_empty_fields_show_errors(driver):
    path = os.path.abspath('index.html').replace('\\', '/')
    driver.get(f'file:///{path}')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert 'Введите имя' in driver.find_element(By.ID, 'nameError').text
    assert 'Введите email' in driver.find_element(By.ID, 'emailError').text
    assert 'Введите пароль' in driver.find_element(By.ID, 'passwordError').text


def test_invalid_email_shows_error(driver):
    path = os.path.abspath('index.html').replace('\\', '/')
    driver.get(f'file:///{path}')
    driver.find_element(By.ID, 'name').send_keys('Иван')
    driver.find_element(By.ID, 'email').send_keys('invalid')
    driver.find_element(By.ID, 'password').send_keys('123456')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert 'Некорректный email' in driver.find_element(By.ID, 'emailError').text


def test_short_password_shows_error(driver):
    path = os.path.abspath('index.html').replace('\\', '/')
    driver.get(f'file:///{path}')
    driver.find_element(By.ID, 'name').send_keys('Иван')
    driver.find_element(By.ID, 'email').send_keys('ivan@example.com')
    driver.find_element(By.ID, 'password').send_keys('123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert 'не менее 6 символов' in driver.find_element(By.ID, 'passwordError').text
