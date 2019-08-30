import csv
import random
import shutil
import os

now_work = "participant"
rates = ['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
for rate in rates:
    if not os.path.exists("./data/"+ now_work +"/%s/truths" % rate):
        os.mkdir("./data/"+ now_work +"/%s/truths" % rate)
    for time in range(0, 100):
        if not os.path.exists("./data/" + now_work + "/%s/truths/%d" % (rate, time)):
            os.mkdir("./data/" + now_work + "/%s/truths/%d" % (rate, time))
        #shutil.copy("./data/truths/0/ground_truth_0.csv", "./data/truths/%d" % time)
        for day in range(0, 20):
            with open("./data/" + now_work + "/%s/truths/%d/ground_truth_%d.csv" % (rate, time, day),"w", newline='') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(["task","truth"])
                for i in range(50):
                    writer.writerow([i, random.randint(0,1)])
    print(rate + " is finished!")