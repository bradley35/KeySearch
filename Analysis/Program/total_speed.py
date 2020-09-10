import csv
import os
import numpy as np
import json
files = sorted(os.listdir(os.path.dirname(os.path.realpath(__file__))+"/../Downloads"))
print(files)
people = []
for file in files:
    csv_file = open(os.path.dirname(os.path.realpath(__file__))+"/../Downloads/"+file)
    csv_reader = csv.reader(csv_file, delimiter=',')


    first = last = next(csv_reader, [])
    for last in csv_reader:
        pass


    time = float(last[1])-float(first[1])
    people.append(time)
people = np.array(people)
people /= np.max(np.abs(people),axis=0)
people *= 100
print(people)
with open('total_time.json', 'w') as outfile:
    json.dump(people.tolist(), outfile)
