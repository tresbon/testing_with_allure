import pytest
from lxml import etree
import re
from requests import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_langs():
    '''Get list of langs'''

    root = etree.fromstring(request('GET',\
        'http://selenium1py.pythonanywhere.com/sitemap.xml'\
            ).content)

    langs = [re.search('(?<=categories-)[\w-]{2,5}(?=.xml)',\
        i[0].text, re.IGNORECASE).group() for i in root if \
        re.search('(?<=categories-)[\w-]{2,5}(?=.xml)', \
            i[0].text, re.IGNORECASE) ]

    langs.sort()

    return langs

laguages_list = get_langs()

def pytest_addoption(parser):

    parser.addoption('--browser', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='en',
                     help="Choose language")

@pytest.fixture(scope="function")
def driver(request):

    browser = request.config.getoption("browser")

    lang = request.config.getoption("language")

    driver = None

    if browser.lower() == "chrome":
        print("\nstart chrome browser for test..")
        #Подлкючить языковые опции в хром
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': lang})
        driver = webdriver.Chrome()
        driver.maximize_window()

    elif browser.lower() == "firefox":
        print("\nstart firefox browser for test..")
        #Подключить языковые опции в Firefox
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", lang)
        driver = webdriver.Firefox()
        driver.maximize_window()

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield driver

    print("\nquit browser..")

    driver.quit()

@pytest.fixture(scope="function")
def lang(request):

    lang = request.config.getoption("language")

    if lang in laguages_list:
        return lang
        
    else:
        return f'--language should by one of {laguages_list}'
