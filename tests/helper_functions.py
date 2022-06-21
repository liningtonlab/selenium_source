from distutils.log import error
from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def switch_contig_tab(driver, curr_tab, is_forward):
    if is_forward:
        direction = "forward"
    else:
        direction = "backward"

    try:
        if is_forward:
            driver.switch_to.window(driver.window_handles[curr_tab+1])
            curr_tab += 1
        elif is_forward is False:
            driver.switch_to.window(driver.window_handles[curr_tab-1])
            curr_tab -= 1
    except IndexError:
        return curr_tab, f"No {direction} tab exists."

    return curr_tab, f"Success"

def search_doi(driver, doi):
    try:
        search_bar = driver.find_element(By.ID, "fname")
    except NoSuchElementException:
        assert False, f"Can't find Search Bar"
    
    search_bar.send_keys(doi)

    try:
        search_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[1]/div[2]/div/div/div[2]/div/div[2]/button")
    except NoSuchElementException:
        assert False, "Can't find Search Button"

    search_button.click()

    WebDriverWait(driver, 30).until(EC.url_changes("https://dev-npa-articles.liningtonlab.org/"))

    assert driver.current_url.startswith("https://dev-npa-articles.liningtonlab.org/submission/"), f"Current URL is {driver.current_url}"
    return driver.current_url

def nav_bar(driver, page_url):

    def deposit_new_article_button(driver, starting_url):

        assert starting_url == driver.current_url, "starting_url has diverged from driver.current_url"

        try:
            deposit_new_article = driver.find_element(By.LINK_TEXT, "Deposit New Article")
        except NoSuchElementException:
            assert False, f"Can't find 'Deposit New Article' button."

        deposit_new_article.click()
        assert driver.current_url == 'https://dev-npa-articles.liningtonlab.org/', "Deposit New Article click failed."

    def instruction_button(driver, starting_url, curr_tab_index):

        assert starting_url == driver.current_url, "starting_url has diverged from driver.current_url"

        # find the element and verify it is the correct one
        try:
            instruction = driver.find_element(By.LINK_TEXT, "Instruction")
        except NoSuchElementException as exc:
            assert False, f"Can't find 'Instruction' button {exc}"
        assert instruction.get_attribute("href") == "https://liningtonlab.github.io/article-pipeline-docs/"

        # click the element and then switch to the new opened tab to check the url is correct. Then switch back
        instruction.click()

        curr_tab_index, tab_error_msg = switch_contig_tab(driver, curr_tab_index, is_forward=True)
        assert driver.current_url == 'https://liningtonlab.github.io/article-pipeline-docs/', f"Instruction click returned unexpected URL. Tab switch was {tab_error_msg}"

        curr_tab_index, tab_error_msg = switch_contig_tab(driver, curr_tab_index, is_forward=False)
        assert driver.current_url == starting_url, f"Failed to switch back to homepage. Tab switch was {tab_error_msg}"


    def contact_us_button(driver):
        try:
            contact_us = driver.find_element(By.LINK_TEXT, "Contact Us")
        except NoSuchElementException as exc:
            assert False, f"Can't find 'Contact Us' button {exc}"


    driver.get(page_url)
    deposit_new_article_button(driver, page_url)
    instruction_button(driver, page_url, 0)
    contact_us_button(driver)



    




    

    




 
