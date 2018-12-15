import binary
import initGround
import initTable


def main():
    votes = initTable.init_twa("./dataset/d_Duck/answer.csv", gap=",")
    ground_list = initGround.init("./dataset/d_Duck/truth.csv", gap=",")

    binary.execute_style(votes, ground_list)


main()
