# Skimmer
What started off as a simple way to gather data from various csv files is now becoming a (somewhat) full-fledged finance manager. This project used python pandas and sqlite to arrange and sort through data. 

At this point, it has a cli interface that I use to manage my accounts. This is good enough for me, so I think I'll leave this project as it is. This was my first time using SQL and I think it was a great learning experience. I think soon enough I'll work with matplotlib to help me visualize the data. 

## Description
This script pulls data from csv files downloaded from my credit cards' websites and organizes them. It then asks me if I need to bill my mom for them or not and generates a report.

## Usage
 - Load raw csv files in `tmp/`
 - Run with `python skimmer.py`
 - Data stored in 'main.db'

## Initial Purpose
I needed to make a script that would parse through and sort my credit card statements. I use credit cards from different companies, so the data is formatted differently. My mother has been kind enough to let me put some of her expenses on my cards so I can get cashback on them. So long as I send her itemized reports at the end of each month, she pays me back
