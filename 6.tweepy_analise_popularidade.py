#https://www.youtube.com/watch?v=_JfI96Qs9o8

#importa bibliotecas
import tweepy as tw
import pandas as pd
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

# Busca tweets conforme query, por padrão busca 10 resultados, se quiser mais é necessário indicar (max 100)
client.search_recent_tweets(query="BBB", max_results=100)



