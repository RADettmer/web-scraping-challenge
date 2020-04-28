#load dependencies - Randy Dettmer 2020/04/28
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

#set browser to Chrome
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

#create scrape dictionary
def scrape():
    data = {}
    text = scrape_info()
    wdata = scrape_weather()
    data['news_title'] = text[0]
    data['news_p'] = text[1]
    data['featured_image_url'] = scrape_image()
    data['max_temp'] = wdata[0]
    data['avg_temp'] = wdata[1]
    data['min_temp'] = wdata[2]
    data['max_ws'] = wdata[3]
    data['avg_ws'] = wdata[4]
    data['min_ws'] = wdata[5]
    data['direction'] = wdata[6]
    data['max_p'] = wdata[7]
    data['avg_p'] = wdata[8]
    data['min_p'] = wdata[9]
    data['mars_facts'] = scrape_facts()
    data['hemisphere_image_urls'] = scrape_hemisphere()
    return data

def scrape_info():
    
    #vist NASA mars web site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #delay if reading a lot of pages of a website to avoid being banned
    time.sleep(2)    
  
    #scrape page into soup
    html = browser.html
    soup = bs(html, "lxml")

    #get latest news title
    news_title = soup.find_all('div', class_='content_title')[1].title

    #get paragraph text
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    text = [news_title, news_p]
    return text

def scrape_image():
    # Visit JPL site for current Mars space image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "lxml")

    # Click on button to get full size image
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    
    # Find full image button and click it
    browser.is_element_not_present_by_text("more info", wait_time=1)
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()

    # Scrape the first Mars image
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

def scrape_weather():
    # Visit the Mars Weather from NASA - alternative site used to collect the weather information
    weather_url = "https://mars.nasa.gov/insight/weather/"
    browser.visit(weather_url)
    html = browser.html
    soup = bs(html, "lxml")
    
    #pull temperatures - max, avg, min
    w1 = soup.tbody.find_all("span", class_='fahrenheit')[0].text
    w2 = soup.tbody.find_all("span", class_='fahrenheit')[1].text
    w3 = soup.tbody.find_all("span", class_='fahrenheit')[2].text

    #pull wind info - max, avg, min, direction
    w4 = soup.tbody.find_all("span", class_='mph')[0].text
    w5 = soup.tbody.find_all("span", class_='mph')[1].text
    w6 = soup.tbody.find_all("span", class_='mph')[2].text
    w7 = soup.tbody.find("td", class_='windspeed point').text

    #pull pressure data - max, avg, min
    w8 = soup.tbody.find_all("td", class_='pressure max')[1].text
    w9 = soup.tbody.find_all("td", class_='pressure avg')[1].text
    w10 = soup.tbody.find_all("td", class_='pressure min')[1].text

    wdata = [w1,w2,w3,w4,w5,w6,w7,w8,w9,w10]
    return wdata

def scrape_facts():
    # Visit the Mars facts webpage
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    # Create pandas df with Mars facts - -
    # Index [2] returns the cleanest data
    df1 = pd.read_html("https://space-facts.com/mars/")[2]
    df1.columns=["Fact", "Value"]
    df1 = df1.set_index("Fact")
    df1 = df1.to_html(index = True, header = True)
    return df1

def scrape_hemisphere():
    # Visit the Mars hemispheres scrape images from the astrogeology.usgs site
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "lxml")

    # Create a dictionary to store data using the keys img_url and title
    hemisphere_image_urls = []
    # Results are returned as an iterable list
    results = soup.find_all("div",class_='item')

    # Loop through returned results
    for result in results:
        hemisphere = {}
        #identifiy title
        title = result.find('h3').text
        #identify image link
        key = result.find("a")["href"]
        #join link together
        link = "https://astrogeology.usgs.gov/" + key
        #       read link
        browser.visit(link)
        html = browser.html
        soup = bs(html, "lxml")
        #collect information for dictionary and append
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere['title']= title
        hemisphere['image_url']= image_url
        hemisphere_image_urls.append(hemisphere)

        return hemisphere_image_urls


#close brwser after scraping
browser.quit()