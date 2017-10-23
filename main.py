from Node import DTreeNode
from DecisionTree import *
import pprint

def chunks(list, n):
    """Yield successive n-sized chunks from list"""
    for i in range(0, len(list), n):
        yield list[i:i + n]

def ID3(KFold):
    shuffled_data = read_data("./iris.data.txt")
    a = list(chunks(shuffled_data, len(shuffled_data)/KFold))

    for k in range(KFold):
        training_data = []
        testing_data = a[k]
        for chunk in range(KFold)
            if chunk != k:
                training_data.append(a[chunk])
        id = 0
        root = DTreeNode(training_data, id)
        

if __name__ == "__main__":
    # KFold value must be greater than 2
    KFold = 5
    ID3(KFold)