# Skimmer

## Development
I needed to make a script that would parse through and sort my credit card statements. I use credit cards from different companies, so the data is formatted differently. My mother has been kind enough to let me put some of her expenses on my cards so I can get cashback on them. So long as I send her itemized reports at the end of each month, she pays me back

## Description
This script pulls data from csv files downloaded from my credit cards' websites and organizes them. It then asks me if I need to bill my mom for them or not and generates a report.

## Usage
 - Load raw csv files in `tmp/`
 - Run with `python skimmer.py`
 - Store old reports in `prev.csv`
