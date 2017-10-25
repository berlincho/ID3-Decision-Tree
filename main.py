from DecisionTree import *
import sys

def chunks(list, n):
    """Yield successive n-sized chunks from list"""
    for i in range(0, len(list), n):
        yield list[i:i + n]

def ID3(KFold):
    shuffled_data = read_data("./iris.data.txt")
    num_data = len(shuffled_data)
    a = list(chunks(shuffled_data, len(shuffled_data)/KFold))
    num_pass = 0

    label1 = 0
    label2 = 0
    label3 = 0

    pass1 = 0
    pass2 = 0
    pass3 = 0

    predict1 = 0
    predict2 = 0
    predict3 = 0

    for k in range(KFold):
        training_data = []
        testing_data = a[k]
        for chunk in range(KFold):
            if chunk != k:
                training_data += a[chunk]

        if RF:
            DTree_forest = []
            for d in range(20):
                training_data_80 = random_pick(training_data, 80)
                node_id = 1
                root = DTreeNode(training_data_80, node_id)
                Build_DTree(root)
                DTree_forest.append(root)

            num_pass_, pass1_, pass2_, pass3_, label1_, label2_, label3_, predict1_, predict2_, predict3_ = validation_forest(DTree_forest, testing_data)
            num_pass += num_pass_
            pass1 += pass1_
            pass2 += pass2_
            pass3 += pass3_

            label1 += label1_
            label2 += label2_
            label3 += label3_

            predict1 += predict1_
            predict2 += predict2_
            predict3 += predict3_

        else:
            node_id = 1
            root = DTreeNode(training_data, node_id)
            Build_DTree(root)

            num_pass_, pass1_, pass2_, pass3_, label1_, label2_, label3_, predict1_, predict2_, predict3_ = validation(root, testing_data)

            num_pass += num_pass_
            pass1 += pass1_
            pass2 += pass2_
            pass3 += pass3_

            label1 += label1_
            label2 += label2_
            label3 += label3_

            predict1 += predict1_
            predict2 += predict2_
            predict3 += predict3_

    # Total Accuracy
    print round(num_pass / float(num_data), 3) 
    # Class1 Iris-virginica <precision> <recall>
    print round(pass1 / float(label1), 3), round(pass1 / float(predict1), 3)
    # Class2 Iris-setosa <precision> <recall>
    print round(pass2 / float(label2), 3), round(pass2 / float(predict2), 3)
    # Class3 Iris-versicolor <precision> <recall>
    print round(pass3 / float(label3), 3), round(pass3 / float(predict3), 3)


RF = False
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-RF":
            RF = True
    # KFold value must be greater than 2
    KFold = 5
    ID3(KFold)