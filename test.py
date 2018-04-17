import csv

with open('uris.csv', "r") as csv_file:
    reader = csv.reader(csv_file)
    x = sum(1 for row in reader)
    print(x)
