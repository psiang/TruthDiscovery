import binary
import initGround
import initTable

def main():
    votes = initTable.init_twa("./dataset/GLAD_binary/mturklabels.txt")
    ground_list = initGround.init("./dataset/GLAD_binary/groundtruth.txt")

    binary.execute(votes, ground_list, style="Uniform")


main()
