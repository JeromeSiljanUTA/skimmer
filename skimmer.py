# Imports
import pandas as pd
import os
import csv
import datetime
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

date_time = datetime.datetime.now()

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

prev_comb_path = "combined.csv"
prev_comb = pd.read_csv(prev_comb_path)

# CustomCash Cleanup
#os.rename(customcash_path, "customcash.csv")
#customcash_path = "customcash.csv"
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
#os.rename(altitude_path, "altitude.csv")
#altitude_path = "altitude.csv"

altitude = pd.read_csv(altitude_path, usecols = ["Amount", "Name", "Date"])
altitude["Date"] = pd.to_datetime(altitude["Date"]).dt.date
altitude = altitude[~(altitude["Name"].str.contains("THANK YOU"))]
altitude["Amount"] = altitude["Amount"] * -1
altitude["Category"] = "Restaurants"
altitude["Tags"] = ""
altitude["Card"] = "USbank Altitude"

# CashPlus Cleanup
#os.rename(cashplus_path, "cashplus.csv")
#cashplus_path = "cashplus.csv"
cashplus = pd.read_csv(cashplus_path, usecols = ["Amount", "Name", "Date"])
cashplus["Date"] = pd.to_datetime(cashplus["Date"]).dt.date
cashplus = cashplus[~(cashplus["Name"].str.contains("THANK YOU"))]
cashplus["Amount"] = cashplus["Amount"] * -1
cashplus["Category"] = ""
cashplus["Tags"] = ""
cashplus["Card"] = "USbank CashPlus"

# Discover Cleanup
#os.rename(discover_path, "discover.csv")
#discover_path = "discover.csv"
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

# unique
unique = comb.append(prev_comb)
unique["Date"] = pd.to_datetime(unique["Date"]).dt.date
unique.sort_values("Date", inplace = True)
unique = comb.drop_duplicates(subset = ["Date", "Amount"], keep = False)
unique.reset_index(drop = True, inplace = True)

print(unique)

#unique.to_csv("newcomb.csv")

"""

prev_comb = unique.append(mom_comb)

mom_comb = unique.copy()

for row in unique.iterrows():
        print("Did you spend " + "${:>5,.2f}".format(float(row[1].Amount)) + " on " + str(row[1].Date)[0:10] + " at " + str(row[1].Name) + "? ")
        if(input().lower() != ("n")):
            print("Adding to your expenses")
            mom_comb.drop(mom_comb[(mom_comb.Name == row[1].Name) & (mom_comb.Amount == row[1].Amount)].index.tolist(), inplace = True)
        else:
            unique.drop(unique[(unique.Name == row[1].Name) & (unique.Amount == row[1].Amount)].index.tolist(), inplace = True)

jerome_string = reports_path + date_time.strftime("%m-%d-%Y-") + "Jerome Report.csv"
mom_string = reports_path + date_time.strftime("%m-%d-%Y-") + "Mom Report.csv"

unique.to_csv(jerome_string, quoting = csv.QUOTE_NONNUMERIC, index = False)
mom_comb.to_csv(mom_string, quoting = csv.QUOTE_NONNUMERIC, index = False)

prev_comb.to_csv(prev_comb_path, quoting = csv.QUOTE_NONNUMERIC, index = False)

#os.remove(altitude_path)
#os.remove(cashplus_path)
#os.remove(discover_path)
"""
