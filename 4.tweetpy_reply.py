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

#define a mensagem resposta
message = "This is a test"

#define o id do usuário que quer monitorar.
# No caso, define a si mesmo como o usuário a ser monitorado
client_id = client.get_me().data.id

#Procurando por tweets que mencione o usuário client_id
while True:
    response = client.get_users_mentions(client_id)

    if response.data != None:
        for tweet in response.data:
            try:
                print(tweet.text)
                client.create_tweet(in_reply_to_tweet_id=tweet.id, text=message)
            
            except:
                pass

    time.sleep(5)