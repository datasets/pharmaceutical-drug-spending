<a className="gh-badge" href="https://datahub.io/core/pharmaceutical-drug-spending"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Pharmaceutical drug spending by country from 1971 to 2021, with indicators such as share of total health spending, spending in USD per capita (using economy-wide PPPs), and share of GDP. Also includes total spending in millions of USD per country per year.

## Data

Data comes from Organisation for Economic Cooperation and Development on https://data.oecd.org/healthres/pharmaceutical-spending.htm

It consists of useful information about percent of health spending, percent of GDP and US dollars per capita for specific countries. Also, we added total spending by countries using their population data.

Population data comes from DataHub's http://datahub.io/core/population since it is regularly updated and includes all country codes.

## Preparation 

There are several steps have been done to get final data.

* We extracted separately each resource by "percent of health spending", "percent of GDP" and "US dollars per capita"
* We merged them into one resource and added new column "TOTAL_SPEND"

"TOTAL_SPEND" is calculated using "US dollars per capita" and "population" data (USD_CAP × population ÷ 1,000,000, rounded to 2 decimal places).
Source for original pharmacy drug spending:  https://stats.oecd.org/sdmx-json/data/DP_LIVE/.PHARMAEXP.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en. 

Process is recorded and automated in python script:

```
# to get population.csv
python scripts/population.py 
# to get final data.csv
python scripts/process.py
```

## License

This dataset is licensed under the [Open Data Commons Public Domain Dedication and Licence (PDDL) v1.0](https://opendatacommons.org/licenses/pddl/) (`ODC-PDDL-1.0`).
