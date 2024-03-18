import math
import csv
import random
import operator
import numpy
import copy


class Iris:
    _sepal_lenght = None
    _sepal_width = None
    _petal_lenght = None
    _petal_width = None
    _flower_type = None

    def __init__(self, sl: float, sw: float, pl: float, pw: float, type: str):
        self._sepal_lenght = sl
        self._sepal_width = sw
        self._petal_lenght = pl
        self._petal_width = pw
        self._flower_type = type

    def sl(self) -> float:
        return self._sepal_lenght

    def sw(self) -> float:
        return self._sepal_width

    def pl(self) -> float:
        return self._petal_lenght

    def pw(self) -> float:
        return self._petal_width

    def type(self) -> str:
        return self._flower_type


def IrisDistance(a: Iris, b: Iris) -> float:
    k = a.sl() - b.sl()
    l = a.sw() - b.sw()
    m = a.pl() - b.pl()
    n = a.pw() - b.pw()
    sum = k * k + l * l + m * m + n * n
    return math.sqrt(sum)

def normalizeData(path : str):
    max = [0.0,0.0,0.0,0.0]
    min = [999.0,999.0,999.0,999.0]
    arrfunc = []
    originalData = None
#    normData = None
    # Get smallest and biggest numbers
    with open(path,'r') as file:
        lines = csv.reader(file)
        originalData = list(lines)
        for x in range(len(originalData) - 1):
            for y in range(4):
                originalData[x][y] = float(originalData[x][y])
                k = originalData[x][y]
                if k > max[y]:
                    max[y] = k
                if k < min[y]:
                    min[y] = k
    # Create a list of functions to apply to its respective column
    for y in range(4):
        g = lambda x: (x - min[y])/(max[y] - min[y])
        arrfunc.append(g)

    #normData = copy.deepcopy(originalData)
    # Normalize applying functions
    for x in range(len(originalData) - 1):
        for y in range(4):
            originalData[x][y] = arrfunc[y](originalData[x][y])
    #print("max values " + repr(max))
    #print("min values " + repr(min))

    #for x in range(len(originalData) - 1):
    #    print(repr(originalData[x]) + " >>>> " + repr(normData[x]))
    return originalData


def euclideanDistance(a, b, lenght):
    unsquaredDistance = 0
    for x in range(lenght):
        r = a[x] - b[x]
        unsquaredDistance += (r * r)
    return math.sqrt(unsquaredDistance)

def nloadDataSet(path: str, split: float):
    trainDataset = []
    testDataset = []
    dataset =  normalizeData(path)
    for x in range(len(dataset) - 1):
        for y in range(4):
            if random.random() < split:
                trainDataset.append(dataset[x])
            else:
                testDataset.append(dataset[x])
    return trainDataset, testDataset



def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAccuracy(testDataset, predictions):
    correct = 0
    for x in range(len(testDataset)):
        if testDataset[x][-1] is predictions[x]:
            correct += 1
    return (correct / float(len(testDataset))) * 100.0


def main():
    trainingDataset = []
    testSet = []
    split = 0.67
    path = "iris.data"  # put dataset path here
    trainingDataset, testSet = nloadDataSet(path, split)
    predictions = []
    k = 3
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingDataset, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('Predito: ' + repr(result) + ' >Atual: ' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Acerto: ' + repr(accuracy) + '%')


if __name__ == '__main__':
    main()
