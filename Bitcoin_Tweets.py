# Importa bibliotecas e Versão compatível com o Python usado para importar tweets (https://github.com/Jefferson-Henrique/GetOldTweets-python)
import sys,getopt,datetime,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got
#Importa biblioteca para iterar no tempo
from datetime import timedelta, date

#Define intervalo de tempo a partir das datas de inicio e fim
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#Salva saida em arquivo csv, com colunas username;date;time;retweets;favorites;text;geo;mentions;hashtags;id;permalink
outputFile = codecs.open("tweets_data", "w+", "utf-8")
outputFile.write('username;date;time;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

start_date = date(2013, 6, 30)
end_date = date(2018, 6, 24)

for single_date in daterange(start_date, end_date):
	#Imprime data analisada
	print(single_date.strftime("%Y-%m-%d"))
	#Define dia seguinte
	next_day = single_date + timedelta(1)
	#Define como criterios a palavra-chave = bitcoin, data de busca, maximo de tweets = 100, dar preferencia a "Top Tweets"
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('bitcoin').setSince(single_date.strftime("%Y-%m-%d")).setUntil(next_day.strftime("%Y-%m-%d")).setMaxTweets(100).setTopTweets(bool)
	#Busca tweets com especificacoes definidas
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	#Escreve tweets encontrados na saida
	with open('tweets_data.csv', 'w') as csvfile:
		for t in tweets:
			outputFile.write(('\n%s;%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d"), t.date.strftime("%H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
		outputFile.flush()