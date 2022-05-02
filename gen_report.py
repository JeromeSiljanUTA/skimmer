import pandas as pd
import sqlite3
import openpyxl

def generate():
    connection = sqlite3.connect('main.db')
    cursor = connection.cursor()

    months_df = {}

    months = [['01','January'], ['02','February'], ['03','March'], ['04','April'], ['05','May'], ['06','June'], ['07','July'], ['08','August'], ['09','September'], ['10','October'], ['11','November'], ['12','December']]

    with pd.ExcelWriter('reports/2022 Report.xlsx') as writer:
        for month in range (12):
            command = 'SELECT Date, Name, Amount, Category, Card FROM main WHERE ID IN (SELECT ID FROM info WHERE TAGS="Mom") AND Date BETWEEN "2022-'
            command += months[month][0]
            command += '-01" AND "2022-'
            command += months[month][0]
            command += '-31"'
            months_df[month] = pd.read_sql(command, connection)
            months_df[month].to_excel(writer, sheet_name = months[month][1], index=False)
