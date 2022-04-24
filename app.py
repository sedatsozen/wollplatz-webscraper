from flask import Flask, render_template, request
from Database import Database
from flask_wtf import FlaskForm
from wtforms import SelectField
from Scraper import Scraper

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

#root_url = "https://www.wollplatz.de/wolle/herstellers" #Starting point for scraping
#scraper = Scraper(url=root_url) #Initialize using __init() method

# manufacturers = scraper.get_elements_by_tag("h2") #In the root page manufacturer names are represented as h2 tags
# yarns_from_manufacturers = [] #Create empty list to append values later
#
# for manufacturer in manufacturers: #Iterate through every manufacturer one by one
#     yarns_from_manufacturers.append(scraper.get_yarns_by_manufacturer(manufacturer)) #Append every yarn with specs
#     scraper.go_to_root() #When every yarn of a manufacturer is searched, go back to root

# result = yarns_from_manufacturers #The list containing every single yarn with specs
# print(result)

#The code above is commented because the yarns are saved into a database after the first execution of the code. It is not needed to be run again.
#But if the "yarns.txt" file is deleted, the code above can be run again to get the same file

database = Database("yarns.txt") #Create database from custom database class
database.insert_csv_into_database() #CSV formatted yarns are saved to a SQLite database

every_value = database.get_data(hersteller="All", nadelstaerke="All") #For filtering, every manufacturer and needle size is saved separately
nadelstaerke_list = []
hersteller_list = []

for i in every_value:
    hersteller_list.append(i[0])
    nadelstaerke_list.append(i[4])

hersteller_list.append("All")
nadelstaerke_list.append("All")

hersteller_list = list(dict.fromkeys(hersteller_list))
nadelstaerke_list = list(dict.fromkeys(nadelstaerke_list))

yarns = database.get_data(hersteller="All", nadelstaerke="All") #Get every yarn without any filter

table_headings = ("Hersteller", "Name", "Preis", "Lieferzeit", "Nadelstaerke", "Zusammenstellung") #Headers for tables

class Form(FlaskForm): #For filtering "select" fields
    hersteller = SelectField("Hersteller", choices=hersteller_list) #Template from WTForms
    nadelstaerke = SelectField("Nadelstaerke", choices=nadelstaerke_list) #Template from WTForms

@app.route('/', methods=["GET", "POST"])
def hello_world():  # put application's code here
    form = Form() #Initialize forms
    if request.method == "POST":
        filtered_yarns = database.get_data(hersteller=form.hersteller.data, nadelstaerke=form.nadelstaerke.data) #Get values of the select fields
        return render_template("table.html", headings=table_headings, data=filtered_yarns, form=form) #Render the html file according to the select field values

    return render_template("table.html", headings=table_headings, data=yarns, form=form) #First, show every yarn


if __name__ == '__main__':
    app.run()
