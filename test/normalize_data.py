from __future__ import print_function
import csv


file = open('identify_data.csv', newline='')
reader = csv.reader(file)

header = next(reader)


d_app = {}
for a in list(set([r[10] for r in reader])):
    d_app[a] = []

# print(d_app)
# print(list_app)

file = open('identify_data.csv', newline='')
reader = csv.reader(file)
header = next(reader)

for row in reader:
    sa = row[10]
    row.remove(sa)
    # print(row)
    if sa in d_app:
        d_app[sa].append(row)

file = open('normalized_data.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'appliance'])

while(not (not d_app)):
    for a in list(d_app):
        row = d_app[a][0]
        d_app[a].remove(row)
        row.append(a)
        writer.writerow(row)
        if not d_app[a]:
            d_app.pop(a)
print('finish')
# print(d_app.keys())
