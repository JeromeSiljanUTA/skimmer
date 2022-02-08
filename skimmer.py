# Set
# Imports and Datetime
import pandas as pd
import os
import datetime
import sqlite3
from flask import Flask, render_template
date_time = datetime.datetime.now()

# Compiling and Cleaning Data
# Grabbing Files
import_dir = "tmp/"
reports_path = "reports/"
downloads = os.listdir(import_dir)

for file in downloads:
    if "3978" in file:
        altitude_path = import_dir + file
    elif "4859" in file:
        cashplus_path = import_dir + file
    elif "Discover" in file:
        discover_path = import_dir + file
    else:
        customcash_path = import_dir + file

def cleanup(customcash_path, altitude_path, cashplus_path, discover_path):
    # CustomCash Cleanup
    customcash = pd.read_csv(customcash_path)
    customcash["Date"] = pd.to_datetime(customcash["Date"]).dt.date
    customcash = customcash[~(customcash["Description"].str.contains("THANK YOU"))]
    customcash["Debit"].fillna(customcash.Credit, inplace = True)
    customcash["Category"] = "Gas Stations"
    customcash["Card"] = "Citi Custom Cash"
    customcash = (customcash.drop(columns = ["Credit", "Status"])
            .rename(columns = {"Description":"Name", "Debit":"Amount"})
         )

    # Altitude Cleanup
    altitude = pd.read_csv(altitude_path, usecols = ["Amount", "Name", "Date"])
    altitude["Date"] = pd.to_datetime(altitude["Date"]).dt.date
    altitude = altitude[~(altitude["Name"].str.contains("THANK YOU"))]
    altitude["Amount"] = altitude["Amount"] * -1
    altitude["Category"] = "Restaurants"
    altitude["Card"] = "USbank Altitude"

    # CashPlus Cleanup
    cashplus = pd.read_csv(cashplus_path, usecols = ["Amount", "Name", "Date"])
    cashplus["Date"] = pd.to_datetime(cashplus["Date"]).dt.date
    cashplus = cashplus[~(cashplus["Name"].str.contains("THANK YOU"))]
    cashplus["Amount"] = cashplus["Amount"] * -1
    cashplus["Category"] = ""
    cashplus["Card"] = "USbank CashPlus"

    # Discover Cleanup
    discover = (pd.read_csv(discover_path, usecols = ["Trans. Date", "Amount", "Description", "Category"])
                  .rename(columns = {"Trans. Date":"Date", "Description":"Name"})
                )
    discover["Date"] = pd.to_datetime(discover["Date"]).dt.date
    discover = discover[~(discover["Name"].str.contains("THANK YOU"))]
    discover["Card"] = "Discover It"

    # combine 
    comb = altitude.append(cashplus).append(discover).append(customcash)
    comb.sort_values("Date", inplace = True)
    comb.reset_index(drop = True, inplace = True)

    return comb

# Getting Previous
main = cleanup(customcash_path, altitude_path, cashplus_path, discover_path)
main.fillna("", inplace = True)

# Insert New
# SQL Setup
connection = sqlite3.connect('main.db')
cursor = connection.cursor()

main.to_sql('new', connection, if_exists = 'replace', index = False)

# Add Unique Values to main
cursor.execute('INSERT INTO main(Date, Name, Amount, Category, Card) SELECT * FROM (SELECT Date, Name, Amount, Category, Card FROM main UNION ALL SELECT Date, Name, Amount, Category, Card FROM new) GROUP BY Date, Name, Amount, Category, Card HAVING COUNT(1) = 1;')

connection.commit()

connection.close()

def find_tagless():
    connection = sqlite3.connect('main.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM main WHERE ID NOT IN (SELECT ID FROM info WHERE tags != "")');
    print('These entries don\'t have tags');
    raw_tagless = cursor.fetchall()

    tagless = []

    for entry in raw_tagless:
        tagless.append({"ID": str(entry[0]),
                        "Date": str(entry[1]),
                        "Name": str(entry[2]),
                        "Amount": str(entry[3]),
                        "Category": str(entry[4]),
                        "Card": str(entry[5])})

    connection.close()
    return tagless

# Flask Setup
app = Flask(__name__, template_folder='web_testing')

@app.route('/')
def main_page():
    tagless = find_tagless()
    print(tagless)
    return render_template('index.html', data=tagless)

@app.route('/add_tag', methods = ['POST'])
def add_tag():
    input_text = request.form['uname']
    print(uname)

if __name__ == "__main__":
    app.run()

