"""
Created By David Camelo on 08/01/2024
"""

# Code to extract GA zip codes for Sales tax report
# Import necessary libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

# URL of the website containing Georgia zip codes
zip_GA_codes = "https://www.zipcodestogo.com/Georgia/"

# Headers to mimic a browser visit (required for some websites to allow scraping)
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Send an HTTP GET request to the website
zips = requests.get(zip_GA_codes, headers=header)

# Check the response status code (for debugging purposes)
# print(zips)

# Parse the HTML content of the response
soup = bs(zips.text, "html.parser")

# Find the specific table containing the zip codes using its class attribute
table = soup.find("table", {"class": "inner_table"})

# Convert the HTML table to a pandas DataFrame
table = pd.read_html(str(table))[0]

# Drop the last column (index 3) which is not needed
table = table.drop(3, axis=1)

# Since the resulting table has extra header rows, assign the correct header row
table.columns = table.iloc[1]  # Assign the new headers
table = table[2:].reset_index(drop=True)  # Drop unnecessary rows and reset the index

# Print a sample of the table to review (for debugging purposes)
# print(table)

# Save the cleaned table into a CSV file
table.to_csv("GA_zip_codes_by_county.csv", index=False)
