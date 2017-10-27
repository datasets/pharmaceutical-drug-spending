import csv
import urllib.request
from datapackage import Package, Resource

sources = ["https://stats.oecd.org/sdmx-json/data/DP_LIVE/.PHARMAEXP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en"]
data = 'archive/pharma-spending.csv'
def pharma_spending_all():
    for s in sources:
        urllib.request.urlretrieve(s, data)
        
def usd_per_cap():
    with open('archive/pharma-spending.csv', 'r') as inp, open('archive/usd-cap.csv', 'w') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION','MEASURE','TIME','Value','Flag Codes'))
        for row in csv.reader(inp):
	        if row[3] == "USD_CAP":
	            writer.writerow((row[0], row[3], row[5], row[6], row[7]))
                
def percent_health_spending():
    with open('archive/pharma-spending.csv', 'r') as inp, open('archive/perc-health-spend.csv', 'w') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION','MEASURE','TIME','Value','Flag Codes'))
        for row in csv.reader(inp):
	        if row[3] == "PC_HEALTHXP":
	            writer.writerow((row[0], row[3], row[5], row[6], row[7]))
                
def percent_gdp():
    with open('archive/pharma-spending.csv', 'r') as inp, open('archive/perc-gdp.csv', 'w') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION','MEASURE','TIME','Value','Flag Codes'))
        for row in csv.reader(inp):
	        if row[3] == "PC_GDP":
	            writer.writerow((row[0], row[3], row[5], row[6], row[7]))

def merge_gdp():
    with open('archive/perc-health-spend.csv', 'r') as inp1, open('archive/perc-gdp.csv', 'r') as inp2, open('archive/merge-health-gdp.csv', 'w') as out:
        writer = csv.writer(out)
        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1, None)  # skip the headers
        reader1_list = list(reader1)
        reader2_list = list(reader2)
        writer.writerow(('LOCATION','TIME','PC_HEALTHXP','PC_GDP','Flag Codes'))
        for row in reader1_list:
            for row1 in reader2_list:
                if row[0] == row1[0] and row[2] == row1[2]:
                    row.append(row1[3])
                    writer.writerow((row[0], row[2], row[3], row[5], row[4]))

def merge_cap():
    with open('archive/merge-health-gdp.csv', 'r') as inp1, open('archive/usd-cap.csv', 'r') as inp2, open('archive/merge-all.csv', 'w') as out:
        writer = csv.writer(out)
        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1, None)  # skip the headers
        reader1_list = list(reader1)
        reader2_list = list(reader2)
        writer.writerow(('LOCATION','TIME','PC_HEALTHXP','PC_GDP','USD_CAP','Flag Codes'))
        for row in reader1_list:
            for row1 in reader2_list:
                if row[0] == row1[0] and row[1] == row1[2]:
                    row.append(row1[3])
                    writer.writerow((row[0], row[1], row[2], row[3], row[5], row[4]))

def merge_total_spending():
    with open('archive/merge-all.csv', 'r') as inp1, open('archive/population.csv', 'r') as inp2, open('data/data.csv', 'w') as out:
        writer = csv.writer(out)
        reader1 = csv.reader(inp1)
        reader2 = csv.reader(inp2)
        next(reader1, None)  # skip the headers
        reader1_list = list(reader1)
        reader2_list = list(reader2)
        writer.writerow(('LOCATION','TIME','PC_HEALTHXP','PC_GDP','USD_CAP','FlAG_CODES','Total Spending'))
        for row in reader1_list:
            for row1 in reader2_list:
                if row[0] == row1[1] and row[1] == row1[2]:
                    row.append(round((float(row1[3])*float(row[4])/1000000), 2))
                    writer.writerow(row)

pharma_spending_all()
usd_per_cap()
percent_health_spending()
percent_gdp()
merge_gdp()
merge_cap()
merge_total_spending()