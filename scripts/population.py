import csv

package = Package('https://datahub.io/core/population/datapackage.json')

resources = package.descriptor['resources']
for resource in resources:
    if resource['name'] == 'population':
        population = Resource({'path': resource['path']})

data = population.read(keyed=False)
with open("archive/population.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(('Country Name','Country Code','Year','Value'))
    for line in data:
        writer.writerow(line)