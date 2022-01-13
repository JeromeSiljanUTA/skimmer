from datetime import timedelta, datetime
import pandas as pd

prev = pd.read_csv("dummy1.csv")
current = pd.read_csv("dummy2.csv")

comb = prev.append(current)

print(prev)
print(current)
print(comb)

unique = comb.drop_duplicates(subset = ["Date", "Amount"], keep = False)

print(unique)
