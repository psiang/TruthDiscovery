import caculate
import tans2csv

def main():
    data_file = "./dataset/GLAD_binary/mturklabels.csv"
    truth_file = "./dataset/GLAD_binary/groundtruth.csv"

    tans2csv.trans_twa("./dataset/GLAD_binary/mturklabels.txt", data_file)
    tans2csv.trans_ground("./dataset/GLAD_binary/groundtruth.txt", truth_file)

    caculate.execute(data_file, truth_file)


if __name__=='__main__':
    main()
