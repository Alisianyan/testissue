# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# importing csv module
import csv
from collections import Counter

# csv file name
filename = "mtesrl_20150626_MD0000600002_stats.txt"

# initializing the titles and rows list
percentile_values = [50, 90, 99, 99.9]
fields = []
rows = []
avgtsmr_grouped_by_event = {}
event_statistics = {}

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    next(csvfile)
    next(csvfile)
    csvreader = csv.DictReader(csvfile, delimiter='\t')

    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d" % (csvreader.line_num))

for row in rows:
    if row['EVENT'] is None:
        continue
    if row['EVENT'] in avgtsmr_grouped_by_event:
        avgtsmr_grouped_by_event[row['EVENT']].append(int(row['AVGTSMR']))
    else:
        avgtsmr_grouped_by_event[row['EVENT']] = [int(row['AVGTSMR'])]
# print(avgtsmr_grouped_by_event)
for key, value in avgtsmr_grouped_by_event.items():
    value.sort()

for k in avgtsmr_grouped_by_event:
    event_statistics[k] = []


def count_percentile(event, percent):
    temp_l = avgtsmr_grouped_by_event[event]
    return temp_l[int(len(temp_l) * percent / 100)]


def values_per_eventname(event, percent):
    event_statistics[event].append(count_percentile(event, percent))


for event, value in avgtsmr_grouped_by_event.items():
    event_statistics[event].append(min(avgtsmr_grouped_by_event[event]))
    for percent in percentile_values:
        values_per_eventname(event, percent)

for x in event_statistics:
    val = event_statistics[x]
    print('{EVENTNAME} min={0} 50%={1} 90%={2}, 99%={3} 99.9%={4}'.format(*val, EVENTNAME=x))

def roundup(elem):
    return elem - (elem % 5)

for event, delays in avgtsmr_grouped_by_event.items():
    print('table for eventType = {}:'.format(event))
    print('ExecTime\tTransNo\tWeight,%\tPercent')
    counts = Counter([roundup(elem) for elem in delays])
    percent = 0;
    for value, count in sorted(counts.items()):
        weight = count*100.0/len(delays)
        percent += weight
        print('{}\t{}\t{}\t{}'.format(value, count, weight, percent))
