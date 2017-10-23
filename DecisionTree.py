import random

def read_data(file_name):
    data = open(file_name, "r")
    total = []

    for line in data:
        one = [x.strip() for x in line.split(',')]
        if len(one) == 5:
            total.append(one)

    total = random.sample(total, len(total))
    return total

