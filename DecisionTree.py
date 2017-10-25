import math
from random import *
from Node import DTreeNode

def normalize(data):
    normal_data = data
    num_feature = 4

    for i in range(num_feature): 
        sorted_data = sort_feature(data, i)
        max = float(sorted_data[0][i])
        min = float(sorted_data[149][i])

        tmp = 0
        for tuple in sorted_data:
            normal = (float(tuple[i]) - min) / (max - min)
            #print normal
            normal_data[tmp][i] = normal
            tmp += 1

    return normal_data

def read_data(file_name):
    data = open(file_name, "r")
    total = []

    for line in data:
        one = [x.strip() for x in line.split(',')]
        if len(one) == 5:
            total.append(one)

    #total = normalize(total)
    total = sample(total, len(total))
    return total

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
        #print len(current.left.data), len(current.right.data)

    if not current.left.isPure and len(current.left.data) > 5:
        Build_DTree(current.left)
    elif not current.right.isPure and len(current.right.data) > 5:
        Build_DTree(current.right)

    return None

def split_data(data, threshold, threshold_index):
    index = threshold_index
    left = [] 
    right = []
    for tuple in data:
        if float(tuple[index]) > threshold:
            right.append(tuple)
        else:
            left.append(tuple)

    return left, right

def best_info_gain_feature(node):
    min_rem = float('inf')
    best_threshold = -1
    best_threshold_index = -1
    num_feature = 4

    # Get min rem as max info. gain
    for i in range(num_feature):
        rem, threshold = calculate_rem(node.data, i)
        if rem < min_rem:
            min_rem = rem
            best_threshold = threshold
            best_threshold_index = i
        #print rem, threshold
    
    #print best_threshold, best_threshold_index
    return best_threshold, best_threshold_index

def calculate_rem(data, feature_index):
    sorted_data = sort_feature(data, feature_index)
    label_index = 4
    check = sorted_data[0][label_index]
    last = float(sorted_data[0][feature_index])
    best_threshold = float(sorted_data[0][feature_index])
    min_rem = float('inf')
    rem = float('inf')

    #if len(sorted_data) == 120 and feature_index ==0:
    #    pprint(sorted_data)
    #    print check, last

    for tuple in sorted_data:
        if tuple[label_index] != check:
            threshold = (float(tuple[feature_index]) + last) / 2.0
            left, right = split_data(sorted_data, threshold, feature_index)
            rem = float(len(left)) / len(sorted_data) * entropy(left) + (float(len(right)) / len(sorted_data)) * entropy(right)
            check = tuple[label_index]

        if rem < min_rem:
            min_rem = rem
            best_threshold = threshold
        last = float(tuple[feature_index])
    return min_rem, best_threshold  

def entropy(data):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    target_attr = 4
    val_freq     = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]]  = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
    return data_entropy

def sort_feature(data, feature_index):
    # Bubble sort
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if float(data[j][feature_index]) > float(data[i][feature_index]):
                data[j], data[i] = data[i], data[j]

    return data

def validation(node, testing_data):
    num_pass = 0
    num_fail = 0
    label_index = 4

    label1 = 0
    label2 = 0
    label3 = 0

    pass1 = 0
    pass2 = 0
    pass3 = 0

    predict1 = 0
    predict2 = 0
    predict3 = 0

    for tuple in testing_data:
        prediction = search_DTree(node, tuple)
        label = tuple[label_index]

        if prediction == label:
            if prediction == "Iris-virginica":
                pass1 += 1
            elif prediction == "Iris-setosa":
                pass2 += 1
            elif prediction == "Iris-versicolor":
                pass3 += 1
        else:
            num_fail += 1
        
        if label == "Iris-virginica":
            label1 += 1
        elif label == "Iris-setosa":
            label2 += 1
        elif label == "Iris-versicolor":
            label3 += 1

        if prediction == "Iris-virginica":
            predict1 += 1
        elif prediction == "Iris-setosa":
            predict2 += 1
        elif prediction == "Iris-versicolor":
            predict3 += 1

    num_pass = pass1 + pass2 + pass3
    return num_pass, pass1, pass2, pass3, label1, label2, label3, predict1, predict2, predict3


def search_DTree(node,tuple):
    if node.isLeaf:
        return node.label
    if float(tuple[node.threshold_index]) < float(node.threshold):
        return search_DTree(node.left, tuple)
    else:
        return search_DTree(node.right, tuple)        

def random_pick(data, num):
    # Pick 80 entries randomly from 120
    selected = {}
    random_data = []
    while len(random_data) < num:
        random_index = randint(0, 119)
        if selected.has_key(random_index):
            continue
        else:
            selected[random_index]  = random_index
            random_data.append(data[random_index])

    return random_data

def validation_forest(DTree_forest, testing_data):
    num_pass = 0
    num_fail = 0
    label_index = 4

    label1 = 0
    label2 = 0
    label3 = 0

    pass1 = 0
    pass2 = 0
    pass3 = 0

    predict1 = 0
    predict2 = 0
    predict3 = 0

    for tuple in testing_data:
        prediction_list = []
        for i in range(len(DTree_forest)):
            prediction_list.append(search_DTree(DTree_forest[i], tuple))

        prediction = vote(prediction_list)
        label = tuple[label_index]

        if prediction == label:
            if prediction == "Iris-virginica":
                pass1 += 1
            elif prediction == "Iris-setosa":
                pass2 += 1
            elif prediction == "Iris-versicolor":
                pass3 += 1
        else:
            num_fail += 1

        if label == "Iris-virginica":
            label1 += 1
        elif label == "Iris-setosa":
            label2 += 1
        elif label == "Iris-versicolor":
            label3 += 1

        if prediction == "Iris-virginica":
            predict1 += 1
        elif prediction == "Iris-setosa":
            predict2 += 1
        elif prediction == "Iris-versicolor":
            predict3 += 1

    num_pass = pass1 + pass2 + pass3
    return num_pass, pass1, pass2, pass3, label1, label2, label3, predict1, predict2, predict3

def vote(prediction_list):
    val_freq = {}
    for record in prediction_list:
        if (val_freq.has_key(record)):
            val_freq[record] += 1
        else:
            val_freq[record] = 1

    max = 0
    major = ""
    for key in val_freq.keys():
        if val_freq[key] > max:
            max = val_freq[key]
            major = key

    return major
