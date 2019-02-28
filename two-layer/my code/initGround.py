def init(loc, gap=""):
    if gap == "":
        fo = open(loc, "r")
        ground_truths = []
        for line in fo.readlines():
            line = line.strip('\n')
            ground_truth = [line.split()[0], line.split()[1]]
            ground_truths.append(ground_truth)
        fo.close()
        return ground_truths
    else:
        fo = open(loc, "r")
        ground_truths = []
        count = 0
        for line in fo.readlines():
            if count == 0:
                count = 1
                continue
            line = line.strip('\n')
            ground_truth = [line.split(gap)[0], line.split(gap)[1]]
            ground_truths.append(ground_truth)
        fo.close()
        return ground_truths
