import csv
import urllib.request

sources = ["https://stats.oecd.org/sdmx-json/data/DP_LIVE/.PHARMAEXP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en"]
data = 'archive/pharma-spending.csv'
def execute():
    for s in sources:
        urllib.request.urlretrieve(s, data)
        
def delete_rows():
    with open('archive/pharma-spending.csv', 'r') as inp, open('data/data.csv', 'w') as out:
        writer = csv.writer(out)
        writer.writerow(('LOCATION','INDICATOR','SUBJECT','MEASURE','FREQUENCY','TIME','Value','Flag Codes'))
        for row in csv.reader(inp):
	        if row[3] == "USD_CAP":
	            writer.writerow(row)

execute()
delete_rows()