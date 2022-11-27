'''
Created on Feb 23, 2022
Decision Tree Source Code from book "Machine Learningin Action"(Peter Harrington), rewritten with numpy
@author: muggledy
'''

import operator
import numpy as np
import treePlotter

class doubleDict(dict):
    def __delitem__(self, key):
        value = super().pop(key)
        super().pop(value, None)
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        super().__setitem__(value, key)
    
    def update(self, another):
        for key, value in another.items():
            self.__setitem__(key, value)
    
    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"

class autoDoubleDict(doubleDict):
    '''https://github.com/muggledy/GreatManQuotes/blob/master/api/search.py'''
    def __init__(self, arr=None):
        self.count = 0
        if arr is not None:
            self.update(arr)
    
    def update(self, arr):
        for obj in arr:
            if obj not in self:
                self[obj] = self.count
                self.count += 1
    
    def delete(self, arr):
        for obj in arr:
            if obj in self:
                del self[obj]

def createDataSet(): #demo
    dataSet = [[1, 1, 0],
               [1, 1, 0],
               [1, 0, 1],
               [0, 1, 1],
               [0, 1, 1]] #the last column is class label, others are characteristics
    labels = [('no surfacing?', autoDoubleDict(['no','yes'])), ('flippers?', autoDoubleDict(['no','yes'])), ('fish', autoDoubleDict(['yes','no']))]
    return np.array(dataSet, dtype=int), labels

def calcFreq(arr1d): #calc frequency of 1d array
    bins = {}
    for i in np.unique(arr1d):
        bins[i] = np.sum(arr1d==i)
    return bins

def calcShannonEnt(dataSet):
    bins = calcFreq(dataSet[:,-1])
    prob = np.array(list(bins.values()), dtype=float) / len(dataSet)
    shannonEnt = -np.sum(prob * np.log2(prob))
    return shannonEnt
    
def splitDataSet(dataSet, axis, value):
    subDataSet = np.hstack((dataSet[:,:axis], dataSet[:,axis+1:]))
    axisData = dataSet[:,axis]
    if value is None:
        return [subDataSet[axisData==i] for i in np.unique(axisData)]
    return subDataSet[axisData==value]
    
def chooseBestFeatureToSplit(dataSet):
    numFeatures = dataSet.shape[1] - 1 #the last column is used for the class labels
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1 #record (column)axis of the feature defined in dataSet
    for i in range(numFeatures):
        newEntropy = 0.0
        for subDataSet in splitDataSet(dataSet, i, None):
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy #calculate the info gain, i.e. reduction in entropy
        if (infoGain > bestInfoGain): #compare this to the best gain so far
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = calcFreq(classList)
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    labels = labels[:] #copy, do not modify labels herein, otherwise cause recursive (logic)error
    classList = dataSet[:,-1]
    if len(np.unique(classList)) == 1: #stop splitting when all of the classes are equal
        return labels[-1][1][classList[0]] #labels[-1] always represents the label information of class
    if dataSet.shape[1] == 1: #stop splitting when there are no more features in dataSet
        return labels[-1][1][majorityCnt(classList)]
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel, bestFeatValue = labels[bestFeat] #bestFeatLabel is the name of root node
    myTree = {bestFeatLabel:{}}
    del labels[bestFeat]
    uniqueFeatVals = np.unique(dataSet[:,bestFeat])
    for value in uniqueFeatVals: #bestFeatValue[value] is the branch name
        myTree[bestFeatLabel][bestFeatValue[value]] = createTree(splitDataSet(dataSet, bestFeat, value), labels)
    return myTree

def classify(modelTree, featLabels, testVec): #featLabels is just labels[:-1] which exclude the last class label
    rootNode = list(modelTree.keys())[0]
    allBranches = modelTree[rootNode]
    nodeAxis = list(zip(*featLabels))[0].index(rootNode) #which feature corresponds to the root node, find the axis of it
    direction = featLabels[nodeAxis][1][testVec[nodeAxis]] #which branch should the test sample go to, find the direction
    node = allBranches[direction] #it may be non-leaf node(a sub tree, recursion) or leaf(class label, over)
    if isinstance(node, dict):
        classLabel = classify(node, featLabels, testVec)
    else:
        classLabel = node
    return classLabel

if __name__ == '__main__':
    dataSet, labels = createDataSet()
    model = createTree(dataSet, labels)
    print(model)
    testVec = [1, 1]
    print(f'Known\nno surfacing?: {labels[0][1][testVec[0]]}, flippers?: {labels[1][1][testVec[1]]}')
    print('Ask\nif a fish?', classify(model, labels[:-1], testVec))
    treePlotter.main(model, 'decision tree of fish')