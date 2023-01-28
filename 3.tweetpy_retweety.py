#https://www.youtube.com/watch?v=tC9GnD0aU2c

#importa bibliotecas
import tweepy as tw
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

#para pegar uma lista de tweets, acionar streaming
#cria uma classe MyStream filha da classe StreamClient do tweetpy

class MyStream(tw.StreamingClient):
    def on_connect(self):               #informa que o streaming começou
        print("Connected")

    def on_tweet(self, tweet):          #é chamada quando um novo tweet que atende aos critérios estabalececidos é detectado
        print(tweet.text)
        try:
            client.retweet(tweet.id)
        
        except Exception as error:
            print(error)


#cria uma instância da classe MyStream
stream = MyStream(bearer_token=token)    

#Criar StreamRules.
#Regras que o stream vai seguir ao retornar o resultado
#Nesta regra: retornar os tweets que contenham #python OU #datascience E nào sejam retweet, nem reply
rule = tw.StreamRule("(#cienciadedados OR #datascience) (-is:retweet -is:reply)")

#Para adicionar a regra ao Stream
#O parâmetro dry_run=True impede que a regra se mantenha válida após finalizado o script
stream.add_rules(rule, dry_run=True)

#Para rodar o stream
stream.filter()