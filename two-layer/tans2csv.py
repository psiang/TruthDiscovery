import csv


def trans_ground(loc_in, loc_out, gap=""):
    if gap == "":
        fo = open(loc_in, "r")
        csv_file = open(loc_out, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['example', 'truth'])
        writer.writerow(['example', 'truth'])
        for line in fo.readlines():
            line = line.strip('\n')
            ground_truth = [line.split()[0], line.split()[1]]
            writer.writerow(ground_truth)
        fo.close()
        csv_file.close()
    else:
        fo = open(loc_in, "r")
        csv_file = open(loc_out, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['example', 'truth'])
        for line in fo.readlines():
            line = line.strip('\n')
            ground_truth = [line.split(gap)[0], line.split(gap)[1]]
            writer.writerow(ground_truth)
        fo.close()
        csv_file.close()


def trans_twa(loc_in, loc_out, gap=""):
    if gap == "":
        fo = open(loc_in, "r")
        csv_file = open(loc_out, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['example', 'worker', 'label'])
        for line in fo.readlines():
            line = line.strip('\n')
            vote = [line.split()[0], line.split()[1], line.split()[2]]
            writer.writerow(vote)
        fo.close()
        csv_file.close()
    else:
        fo = open(loc_in, "r")
        csv_file = open(loc_out, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['example', 'worker', 'label'])
        for line in fo.readlines():
            line = line.strip('\n')
            vote = [line.split(gap)[0], line.split(gap)[1], line.split(gap)[2]]
            writer.writerow(vote)
        fo.close()
        csv_file.close()


def trans_wta(loc_in, loc_out, gap=""):
    if gap == "":
        fo = open(loc_in, "r")
        csv_file = open(loc_out, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['example', 'worker', 'label'])
        for line in fo.readlines():
            line = line.strip('\n')
            vote = [line.split()[1], line.split()[0], line.split()[2]]
            writer.writerow(vote)
        fo.close()
        csv_file.close()
    else:
        fo = open(loc_in, "r")
        csv_file = open(loc_out, 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['example', 'worker', 'label'])
        for line in fo.readlines():
            line = line.strip('\n')
            vote = [line.split(gap)[1], line.split(gap)[0], line.split(gap)[2]]
            writer.writerow(vote)
        fo.close()
        csv_file.close()

