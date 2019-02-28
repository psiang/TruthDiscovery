import caculate
import tans2csv

def main():
    data_file = "./dataset/barzanMozafari_binary/labels.csv"
    truth_file = "./dataset/barzanMozafari_binary/evaluation.csv"

    tans2csv.trans_wta("./dataset/barzanMozafari_binary/labels.txt", data_file)
    tans2csv.trans_ground("./dataset/barzanMozafari_binary/evaluation.txt", truth_file)

    caculate.execute(data_file, truth_file)


if __name__=='__main__':
    main()