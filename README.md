Pharmaceutical Drug Spending by countries with indicators such as a share of total health spending, in USD per capita (using economy-wide PPPs) and as a share of GDP. Plus, total spending by each countries in the specific year. 

## Data

Data comes from Organisation for Economic Cooperation and Development on https://data.oecd.org/healthres/pharmaceutical-spending.htm

It consists of useful information about percent of health spending, percent of GDP and US dollars per capita for specific countries. Also, we added total spending by countries using their population data.

Population data comes from DataHub http://datahub.io/core/population since it is regularly updated and includes all country codes.

## Preparation 

There are several steps have been done to get final data.

* We extracted separately each resource by "percent of health spending", "percent of GDP" and "US dollars per capita"
* We merged them into one resource and added new column "TOTAL_SPEND"

"TOTAL_SPEND" is calculated using "US dollars per capita" and "population" data.
Source for original pharmacy drug spending:  https://stats.oecd.org/sdmx-json/data/DP_LIVE/.PHARMAEXP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en. 

Process is recorded and automated in python script:

```
# to get population.csv
scripts/population.py 
# to get final data.csv
scripts/process.py
```

## License

Public Domain Dedication and License (PDDL)