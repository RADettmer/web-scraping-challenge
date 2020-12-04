# load dependencies - Randy Dettmer 2020/04/30
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from selenium import webdriver

# set browser to Chrome
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# create scrape dictionary
def scrape():
    data = {}
   
# vist NASA mars web site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    #delay to make sure page loads
    time.sleep(2)    
  
    #scrape page into soup
    html = browser.html
    soup = bs(html, "lxml")

    #get latest news title
    data['news_title'] = soup.find_all('div', class_='content_title')[1].text

    #get paragraph text
    data['news_p'] = soup.find('div', class_='article_teaser_body').get_text()

# Visit JPL site for current Mars space image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    #delay to make sure page loads
    time.sleep(1)  

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
    data['featured_image_url'] = "https://www.jpl.nasa.gov" + image
    #return featured_image_url

# Visit the Mars Weather from NASA - alternative site used to collect the weather information
    weather_url = "https://mars.nasa.gov/insight/weather/"
    browser.visit(weather_url)

    #delay to make sure page loads
    time.sleep(1)  

    html = browser.html
    soup = bs(html, "lxml")
    
    #pull temperatures - max, avg, min
    data['max_temp'] = soup.tbody.find_all("span", class_='fahrenheit')[0].text
    data['avg_temp'] = soup.tbody.find_all("span", class_='fahrenheit')[1].text
    data['min_temp'] = soup.tbody.find_all("span", class_='fahrenheit')[2].text

    #pull wind info - max, avg, min, direction
    data['max_ws'] = soup.tbody.find_all("span", class_='mph')[0].text
    data['avg_ws'] = soup.tbody.find_all("span", class_='mph')[1].text
    data['min_ws'] = soup.tbody.find_all("span", class_='mph')[2].text
    data['direction'] = soup.tbody.find("td", class_='windspeed point').text

    #pull pressure data - max, avg, min
    data['max_p'] = soup.tbody.find_all("td", class_='pressure max')[1].text
    data['avg_p'] = soup.tbody.find_all("td", class_='pressure avg')[1].text
    data['min_p'] = soup.tbody.find_all("td", class_='pressure min')[1].text

# Visit the Mars facts webpage
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    #delay to make sure page loads
    time.sleep(1)  

    # Create pandas df with Mars facts - -
    # Index [2] returns the cleanest data
    df1 = pd.read_html("https://space-facts.com/mars/")[2]
    df1.columns=["Fact", "Value"]
    df1 = df1.set_index("Fact")
    df1 = df1.to_html(index = True, header = True)
    data['mars_facts'] = df1
    #return df1

# Visit the Mars hemispheres scrape images from the astrogeology.usgs site
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    #delay to make sure page loads
    time.sleep(1)  

    html = browser.html
    # I used lxml because it seemed I received more consistant responses over html.parser
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
        #read link
        browser.visit(link)
        html = browser.html
        soup = bs(html, "lxml")
        #collect information for dictionary and append
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere['title']= title
        hemisphere['image_url']= image_url
        hemisphere_image_urls.append(hemisphere)

        #return hemisphere_image_urls
    data['hemisphere_image'] = hemisphere_image_urls
    return data

#close browser after scraping - not needed
#browser.quit()