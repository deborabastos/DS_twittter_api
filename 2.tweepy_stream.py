#https://www.youtube.com/watch?v=tC9GnD0aU2c

#importa bibliotecas
import tweepy as tw
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Set up das credenciais
consumer_key = os.environ['api_key']
consumer_secret = os.environ['api_secret_key']
token = os.environ['beares_token']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

# Conecta com API do Twitter
client = tw.Client(token, consumer_key, consumer_secret, access_token, access_token_secret)

# Esse código somente é usado se for necessários usar algumas funções da antiga versão do tweepy
auth = tw.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tw.API(auth)


#cria lista de termos a serem buscados
search_terms = ["data science", "ciência de dados"]

#cria uma classe MyStream filha da classe StreamClient do tweetpy
#essa classe será usada futuramente para abrir a transmissão (stream)
#usaremos algumas funções herdadas da StreamClient

class MyStream(tw.StreamingClient):
    def on_connect(self):               #roda quando o stream começa a rodar 
        print("Connected")

    def on_tweet(self, tweet):          #é chamada quando um novo tweet que atende aos critérios estabalececidos é detectado
        if tweet.referenced_tweets == None:
            print(tweet.text)

            time.sleep(0.2)
    
#cria uma instância da classe MyStream
stream = MyStream(bearer_token=token)

#adicionado os termos indicados na lista à regra de filtragem
#IMPORTANTE: as regras não desaparecem quando encerra o bot. Para deletar um regra, é necessário usar detele_rules().
#para ver a lista de regras ativas, usar get_rules()
for term in search_terms:
    stream.add_rules(tw.StreamRule(term))


#Para começar o streaming e filtrar os termos
stream.filter(tweet_fields=["referenced_tweets"])

