from flask import Flask, render_template

#import pymongo library
frpm flask_pymongo import PyMongo

#import scrape_mars
import scrape_mars

#create an instance of our Flask app
app = Flask(__name__)

#create connection to mongo
conn = 'mongodb://localhost:27017'

#pass clonnectin to the pymong instance
client = pymongo.MongoClient(conn)

#connect to a database
db = client.mars_db

#drops collection if available to remove duplicates
db.mars.drop()

#creates a collection in the database
#db.mars.insert_many() - move???

@app.route('/')
def index():
    #store mars data into list
    mars1 = list(db.mars.find())
    print(mars1)

    #retrun the template with list passed index
    retrun render_template('index.html', mars1=mars1)

if__name__="__main__":
    app.run(debug=True)

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
    
    
