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


#############################################
#### BASIC 
#############################################

# Cria e posta um tweet na minha conta
# client.create_tweet(text="Hello World!")

# Dar like no tweet pelo ID
client.like(1619155250971131904)

# Retwitar pelo ID
client.retweet(1619155250971131904)

# Responder tweet pelo ID
client.create_tweet(in_reply_to_tweet_id=1619155250971131904, text="Hey you, user!")

#Mostrar cada novo tweet da minha timeline no console
#Pode recuperar vários dados, como: .id, .text, .created_at, .user, .media, .poll, outros.
print("------------------------------------------------------------------------------")
print("Tweets da minha timeline \n")
for tweet in api.home_timeline():
    print(str(tweet.user.screen_name) + ": " + tweet.text + "\n")

time.sleep(2)
print("------------------------------------------------------------------------------")


#É possível salvar o id de uma conta e, então, segui-la, mandar mensagem, dar like nos posts.
#Primeito é preciso pegar o id da conta usando o @:
username = "pizzadedados"
person = client.get_user(username=username).data.id

#Para ver todos os tweets de um usuário no console:
print("Tweets do usuário @" + username + "\n")
for tweet in client.get_users_tweets(person).data:
    print(tweet.text)
