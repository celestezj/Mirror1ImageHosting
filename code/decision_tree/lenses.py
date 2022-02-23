from trees import *
import os.path

with open(os.path.join(os.path.dirname(__file__), 'lenses.txt'), 'r') as f:
    txt = [inst.strip().split('\t') for inst in f.readlines()]

dataSet = []
labels = []
for column, lab in zip(list(zip(*txt)), ['age', 'prescript', 'astigmatic', 'tearRate', 'class']):
    t = autoDoubleDict(list(set(column)))
    labels.append((lab, t))
    dataSet.append([t[_] for _ in column])
dataSet = np.array(list(zip(*dataSet)))

model = createTree(dataSet, labels)
treePlotter.main(model, 'predict lenses')