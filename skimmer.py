# Set
# Imports and Datetime
import pandas as pd
import os
import datetime
import sqlite3
date_time = datetime.datetime.now()

# Compiling and Cleaning Data
# Grabbing Files
import_dir = "tmp/"
downloads = os.listdir(import_dir)

for file in downloads:
    if "4808" in file:
    #if "3978" in file:
        altitude_path = import_dir + file
    elif "5100" in file:
    #elif "4859" in file:
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
connection = sqlite3.connect('tester.db')
cursor = connection.cursor()

#main.to_sql('new', connection, if_exists = 'replace', index = False)

# Add Unique Values to main
#cursor.execute('INSERT INTO main(Date, Name, Amount, Category, Card) SELECT * FROM (SELECT Date, Name, Amount, Category, Card FROM main UNION ALL SELECT Date, Name, Amount, Category, Card FROM new) GROUP BY Date, Name, Amount, Category, Card HAVING COUNT(1) = 1;')

all_rows = main.iterrows()

for row in all_rows:
    row = row[1]
    date = '"' + str(row[0]) + '", '
    name = '"' + str(row[1]) + '", '
    amount = '"' + str(row[2]) + '", '
    category = '"' + str(row[3]) + '", '
    card = '"' + str(row[4]) + '"'
    #print('INSERT INTO main(Date, Name, Amount, CAtegory, Card) VALUES (' + date + name + amount + category + card + ');')
    try:
        cursor.execute('INSERT INTO main(Date, Name, Amount, CAtegory, Card) VALUES (' + date + name + amount + category + card + ');')
    except sqlite3.IntegrityError:
        #print(date + name + amount + category + card + ' is a duplicate entry')
        print(name + ' is duplicate')

connection.commit()

connection.close()

# Merchant Dictionary
merchant_dict = {
        "walmart":"Walmart",
        "patel brothers":"Patel Brothers",
        "amazon":"Amazon",
        "jcpenney":"JCPenney",
        "mcdonald":"McDonald's",
        "buffalo wild wings":"Buffalo Wild Wings",
        "family dollar":"Family Dollar",
        "chick-fil-a":"Chick-fil-a",
        "chickfil a":"Chick-fil-a",
        "wendy's":"Wendy's",
        "amzn":"Amazon",
        "in n out":"In N Out",
        "ihop":"IHOP",
        "six flags":"Six Flags",
        "panda":"Panda Express",
        "waffle house":"Waffle House",
        "starbucks":"Starbucks",
        "walgreens":"Walgreens",
        "wingstop":"Walgreens",
        "fuzzy taco":"Fuzzy Taco Shop"
}

def find_tagless():
    connection = sqlite3.connect('tester.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM main WHERE ID NOT IN (SELECT ID FROM info)');
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

def add_merchant(raw):
    raw_lower = raw.lower()
    for merchant in merchant_dict:
        if(merchant in raw_lower):
            return merchant_dict[merchant]

    return raw

def add_tags(tagless):
    connection = sqlite3.connect('tester.db')
    cursor = connection.cursor()

    for entry in tagless:
        prompt = ('Was the purchase on ' + entry['Date'] 
                + ' for ' + entry['Amount'] 
                + ' called ' + entry['Name'] 
                + ' yours? ')
        mine = (input(prompt)).lower()

        if(mine == 'yes' or mine == 'y'):
            cleaned = add_merchant(entry['Name'])
            if(cleaned != entry['Name']):
                merchant = cleaned
            else:
                merchant = input('Enter merchant name: ')

            notes = input('Enter notes: ')
            tags = input('Enter tags: ')
            cursor.execute('INSERT INTO info(ID, Merchant, Notes, Tags) VALUES(' + entry["ID"] + ', "' + merchant + '", "' + notes + '", "' + tags + '")')
        elif(mine == 'c'):
            """
            cursor.execute('select Date, Name, Amount, Category, info.Tags, Card, Notes from main join info on main.ID = info.ID')
            for row in cursor:
                print(row)
                """
            connection.commit()
        else:
            cursor.execute('INSERT INTO info(ID, Tags) VALUES("' + entry['ID'] + '", "Mom")')


    connection.commit()
    connection.close()

tagless = find_tagless()
add_tags(tagless)

"""
if((input('Would you like to generate reports? ').lower()) == 'yes' or 'y'):
    os.system('gen_report.py')
    print("Success: Reports generated!")
else:
    print("No reports generated")
"""
