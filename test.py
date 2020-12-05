import csv
import datetime
print(datetime.datetime.today().weekday())
with open('data.csv') as csvfile:
    reader = csv.DictWriter(csvfile)
    
    

