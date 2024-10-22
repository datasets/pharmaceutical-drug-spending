import csv
import urllib.request

# URL of the population data
url = 'https://raw.githubusercontent.com/datasets/population/refs/heads/main/data/population.csv'

# Fetching the data from the URL
with urllib.request.urlopen(url) as response:
    data = response.read().decode('utf-8')

# Split the content into lines
lines = data.splitlines()

# Open the CSV file for writing
with open("archive/population.csv", "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    
    # Write the data rows
    for line in csv.reader(lines):
        writer.writerow(line)
