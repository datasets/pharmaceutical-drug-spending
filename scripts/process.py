import csv
import urllib.request

# New OECD SDMX 2.1 API (stats.oecd.org was retired; data now lives in sdmx.oecd.org)
# Pharmaceutical spending = System of Health Accounts, function HC5, all financing, all providers.
# Each measure needs a separate request because PRICE_BASE differs.
_BASE = "https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.0"
_PARAMS = "?dimensionAtObservation=AllDimensions&format=csvfile"

SOURCES = {
    "PC_HEALTHXP": f"{_BASE}/.A.EXP_HEALTH.PT_EXP_HLTH._T._Z.HC5._T._T._Z._Z._Z{_PARAMS}",
    "PC_GDP":      f"{_BASE}/.A.EXP_HEALTH.PT_B1GQ._T._Z.HC5._T._T._Z._Z._Z{_PARAMS}",
    "USD_CAP":     f"{_BASE}/.A.EXP_HEALTH.USD_PPP_PS._T._Z.HC5._T._T._Z._Z.V{_PARAMS}",
}

POPULATION_FILE = "archive/population.csv"


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def fetch_measure(url):
    """Return {(country, year): float} from an OECD SDMX CSV response."""
    result = {}
    reader = csv.reader(_fetch(url).splitlines())
    next(reader)  # skip header
    for row in reader:
        value = row[14]  # OBS_VALUE column
        if value:
            result[(row[1], row[13])] = float(value)  # (REF_AREA, TIME_PERIOD)
    return result


def load_population():
    """Return {(country_code, year): population} from the local population CSV."""
    result = {}
    with open(POPULATION_FILE, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[3]:
                result[(row[1], row[2])] = float(row[3])
    return result


health_pct = fetch_measure(SOURCES["PC_HEALTHXP"])
gdp_pct    = fetch_measure(SOURCES["PC_GDP"])
usd_cap    = fetch_measure(SOURCES["USD_CAP"])
population = load_population()

common_keys = sorted(set(health_pct) & set(gdp_pct) & set(usd_cap))

with open("data/data.csv", "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(("LOCATION", "TIME", "PC_HEALTHXP", "PC_GDP", "USD_CAP", "TOTAL_SPEND"))
    for key in common_keys:
        country, year = key
        usd = usd_cap[key]
        pop = population.get(key)
        total_spend = round(pop * usd / 1_000_000, 2) if pop else ""
        writer.writerow((country, year, health_pct[key], gdp_pct[key], usd, total_spend))
