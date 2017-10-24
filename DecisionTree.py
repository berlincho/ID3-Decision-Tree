import random
import math

def read_data(file_name):
    data = open(file_name, "r")
    total = []

    for line in data:
        one = [x.strip() for x in line.split(',')]
        if len(one) == 5:
            total.append(one)

    total = random.sample(total, len(total))
    return total

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
    
    return best_threshold, best_threshold_index

def calculate_rem(data, feature_index):
    sorted_data = sort_feature(data, feature_index)
    label_index = 4
    check = data[0][label_index]
    last = float(data[0][feature_index])
    best_threshold = float(data[0][feature_index])
    min_rem = float('inf')
    rem = float('inf')

    for tuple in sorted_data:
        if tuple[label_index] != check:
            threshold = (float(tuple[feature_index]) + last) / 2.0
            left, right = split_data(data, threshold, feature_index)
            rem = (len(left) / len(sorted_data)) * entropy(left) + (len(right) / len(sorted_data)) * entropy(right)
        if rem < min_rem:
            min_rem = rem
            best_threshold = threshold

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
            if float(data[j][feature_index]) < float(data[i][feature_index]):
                data[j], data[i] = data[i], data[j]
    
    return data

def validation(node, testing_data):
    num_pass = 0
    num_fail = 0
    label_index = 4
    for tuple in testing_data:
        prediction = search_DTree(node, tuple)
        label = tuple[label_index]

        if prediction == label:
            num_pass += 1
        else:
            num_fail += 1

    accuracy = num_pass  / float(len(testing_data))
    print accuracy


def search_DTree(node,tuple):
    if node.isLeaf:
        return node.label
    if float(tuple[node.threshold_index]) < float(node.threshold):
        return search_DTree(node.left, tuple)
    else:
        return search_DTree(node.right, tuple)        