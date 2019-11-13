import csv
import numpy as np

path = r"C:\Users\Piotr\Desktop\Dataset.csv"

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

#Slice 2D list to 3D list
dataset3D = []
tempList = []

for i in range(len(dataset)):
    if dataset[i][0] == 0 and i != 0:
        dataset3D.append(tempList)
        tempList = []
    tempList.append(dataset[i])

dataset3D.append(tempList)



print (dataset3D[:3])
