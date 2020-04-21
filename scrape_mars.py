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

#necessary????

#set browser to Chrome - will this fix my problems???
def init_browser():
    executable_path = {"excutable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    
    #vist NASA mars web site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #delay if reading a lot of pages of a website to avoid being banned
    time.sleep(1)    
  
    #scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")
    #get latest news title
    news_title = soup.find('a', target='_self')
    
    
