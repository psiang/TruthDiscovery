import multi
import initGround
import initTable


def main():
    votes = initTable.init_wta("./dataset/AdultContent2_multi/labels.txt")
    ground_list = initGround.init("./dataset/AdultContent2_multi/gold.txt")

    multi.execute_style(votes, ground_list)


main()
