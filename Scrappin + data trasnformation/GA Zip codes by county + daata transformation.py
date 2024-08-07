''' 
Created By David Camelo on 08/01/2024
'''

#Code to extract GA zip codes for Sales tax report
# Import necessary libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

# URL of the website containing Georgia zip codes
zip_GA_codes = "https://www.zip-codes.com/state/ga.asp"

# Headers to mimic a browser visit (required for some websites to allow scraping)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Send an HTTP GET request to the website
zips = requests.get(zip_GA_codes, headers=header)

# Check the response status code (for debugging purposes)
#print(zips)

# Parse the HTML content of the response
soup = bs(zips.text, "html.parser")

# Find the specific table containing the zip codes using its class attribute
table = soup.find("table", {"class": "statTable"})

# Convert the HTML table to a pandas DataFrame
table = pd.read_html(str(table))[0]

#Review Table to verify quality
#table

# Drop the last column (index 3) which is not needed
table = table.drop(3, axis=1)

# Since the resulting table has extra header rows, assign the correct header row
table.columns = table.iloc[0]  # Assign the new headers
table = table[1:].reset_index(drop=True)  # Drop unnecessary rows and reset the index

# Print a sample of the table to review (for debugging purposes)
# print(table)

"""
Cell generated by Data Wrangler.
"""

def clean_data(table):
    # Split text using string 'ZIP Code' in column: 'ZIP Code'
    loc_0 = table.columns.get_loc('ZIP Code')
    table_split = table['ZIP Code'].str.split(pat='ZIP Code', expand=True).add_prefix('ZIP Code_')
    table = pd.concat([table.iloc[:, :loc_0], table_split, table.iloc[:, loc_0:]], axis=1)
    table = table.drop(columns=['ZIP Code'])
    # Drop column: 'ZIP Code_0'
    table = table.drop(columns=['ZIP Code_0'])
    # Rename column 'ZIP Code_1' to 'ZIP code'
    table = table.rename(columns={'ZIP Code_1': 'ZIP code'})
    # Replace all instances of "Dekalb" with "DeKalb" in column: 'County'
    table['County'] = table['County'].str.replace("Dekalb", "DeKalb", case=False, regex=False)
    # Replace all instances of "Mcintosh" with "McIntosh" in column: 'County'
    table['County'] = table['County'].str.replace("Mcintosh", "McIntosh", case=False, regex=False)
    # Replace all instances of "Mcduffie" with "McDuffie" in column: 'County'
    table['County'] = table['County'].str.replace("Mcduffie", "McDuffie", case=False, regex=False)
    return table

table_clean = clean_data(table.copy())
# Save the cleaned table into a CSV file
table_clean.to_csv("GA_zip_codes_by_county.csv", index=False)
