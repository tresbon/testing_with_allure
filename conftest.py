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

    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='en',
                     help="Choose language")
    
    parser.addoption('--product_page', action='store',
                    default='http://selenium1py.pythonanywhere.com/' + \
                        'en-gb/catalogue/the-city-and-the-stars_95/',
                     help="Choose_product_link")

@pytest.fixture(scope="function")
def browser(request):

    browser_name = request.config.getoption("browser_name")

    lang = request.config.getoption("language")

    browser = None

    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        #Подлкючить языковые опции в хром
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': lang})
        browser = webdriver.Chrome()
        browser.maximize_window()

    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        #Подключить языковые опции в Firefox
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", lang)
        browser = webdriver.Firefox()
        browser.maximize_window()

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser

    print("\nquit browser..")

    browser.quit()

@pytest.fixture(scope="function")
def lang(request):

    lang = request.config.getoption("language")

    if lang in laguages_list:
        return lang
        
    else:
        return f'--language should by one of {laguages_list}'

@pytest.fixture(scope="function")
def push_by(request):
    return By

@pytest.fixture(scope="function")
def product_link(request):
    return request.config.getoption("product_page")