from lxml import html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests as req
import urllib.request
import time
from bs4 import BeautifulSoup

class Scraper:
    def scrape(self):
        url = 'https://mangarock.com/manga/latest'

        response = req.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        for tag in soup.find_all("script"):
            print(tag)

        #print(soup.prettify())

# driver = webdriver.Chrome()S
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found" not in driver.page_source
# driver.close()

s = Scraper()
s.scrape()