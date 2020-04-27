#import dependencies - Randy Dettmer - 2020/04/21
from flask import Flask, render_template, redirect

#import pymongo library
from flask_pymongo import PyMongo

#import scrape_mars as a scraping tool
import scrape_mars

#create an instance of our Flask app
app = Flask(__name__)

#create connection to mongo
#conn = 'mongodb://localhost:27017'

#pass connection to the pymongo instance
#client = pymongo.MongoClient(conn)

#connect to a database
#db = client.mars_db

#drops collection if available to remove duplicates
#db.mars.drop()

#create connection to mongo
app.confi["MONGO_URI"] = "mongodb://localhost:27017/app"
mongo = PyMongo(app)

#this is test code and may not be necessary - - - - - testing 7
#import os 
#from flask import send_from_directory     

#@app.route('/favicon.ico') 
#def favicon(): 
    #return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#ending of testing 7


#home route
@app.route("/")
def index():
    #store mars data into list
    mars = mongo.db.mars.find_one()

    #return the template with list passed index
    return render_template('index.html', mars=mars)

#scrape route
@app.route("/scrape")
def scrapper():
    #test
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Completed"


#end of file
if __name__ == "__main__":
    app.run(debug=True)