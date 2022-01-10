import pandas as pd
import os
import datetime

date_time = datetime.datetime.now()

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

os.rename(altitude_path, "altitude.csv")
os.rename(cashplus_path, "cashplus.csv")
os.rename(discover_path, "discover.csv")

altitude_path = "altitude.csv"
cashplus_path = "cashplus.csv"
discover_path = "discover.csv"
prev_comb_path = "combined.csv"

# Read files
altitude = pd.read_csv(altitude_path)
cashplus = pd.read_csv(cashplus_path)
discover = pd.read_csv(discover_path)
prev_comb = pd.read_csv(prev_comb_path)

# Drop & Rename columns
altitude.drop(columns = ["Memo", "Transaction"], inplace = True)
cashplus.drop(columns = ["Memo", "Transaction"], inplace = True)
discover.drop(columns = "Post Date", inplace = True)

altitude["Category"] = "Restaurants"
cashplus["Category"] = ""
discover.rename(columns = {"Trans. Date":"Date", "Description":"Name"}, inplace = True)

# Adjust column values
altitude["Amount"] = altitude["Amount"] * -1
cashplus["Amount"] = cashplus["Amount"] * -1

# Drop payments
altitude = altitude[~(altitude["Name"].str.contains("THANK YOU"))]
cashplus = cashplus[~(cashplus["Name"].str.contains("THANK YOU"))]
discover = discover[~(discover["Name"].str.contains("THANK YOU"))]

# combine 
comb1 = altitude.append(cashplus)
comb = comb1.append(discover)

comb["Date"] = pd.to_datetime(comb["Date"])

comb.sort_values("Date", inplace = True)

comb.reset_index(drop = True, inplace = True)

last_entry = prev_comb.tail(1)

last_entry_date = prev_comb.tail(1).iat[0, 0]
last_entry_amount = prev_comb.tail(1).iat[0, 2]

target_index = comb[(comb.Date == last_entry_date) & (comb.Amount == last_entry_amount)].index.tolist()

comb = comb.iloc[target_index[0] + 1:]

mom_comb = comb.copy(deep = False)

for row in comb.iterrows():
        print("Did you spend " + "${:>5,.2f}".format(float(row[1].Amount)) + " on " + str(row[1].Date)[0:10] + " at " + str(row[1].Name) + "? ")
        if(input().lower() != ("n")):
            print("Adding to your expenses")
            mom_comb.drop(mom_comb[(mom_comb.Name == row[1].Name) & (mom_comb.Amount == row[1].Amount)].index.tolist(), inplace = True)
        else:
            comb.drop(comb[(comb.Name == row[1].Name) & (comb.Amount == row[1].Amount)].index.tolist(), inplace = True)

jerome_string = reports_path + date_time.strftime("%m-%d-%Y-") + "Jerome Report.csv"
mom_string = reports_path + date_time.strftime("%m-%d-%Y-") + "Mom Report.csv"

comb.to_csv(jerome_string, index = False)
mom_comb.to_csv(mom_string, index = False)

os.remove(altitude_path)
os.remove(cashplus_path)
os.remove(discover_path)
