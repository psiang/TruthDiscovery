import csv
import random

for day in range(20):
    with open("./data/truths/ground_truth_%d.csv" % (day),"w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["task","truth"])
        for i in range(50):
            writer.writerow([i, random.randint(0,1)])