import pytest
from random import choice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_mail():
    '''Generates email with 3 letters @ 3 letters . 3 letters'''
    letters = [chr(i) for i in range(ord('a'),ord('z')+1)]
    return ''.join(choice(letters) for l in range(3)) + '@' +\
        ''.join([choice(letters) for l in range(3)])  + '.' +\
        ''.join([choice(letters) for l in range(3)]) 

def generate_pass(nletters:int,ndigits:int):
    '''Generates password with nletters and ndigids'''
    letters = [chr(i) for i in range(ord('a'),ord('z')+1)]
    digits = [str(i) for i in range (10)]
    return ''.join([choice(letters) for l in range(nletters)]) + \
    ''.join([choice(digits) for d in range(ndigits)])

mail = generate_mail()
password = generate_pass(5,4)

def test_user_see_greeting_message(driver):
    driver.get('http://selenium1py.pythonanywhere.com/ru/')

    l_link = driver.find_element_by_css_selector('a#login_link')
    l_link.click()

    email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, \
            "#id_registration-email"))
    )
    email.send_keys(mail)

    pass1 = driver.find_element_by_css_selector('#id_registration-password1')
    pass1.send_keys(password)

    pass2 = driver.find_element_by_css_selector('#id_registration-password2')
    pass2.send_keys(password)

    button = driver.find_element_by_css_selector(\
        "form#register_form button[name='registration_submit']")
    button.click()

    success_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, \
            "div#messages div.alertinner.wicon"))
    )

    # Проверяем что сообщение о регистрации не пустое
    # Чтобы избежать зависимости теста от языка
    assert success_message.text 
    print('Test #1 Sing Up passed')
