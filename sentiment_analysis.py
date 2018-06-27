#NLTK usado para detectar palavras em ingles
import nltk
#Para leitura de csv
import csv, codecs
#Para interpretação de datas
from datetime import datetime
#Vader usado para analise de sentimentos
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
#from vaderSentiment import SentimentIntensityAnalyzer

#constantantes para ordem dos indices no arquivo de entrada
INDEX_DATE = 1
INDEX_RETWEETS = 3
INDEX_FAVORITES = 4
INDEX_TEXT = 5
INDEX_ID = 9

#Importa vocabulario em ingles para filtrar palavras na lingua
nltk.download('words')
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

#Cria vocabulario relacionado ao bitcoin
bitcoin_vocab = {'bitcoin', 'bitcoins', 'altcoin', 'altcoins', 'crypto', 'cryptos', 'cryptocurrency', 'cryptocurrencies', 'litcoin', 'litoins', 'ethereum', 'shitcoin', 'shitcoins'}

#Analisa se um texto tem pelo menos um terco das palavras validas em ingles
def in_english(sentence):
    words = sentence.split()
    valid_words = 0
    english_words = 0
    prev = ''
    for word in words:
        #remove virgulas, pontos, reticencias, parenteses e aspas
        word = word.replace(',','')
        word = word.replace('.','')
        word = word.replace(':','')
        word = word.replace('(','')
        word = word.replace(')','')
        word = word.replace('','')
        word = word.replace('"','')
        #Verifica se nao eh um link, um emoticon, ou uma hashtag, ou termo relacionado ao bitcoin (nao esta no dicionario)
        if prev != '#' and '1' not in word and '2' not in word and '3' not in word and '4' not in word and '5' not in word and '6' not in word and '7' not in word and '8' not in word and '9' not in word and '<' not in word and '>' not in word and '/' not in word and '(' not in word and ')' not in word and '#' not in word and '@' not in word and len(word) > 0 and word.lower() not in bitcoin_vocab:
            valid_words += 1
            if word.lower() in english_vocab:
                english_words += 1
        prev = word
    if english_words/(valid_words+0.001) >= 1/3 - 0.01:
        return True
    return False 

#Abre entrada
with open('tweets_data', 'r',  encoding="utf8", newline='') as myfile:
        text = myfile.read()
#Le entrada no formato CSV
text_data = csv.reader(text.split('\n'), delimiter=';')

#Pula cabecario
header = next(text_data)

#Inicializa analisador de sentimentos
analyzer = SentimentIntensityAnalyzer()

#Cria saida completa dos dados
outputFile_raw = codecs.open("sentiment_data_raw", "w+", "utf-8")
outputFile_raw.write('id;date;retweets;favorites;pos;neg;neu;compound')

#Cria saida com dados de interesse por dia
outputFile = codecs.open("sentiment_data", "w+", "utf-8")
outputFile.write('date;found_tweets(fractional to searched); percentual_positive; percentual_negative;weighted_positive; weighted_negative; avarage_relevance')

#verifica se eh a primeira linha
first_tweet = True

#Dadoa a serem encontrados por dia
found_tweets = 0
positive_tweets = 0
weighted_positive_tweets = 0
negative_tweets = 0
weighted_negative_tweets = 0
weight_tweets = 0
relevance_sum = 0

#Ignored columns
ig_rows = 0
#Analisa sentimentos em cada entrada
for row in text_data:
    if(len(row) < 11):
        #Se houver algo de errado com a coluna, ignora essa e avisa
        print("Coluna ", row[1], " ignorada")
        ig_rows +=1
        continue

    #Se a data do tweet for um novo dia, calcula valores para dia anterior (se valido) e imprime na saida por dias
    date = datetime.strptime(row[INDEX_DATE],"%Y-%m-%d")
    if first_tweet or date != analysed_date:
        if(first_tweet != True):
            outputFile.write(('\n%s;%f;%f;%f;%f;%f;%f' % (datetime.strftime(analysed_date, "%Y-%m-%d"),found_tweets/100 , positive_tweets/found_tweets, negative_tweets/found_tweets, weighted_positive_tweets/weight_tweets, weighted_negative_tweets/weight_tweets,relevance_sum/found_tweets)))
            outputFile.flush()
            outputFile_raw.flush()
            print(analysed_date.strftime("%Y-%m-%d"))
            found_tweets = 0
            positive_tweets = 0
            weighted_positive_tweets = 0
            negative_tweets = 0
            weighted_negative_tweets = 0
            weight_tweets = 0
            relevance_sum = 0
        else:
            first_tweet = False
        analysed_date = date

    #Se o tweet esta em ingles, faz analise de sentimentos
    if in_english(row[INDEX_TEXT]):
        vs = analyzer.polarity_scores(row[INDEX_TEXT])
        positive = vs['pos']
        negative = vs['neg']
        neutral = vs['neu']
        compound = vs['compound']
    #Senao, anula todos os fatores da analise de sentimentos
    else:
        positive = 0
        negative = 0
        neutral = 0
        compound = 0

    #Imprime os valores referentes ao tweet
    outputFile_raw.write(('\n%s;%s;%d;%d;%f;%f;%f;%f' % (row[INDEX_ID], analysed_date.strftime("%Y-%m-%d"), int(row[INDEX_RETWEETS]) , int(row[INDEX_FAVORITES]), positive, negative, neutral, compound)))
            
    #Atualiza os valores usados para calcular as estatisticas do dia
    found_tweets += 1
    weight_tweets += (int(row[INDEX_FAVORITES]) + int(row[INDEX_RETWEETS]) + 1)
    relevance_sum += int(row[INDEX_FAVORITES]) + int(row[INDEX_RETWEETS])
    if(compound > 0.05):
        positive_tweets += 1
        weighted_positive_tweets += (int(row[INDEX_FAVORITES]) + int(row[INDEX_RETWEETS]) + 1)
    elif(compound < -0.05):
        negative_tweets += 1
        weighted_negative_tweets += (int(row[INDEX_FAVORITES]) + int(row[INDEX_RETWEETS]) + 1)

print("Total de linhas ignoradas: ", ig_rows)