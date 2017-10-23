from Node import DTreeNode
from DecisionTree import *

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
        for chunk in range(KFold):
            if chunk != k:
                training_data += a[chunk]

        root = DTreeNode(training_data, id)
        Build_DTree(root)

def Build_DTree(node):
    current = node
    if current.isLeaf and not current.isPure:
        id = current.node_id
        current.threshold, current.threshold_index = best_info_gain_feature(current)
        left_data, right_data = split_data(current.data, current.threshold, current.threshold_index)
        id += 1
        current.left = DTreeNode(left_data, id)
        id += 1
        current.right = DTreeNode(right_data, id)
        current.isLeaf = False

    if len(current.left.data) >= 5:
        Build_DTree(current.left)
    elif len(current.right.data) >= 5:
        Build_DTree(current.right)
    else:
        return None


if __name__ == "__main__":
    # KFold value must be greater than 2
    KFold = 5
    ID3(KFold)