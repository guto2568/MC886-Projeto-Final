#Para leitura de csv
import csv
#Para interpretação de datas
from datetime import datetime

#Abre os arquivos de dados
with open('sentiment_data', 'r') as myfile:
        sentiment_data = myfile.read()
sentiment = csv.reader(sentiment_data.split('\n'), delimiter=';')

with open('test_raw.csv', 'r') as myfile:
        test_data = myfile.read()
test = csv.reader(test_data.split('\n'), delimiter=',')

with open('train_raw.csv', 'r') as myfile:
        train_data = myfile.read()
train = csv.reader(train_data.split('\n'), delimiter=',')

#Cria dicionarios para nomes de colunas
header_sentiment = next(sentiment)
index_sentiment = {}
for i in range(0, len(header_sentiment)):
	index_sentiment[header_sentiment[i]] = i

header_train = next(train)
header_train = next(test)
index_train = {}
for i in range(0, len(header_train)):
	index_train[header_train[i]] = i


#converte para vetores
sentiment_vec = []
for row in sentiment:
	sentiment_vec.append(row)

train_vec = []
for row in train:
	train_vec.append(row)

test_vec = []
for row in test:
	test_vec.append(row)

#Junta sentimento e treino por data e imprime em um arquivo novo

i_train = 0
i_senti = 0
with open('train.csv', 'w', newline='') as csvfile:
	#cria formato
	filewriter = csv.writer(csvfile, delimiter=',')
	new_header = ["Date", "Bitcoin_Price_Variation" ,"Day", "Month", "Year"]
	for i in range(index_train["Open"], len(header_train)):
		new_header.append(header_train[i])
	for i in range(index_sentiment["found_tweets(fractional to searched)"], len(header_sentiment)):
		new_header.append(header_sentiment[i])
	filewriter.writerow(new_header)
	while i_train < len(train_vec):
		date_train = datetime.strptime(train_vec[i_train][index_train['Date']], "%d/%m/%y")
		date_sentiment = datetime.strptime(sentiment_vec[i_senti][index_sentiment['date']], "%Y-%m-%d")
		while date_sentiment < date_train:
			i_senti += 1
			date_sentiment = datetime.strptime(sentiment_vec[i_senti][index_sentiment['date']], "%Y-%m-%d")
		if date_sentiment == date_train:
			filewriter.writerow([datetime.strftime(date_sentiment, "%Y-%m-%d"), float(train_vec[i_train][index_train['Close']]) - float(train_vec[i_train][index_train['Open']]), date_sentiment.day, date_sentiment.month ,date_sentiment.year] + train_vec[i_train][index_train["Open"]:] + sentiment_vec[i_senti][index_sentiment["found_tweets(fractional to searched)"]:])
		i_train += 1	

i_test = 0
i_senti = 0
with open('test.csv', 'w', newline='') as csvfile:
	#cria formato
	filewriter = csv.writer(csvfile, delimiter=',')
	new_header = ["Date", "Bitcoin_Price_Variation" ,"Day", "Month", "Year"]
	for i in range(index_train["Open"], len(header_train)):
		new_header.append(header_train[i])
	for i in range(index_sentiment["found_tweets(fractional to searched)"], len(header_sentiment)):
		new_header.append(header_sentiment[i])
	filewriter.writerow(new_header)
	while i_test < len(test_vec):
		date_test = datetime.strptime(test_vec[i_test][index_train['Date']], "%d/%m/%y")
		date_sentiment = datetime.strptime(sentiment_vec[i_senti][index_sentiment['date']], "%Y-%m-%d")
		while date_sentiment < date_test:
			i_senti += 1
			date_sentiment = datetime.strptime(sentiment_vec[i_senti][index_sentiment['date']], "%Y-%m-%d")
		if date_sentiment == date_test:
			filewriter.writerow([datetime.strftime(date_sentiment, "%Y-%m-%d"), float(test_vec[i_test][index_train['Close']]) - float(test_vec[i_test][index_train['Open']]), date_sentiment.day, date_sentiment.month ,date_sentiment.year] + test_vec[i_test][index_train["Open"]:] + sentiment_vec[i_senti][index_sentiment["found_tweets(fractional to searched)"]:])
		i_test += 1	




