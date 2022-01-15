# Imports
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

# Custom Cash Cleanup
os.rename(customcash_path, "customcash.csv")
customcash_path = "customcash.csv"
customcash = pd.read_csv(customcash_path)

print(Customcash)

# Altitude Cleanup
os.rename(altitude_path, "altitude.csv")
altitude_path = "altitude.csv"
altitude = pd.read_csv(altitude_path)
altitude.drop(columns = ["Memo", "Transaction"], inplace = True)
altitude = altitude[~(altitude["Name"].str.contains("THANK YOU"))]
altitude["Amount"] = altitude["Amount"] * -1
altitude["Category"] = "Restaurants"
altitude["Card"] = "USbank Altitude"

# Discover Cleanup
discover_path = "discover.csv"
os.rename(discover_path, "discover.csv")
discover = pd.read_csv(discover_path)
discover.drop(columns = "Post Date", inplace = True)
discover.rename(columns = {"Trans. Date":"Date", "Description":"Name"}, inplace = True)
discover = discover[~(discover["Name"].str.contains("THANK YOU"))]
discover["Card"] = "Discover It"

# CashPlus Cleanup
os.rename(cashplus_path, "cashplus.csv")
cashplus_path = "cashplus.csv"
cashplus = pd.read_csv(cashplus_path)
cashplus.drop(columns = ["Memo", "Transaction"], inplace = True)
cashplus = cashplus[~(cashplus["Name"].str.contains("THANK YOU"))]
cashplus["Amount"] = cashplus["Amount"] * -1
cashplus["Category"] = ""
cashplus["Card"] = "USbank CashPlus"


"""
# combine 
comb = altitude.append(cashplus).append(discover)

comb["Date"] = pd.to_datetime(comb["Date"])
comb.sort_values("Date", inplace = True)
comb.reset_index(drop = True, inplace = True)


unique = comb.append(prev_comb)
unique = comb.drop_duplicates(subset = ["Date", "Amount"], keep = False)

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
