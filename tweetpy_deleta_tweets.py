'''
Script para apagar todos os meus tweets mais antigos que determinada data
'''
# from keep_alive import keep_alive
import tweepy
from config import *
import datetime
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

# Set up das credenciais
api_key = os.environ['api_key']
api_secret = os.environ['api_secret_key']
bearer_token = os.environ['beares_token']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def fetch_tweets(username):
  '''
  Baixa todos os tweets do usuário
  determinado em 'username'
  '''
  print("Resgatando Tweets. . .")
  all_tweets = []

  new_tweets = api.user_timeline(screen_name=username, tweet_mode='extended', count=200, exclude_replies=False)

  all_tweets.extend(new_tweets)

  # Salva o id do tweet antigo menos um
  oldest = all_tweets[-1].id - 1
  
  while len(new_tweets) > 0:   # Continua pegando tweets até a requisição retornar nada
      # Todos as requests posteriores usam max_id "para avançar no tempo"
      new_tweets = api.user_timeline(screen_name=username, tweet_mode='extended', count=200, max_id=oldest)

    
      all_tweets.extend(new_tweets)
    # Atualiza o id
      oldest = all_tweets[-1].id - 1

      
  # Transform the tweepy tweets into a 2D array that will populate the csv
  output = [ 
                [ tweet.id, 
                  tweet.created_at, 
                  tweet.created_at.strftime("%d-%m-%Y"), 
                  tweet.retweet_count,
                  tweet.favorite_count,
                  username ] for tweet in all_tweets
          ]

  for sublist in output:
    sublist.append(username)


  return output

def validate_date(date_text):
  '''
  Verifica se a data entrada pelo usuário
  está no foramto YYYY-MM-DD. Se não estiver,
  levanta uma exeção com mensagem de erro.
  '''

  try:
    datetime.datetime.strptime(date_text, '%Y-%m-%d')

  except ValueError:
    raise ValueError("A data não está no formato YYYY-MM-DD. Execute o programa novamente.")

def filter_tweets(start, tweets):
  '''
  Usa o dataframe com todos os tweets
  e a data de corte, depois da qual os
  tweets devem ser mantidos, para gerar
  uma lista com os ids das publicações
  devem ser removidas.
  '''

  print("Filtrando Tweets. . .")
  now = datetime.datetime.now()
  start_date = pd.to_datetime(start, format = "%Y-%m-%d")

  # Filtra intervalo de tweets que quero manter
  keep_dates = pd.date_range(start=start_date, end=now)
  keep_dates = [str(date)[:10] for date in keep_dates]

  # Cria uma lista de ids cujo tweet deve ser mantido
  tweets_to_delete = [ tweet[0] for tweet in tweets if str(pd.to_datetime(tweet[1]))[:10] not in keep_dates ]

  return tweets_to_delete


def delete_tweets(tweet_ids):

  '''
  Deleta os tweets cujos números
  identificadores estão na lista
  tweet_ids
  '''
  print("Deletando Tweets. . .")
  # Começa a deletar:
  delete_count = 0
  for tweet_id in tweet_ids:

      try:
          api.destroy_status(tweet_id)
          print(tweet_id, 'deletado!', delete_count)
          delete_count += 1

      except:
          print(tweet_id, 'não pode ser deletado!')

  print('Pronto!', delete_count, 'tweets foram deletados, ao todo.')


##########################
### Execução principal ###
##########################

def main():
  print("Iniciando. . .")
  
  username = "dplayer14"

  start = "2021-10-25"

  while True:
    try:
      tweets = fetch_tweets(username)
      tweets = filter_tweets(start, tweets)
      delete_tweets(tweets)
    except tweepy.TweepyException as e:
      try:
        print(e)  
      except: 
        print("error")

# keep_alive()
main()
