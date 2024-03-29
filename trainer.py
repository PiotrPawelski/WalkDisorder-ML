import csv
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import pickle

path = "Dataset.csv"

#Load CSV
with open(path, 'r') as csvData:
    dataset = list(csv.reader(csvData, delimiter=';'))

#Exclude header
dataset = dataset[1:]

#Convert to float
for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        dataset[i][j] = float(dataset[i][j])

#Process timestamps
diff = 0
time = dataset[0][0]

for i in range(len(dataset)):
    ABS = abs(dataset[i][1]) + abs(dataset[i][2]) + abs(dataset[i][3])

    if diff > 700 and ABS > 15:
        diff = 0
        time = dataset[i][0]
    
    diff = dataset[i][0] - time
    dataset[i][0] = diff

#Merge data for one step
dataset3D = []
tempList = []

for i in range(len(dataset)):
    if dataset[i][0] == 0 and i != 0 and dataset[i-1][0] != 0:
        dataset3D.append(tempList[:210])
        tempList = []
    tempList += dataset[i][1:]

dataset3D.append(tempList[:210])

#Define algorithms
anomaly_algorithms = [
    ("Isolation Forest", IsolationForest(behaviour='new',
                                         contamination='auto')),
    ("Local Outlier Factor", LocalOutlierFactor(
        n_neighbors=35, contamination='auto', novelty=True))]


for name, algorithm in anomaly_algorithms:

    #Train model
    algorithm.fit(dataset3D)

    #Save model
    filename = name + '.model'

    with open(filename, "wb") as File:
        pickle.dump(algorithm, File)
