from sklearn.svm import SVR
import numpy as np
import csv
from sklearn.feature_selection import SelectKBest, f_regression, chi2
from sklearn.preprocessing import StandardScaler 

WINDOW_SIZE = 10
KERNEL = 'poly'


#Le conjunto de treino
with open('train.csv', 'r') as myfile:
    train_data = myfile.read()
train_csv = csv.reader(train_data.split('\n'), delimiter=',')

#pula header
header = next(train_csv)

train = []
for row in train_csv:
	train.append(row[:])

means = []
maxs = []
mins = []

#Normaliza valores
for i in range(1, len(train[0])):
	for j in range(0, len(train)):
		if "," in train[j][i] :
			train[j][i] = train[j][i].replace(',','')
	minimum = float(train[0][i])
	maximum = float(train[0][i])
	mean = 0
	for j in range(0, len(train)):
		if(float(train[j][i]) < minimum):
			minimum = float(train[j][i])
		if(float(train[j][i]) > maximum):
			maximum = float(train[j][i])
		mean += float(train[j][i])
	mean /= len(train)
	means.append(mean)
	maxs.append(maximum)
	mins.append(minimum)
	for j in range(0, len(train)):
		train[j][i] = float((float(train[j][i]) - mean)/(maximum - minimum + 1))

#Gera alvos, entradas e labels
label = []
target = []
input_variables = []

for i in range(WINDOW_SIZE, len(train)):
	label.append(train[i][0])
	target.append(train[i][1])
	sample = []
	for j in range(i - WINDOW_SIZE, i):
		for k in range(2, len(train[j])):
			sample.append(train[j][k])
	input_variables.append(sample)

#diminui o numero de features
slk = SelectKBest(f_regression, k=10)
slk.fit(input_variables, target)
input_variables = slk.transform(input_variables)

#treina regressor
regressor = SVR(kernel = KERNEL, gamma = 0.00001, degree = 2, tol = 1e-5, epsilon = 1e-3)
regressor.fit(input_variables, target)
previsions = regressor.predict(input_variables)

with open('result_train_set.csv', 'w', newline='') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',')
	new_header = ["Date", "Bitcoin_Predicted_Variation" ,"Bitcoin_Real_Variation"]
	for i in range(0, len(input_variables)):
		filewriter.writerow([label[i], previsions[i], target[i]])

cost_func = 0
acert_sinal = 0
for i in range(0, len(target)):
	cost_func += (target[i] - previsions[i])*(target[i] - previsions[i])
	if(target[i]*previsions[i] > 0):
		acert_sinal += 1
cost_func /= len(target)

print("train cost =", cost_func)

#Le conjunto de teste
with open('test.csv', 'r') as myfile:
    test_data = myfile.read()
test_csv = csv.reader(test_data.split('\n'), delimiter=',')

#pula header
header = next(test_csv)

test = []
for row in test_csv:
	test.append(row[:])

means = []
maxs = []
mins = []

#Normaliza valores
for i in range(1, len(test[0])):
	for j in range(0, len(test)):
		if "," in test[j][i] :
			test[j][i] = test[j][i].replace(',','')
	minimum = float(test[0][i])
	maximum = float(test[0][i])
	mean = 0
	for j in range(0, len(test)):
		if(float(test[j][i]) < minimum):
			minimum = float(test[j][i])
		if(float(test[j][i]) > maximum):
			maximum = float(test[j][i])
		mean += float(test[j][i])
	mean /= len(test)
	means.append(mean)
	maxs.append(maximum)
	mins.append(minimum)
	for j in range(0, len(test)):
		test[j][i] = float((float(test[j][i]) - mean)/(maximum - minimum + 1))

#Gera alvos, entradas e labels
label = []
target = []
input_variables = []

for i in range(WINDOW_SIZE, len(test)):
	label.append(test[i][0])
	target.append(test[i][1])
	sample = []
	for j in range(i - WINDOW_SIZE, i):
		for k in range(2, len(test[j])):
			sample.append(test[j][k])
	input_variables.append(sample)

#Encontra previsoes
input_variables = slk.transform(input_variables)
previsions = regressor.predict(input_variables)

with open('result_test_set.csv', 'w', newline='') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',')
	new_header = ["Date", "Bitcoin_Predicted_Variation" ,"Bitcoin_Real_Variation"]
	for i in range(0, len(input_variables)):
		filewriter.writerow([label[i], previsions[i], target[i]])

cost_func = 0
acert_sinal = 0
for i in range(0, len(target)):
	cost_func += (target[i] - previsions[i])*(target[i] - previsions[i])
	if(previsions[i]*target[i] > 0):
		acert_sinal += 1
cost_func /= len(target)

print("test cost =", cost_func)