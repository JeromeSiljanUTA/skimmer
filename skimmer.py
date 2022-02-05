# Imports and Datetime
import pandas as pd
import os
import csv
import datetime

date_time = datetime.datetime.now()

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

prev = pd.read_csv("prev.csv")

def cleanup(customcash_path, altitude_path, cashplus_path, discover_path):
    # CustomCash Cleanup
    customcash = pd.read_csv(customcash_path)
    customcash["Date"] = pd.to_datetime(customcash["Date"]).dt.date
    customcash = customcash[~(customcash["Description"].str.contains("THANK YOU"))]
    customcash["Debit"].fillna(customcash.Credit, inplace = True)
    customcash["Category"] = "Gas Stations"
    customcash["Tags"] = ""
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
    altitude["Tags"] = ""
    altitude["Card"] = "USbank Altitude"

    # CashPlus Cleanup
    cashplus = pd.read_csv(cashplus_path, usecols = ["Amount", "Name", "Date"])
    cashplus["Date"] = pd.to_datetime(cashplus["Date"]).dt.date
    cashplus = cashplus[~(cashplus["Name"].str.contains("THANK YOU"))]
    cashplus["Amount"] = cashplus["Amount"] * -1
    cashplus["Category"] = ""
    cashplus["Tags"] = ""
    cashplus["Card"] = "USbank CashPlus"

    # Discover Cleanup
    discover = (pd.read_csv(discover_path, usecols = ["Trans. Date", "Amount", "Description", "Category"])
                  .rename(columns = {"Trans. Date":"Date", "Description":"Name"})
                )
    discover["Date"] = pd.to_datetime(discover["Date"]).dt.date
    discover = discover[~(discover["Name"].str.contains("THANK YOU"))]
    altitude["Tags"] = ""
    discover["Card"] = "Discover It"

    # combine 
    comb = altitude.append(cashplus).append(discover).append(customcash)
    comb.sort_values("Date", inplace = True)
    comb.reset_index(drop = True, inplace = True)

    return comb

# Getting Previous
main = cleanup(customcash_path, altitude_path, cashplus_path, discover_path)
main["Mine"] = ""
main = main.append(prev)
main["Date"] = main["Date"].astype(str)
main.drop_duplicates(subset = ["Date", "Name", "Amount"], keep = False, ignore_index = True, inplace = True)

print(main)

#main.to_csv("prev.csv", index = False)

# Magic Number: 50
