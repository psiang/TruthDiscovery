import caculate
import tans2csv

def main():
    data_file = "./dataset/d_Duck/answer.csv"
    truth_file = "./dataset/d_Duck/truth.csv"

    caculate.execute(data_file, truth_file)


if __name__=='__main__':
    main()