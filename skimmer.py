# Imports and Datetime
import pandas as pd
import os
import csv
import datetime

date_time = datetime.datetime.now()

def cleanup(customcash_path, altitude_path, cashplus_path, discover_path):
    # CustomCash Cleanup
    customcash = pd.read_csv(customcash_path)
    customcash["Date"] = pd.to_datetime(customcash["Date"]).dt.date
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

# Grabbing Files
import_dir = "tmp/"
reports_path = "reports/"
downloads = os.listdir(import_dir)

for file in downloads:
    if "4808" in file:
        altitude_path = import_dir + file
    elif "5100" in file:
        cashplus_path = import_dir + file
    elif "Discover" in file:
        discover_path = import_dir + file
    else:
        customcash_path = import_dir + file

#prev_comb_path = "combined.csv"
#prev_comb = pd.read_csv(prev_comb_path)

# unique
#unique = comb.append(prev_comb)
#unique["Date"] = pd.to_datetime(unique["Date"]).dt.date
#unique.sort_values("Date", inplace = True)
#unique = comb.drop_duplicates(subset = ["Date", "Amount"], keep = False)
#unique.reset_index(drop = True, inplace = True)

comb = cleanup(customcash_path, altitude_path, cashplus_path, discover_path)

print(comb)
