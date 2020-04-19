from flask import Flask, render_template

#import pymongo library
import pymongo

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
