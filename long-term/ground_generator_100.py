import csv
import random
import shutil
import os

for time in range(1, 100):
    if not os.path.exists("./data/truths/%d" % time):
        os.mkdir("./data/truths/%d" % time)
    shutil.copy("./data/truths/0/ground_truth_0.csv", "./data/truths/%d" % time)
    for day in range(1, 20):
        with open("./data/truths/%d/ground_truth_%d.csv" % (time, day),"w", newline='') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["task","truth"])
            for i in range(50):
                writer.writerow([i, random.randint(0,1)])