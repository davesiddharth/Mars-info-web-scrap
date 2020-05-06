from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission_to_Mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find records of data from the mongo database
    mars_data = mongo.db.mars_db.find_one()

    # Return template and data
    return render_template("index.html", data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_detail = scrape_mars.mars_news_scrape()
    mars_detail = scrape_mars.jpl_img_scrape()
    mars_detail = scrape_mars.mars_weather_scrape()
    mars_detail = scrape_mars.mars_facts_scrape()
    mars_detail = scrape_mars.mars_hemispheres_scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_db.update({}, mars_detail, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

