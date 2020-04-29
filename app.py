#import dependencies - Randy Dettmer - 2020/04/21
from flask import Flask, render_template, redirect, send_from_directory
from flask_pymongo import PyMongo
import os

#import scrape_mars as a scraping tool
import scrape_mars

#create an instance of our Flask app
app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/app"
mongo = PyMongo(app)

#home route
@app.route("/")
def home():
    #store mars data into list
    mars = mongo.db.mars.find_one()
    #return the template with list passed index
    return render_template('index.html', mars=mars)

#route that will scrape
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    #pull data from sites using scrape_mars.py
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    #redirect back to home page
    return redirect("/", code=302)

#added to correct and or prevent favicon error
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#end of file
if __name__ == "__main__":
    app.run(debug=True)