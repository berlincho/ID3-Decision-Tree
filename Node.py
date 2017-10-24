# Node class template
class DTreeNode:
    def __init__(self, data, node_id):
        self.data = data
        self.node_id = node_id
        self.left = None
        self.right = None
        self.threshold = -1
        self.threshold_attr_index = -1
        self.isLeaf = True
        self.isPure, self.label = self.majority_value(data)

    def majority_value(self, data):
        if len(data) == 0:
            print "fuck"

        valFreq = {}
        label_index = 4
        
        #calculate frequency of values in target attr
        for tuple in data:
            if valFreq.has_key(tuple[label_index]):
                valFreq[tuple[label_index]] += 1 
            else:
                valFreq[tuple[label_index]] = 1
        max = 0
        major = ""
        isPure = False

        for key in valFreq.keys():
            if valFreq[key] > max:
                max = valFreq[key]
                major = key
        if len(valFreq.keys()) == 1:
            isPure = True

        return isPure, major 