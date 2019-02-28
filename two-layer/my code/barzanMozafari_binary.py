import binary
import initGround
import initTable


def main():
    votes = initTable.init_wta("./dataset/barzanMozafari_binary/labels.txt")
    ground_list = initGround.init("./dataset/barzanMozafari_binary/evaluation.txt")

    binary.execute(votes, ground_list, style="Uniform")


main()
