import csv
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import pickle
import collections

path = "DatasetTestDisorder.csv"

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

#Load models
isolation = pickle.load(open("Isolation Forest.model", 'rb'))
factor = pickle.load(open("Local Outlier Factor.model", 'rb'))

#Collect models
anomaly_algorithms = [
    ("Isolation Forest", isolation),
    ("Local Outlier Factor", factor)]


for name, algorithm in anomaly_algorithms:

    #Test data
    print("\n" + name + "\n")

    testTable = algorithm.predict(dataset3D)
    print(testTable)

    positives = collections.Counter(testTable)[1]
    negatives = collections.Counter(testTable)[-1]
    print ("\nPositives: " + str(positives))
    print ("Negatives: " + str(negatives) + "\n")

    
