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

        node_id = 1
        root = DTreeNode(training_data, node_id)
        Build_DTree(root)

        validate(root, testing_data)

def Build_DTree(node):
    current = node
    if current.isLeaf and not current.isPure:
        node_id = current.node_id
        current.threshold, current.threshold_index = best_info_gain_feature(current)
        left_data, right_data = split_data(current.data, current.threshold, current.threshold_index)
        node_id += 1
        current.left = DTreeNode(left_data, node_id)
        node_id += 1
        current.right = DTreeNode(right_data, node_id)
        current.isLeaf = False

    if not current.left.isPure and len(current.left.data) >= 10:
        Build_DTree(current.left)
    elif not current.right.isPure and len(current.right.data) >= 10:
        Build_DTree(current.right)
    else:
        return None


if __name__ == "__main__":
    # KFold value must be greater than 2
    KFold = 5
    ID3(KFold)