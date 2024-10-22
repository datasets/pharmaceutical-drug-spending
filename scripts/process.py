import csv
import urllib.request

sources = ["https://stats.oecd.org/sdmx-json/data/DP_LIVE/.PHARMAEXP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en"]
data = 'archive/pharma-spending.csv'

def pharma_spending_all():
    for s in sources:
        urllib.request.urlretrieve(s, data)

def usd_per_cap():
    with open('archive/pharma-spending.csv', 'r') as inp, open('archive/usd-cap.csv', 'w', newline='') as out:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        writer.writerow(('LOCATION', 'MEASURE', 'TIME', 'Value', 'Flag Codes'))
        next(reader)  # Skip header
        writer.writerows([(row[1], row[4], row[6], row[7], row[8]) for row in reader if row[4] == "USD_CAP"])

def percent_health_spending():
    with open('archive/pharma-spending.csv', 'r') as inp, open('archive/perc-health-spend.csv', 'w', newline='') as out:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        writer.writerow(('LOCATION', 'MEASURE', 'TIME', 'Value', 'Flag Codes'))
        next(reader)  # Skip header
        writer.writerows([(row[1], row[4], row[6], row[7], row[8]) for row in reader if row[4] == "PC_HEALTHXP"])

def percent_gdp():
    with open('archive/pharma-spending.csv', 'r') as inp, open('archive/perc-gdp.csv', 'w', newline='') as out:
        reader = csv.reader(inp)
        writer = csv.writer(out)
        writer.writerow(('LOCATION', 'MEASURE', 'TIME', 'Value', 'Flag Codes'))
        next(reader)  # Skip header
        writer.writerows([(row[1], row[4], row[6], row[7], row[8]) for row in reader if row[4] == "PC_GDP"])

# Optimized merging with dictionaries to avoid nested loops
def merge_gdp():
    with open('archive/perc-health-spend.csv', 'r') as inp1, open('archive/perc-gdp.csv', 'r') as inp2, open('archive/merge-health-gdp.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION', 'TIME', 'PC_HEALTHXP', 'PC_GDP', 'Flag Codes'))

        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1), next(reader2)  # Skip headers

        health_dict = {(row[0], row[2]): row for row in reader1}  # Key by LOCATION, TIME
        for row2 in reader2:
            key = (row2[0], row2[2])
            if key in health_dict:
                row = health_dict[key]
                writer.writerow((row[0], row[2], row[3], row2[3], row[4]))

def merge_cap():
    with open('archive/merge-health-gdp.csv', 'r') as inp1, open('archive/usd-cap.csv', 'r') as inp2, open('archive/merge-all.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION', 'TIME', 'PC_HEALTHXP', 'PC_GDP', 'USD_CAP', 'Flag Codes'))

        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1), next(reader2)  # Skip headers

        health_gdp_dict = {(row[0], row[1]): row for row in reader1}  # Key by LOCATION, TIME
        for row2 in reader2:
            key = (row2[0], row2[2])
            if key in health_gdp_dict:
                row = health_gdp_dict[key]
                writer.writerow((row[0], row[1], row[2], row[3], row2[3], row[4]))

def merge_total_spending():
    with open('archive/merge-all.csv', 'r') as inp1, open('archive/population.csv', 'r') as inp2, open('data/data.csv', 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION', 'TIME', 'PC_HEALTHXP', 'PC_GDP', 'USD_CAP', 'FlAG_CODES', 'TOTAL_SPEND'))

        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1), next(reader2)  # Skip headers

        merge_all_dict = {(row[0], row[1]): row for row in reader1}  # Key by LOCATION, TIME
        for row2 in reader2:
            key = (row2[1], row2[2])
            if key in merge_all_dict:
                row = merge_all_dict[key]
                total_spending = round(float(row2[3]) * float(row[4]) / 1_000_000, 2)
                writer.writerow((*row, total_spending))

pharma_spending_all()
usd_per_cap()
percent_health_spending()
percent_gdp()
merge_gdp()
merge_cap()
merge_total_spending()
