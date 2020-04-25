#import dependencies - Randy Dettmer - 2020/04/21
from flask import Flask, render_template, redirect

#import pymongo library
from flask_pymongo import PyMongo

#import scrape_mars as a scraping tool
import scrape_mars

#create an instance of our Flask app
app = Flask(__name__)

#create connection to mongo
conn = 'mongodb://localhost:27017'

#pass connection to the pymongo instance
client = pymongo.MongoClient(conn)

#connect to a database
db = client.mars_db

#drops collection if available to remove duplicates
db.mars.drop()

#this is test code and may not be necessary
import os 
from flask import send_from_directory     

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')




#creates a collection in the database
#db.mars.insert_many() - move???


#another test - - - - - - - - -

#from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
#import scrape_craigslist

#app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
#mongo = PyMongo(app)

#another test -- - - - - - - - - -


@app.route('/')
def index():
    #store mars data into list
    mars1 = list(db.mars.find())
    print(mars1)

    #return the template with list passed index
    return render_template('index.html', mars1=mars1)

if __name__ == "__main__":
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
    
    
