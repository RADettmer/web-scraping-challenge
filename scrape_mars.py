#load dependencies - Randy Dettmer 2020/04/19
from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():
    #set browser to Chrome
    executable_path = {"excutable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {} #updated name of this variable??

    url = "https//????fill-this-in" #update this url
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser") #change to xtml?? parcer?
    #incomplete items below - need to be updated []? why?
    listings[] = soup.find("div", class="?").get_text()

    return listings

#end of file

#necessary????

def scrape_info():
    browser = init_browser()
    
    #vist NASA mars web site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #delay if reading a lot of pages of a website to avoid being banned
    #time.sleep(1)    
  
    #scrape page into soup
    html = browser.html
    soup = bs(html, "html.parser")
    #get latest news title
    news_title = soup.find('a', target='_self')
    
    
