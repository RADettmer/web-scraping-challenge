#load dependencies - Randy Dettmer 2020/04/19

from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
    #note
    excutable_path = {"excutable_path": "url/locatl/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {} #updated name of this variable??

    url = "https//????fill-this-in" #update this url
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser") #change to xtml?? parcer?

    listings[] = soup.find("", class="").get_text()

    return listings

#end of file
