def init_twa(loc, gap=""):
    if gap == "":
        fo = open(loc, "r")
        votes = []
        for line in fo.readlines():
            line = line.strip('\n')
            vote = [line.split()[0], line.split()[1], line.split()[2]]
            votes.append(vote)
        fo.close()
        return votes
    else:
        fo = open(loc, "r")
        votes = []
        count = 0
        for line in fo.readlines():
            if count == 0:
                count = 1
                continue
            line = line.strip('\n')
            vote = [line.split(gap)[0], line.split(gap)[1], line.split(gap)[2]]
            votes.append(vote)
        fo.close()
        return votes


def init_wta(loc, gap=""):
    if gap == "":
        fo = open(loc, "r")
        votes = []
        for line in fo.readlines():
            line = line.strip('\n')
            vote = [line.split()[1], line.split()[0], line.split()[2]]
            votes.append(vote)
        fo.close()
        return votes
    else:
        fo = open(loc, "r")
        votes = []
        count = 0
        for line in fo.readlines():
            if count == 0:
                count = 1
                continue
            line = line.strip('\n')
            vote = [line.split(gap)[1], line.split(gap)[0], line.split(gap)[2]]
            votes.append(vote)
        fo.close()
        return votes
