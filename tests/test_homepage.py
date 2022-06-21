from distutils.log import error
from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from .helper_functions import nav_bar, search_doi

input_doi_list = ["10.1021/acs.jnatprod.0c00283", ]

@pytest.mark.parametrize("input_doi", input_doi_list)
def test_homepage(input_doi):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_driver  = webdriver.Chrome(options=chrome_options)
    
    # look for the navbar and test it
    nav_bar(driver=chrome_driver, page_url="https://dev-npa-articles.liningtonlab.org/")

    # look for the search bar
    search_doi(driver=chrome_driver, doi=input_doi)
    
    # assert submission_link == chrome_driver.current_url
