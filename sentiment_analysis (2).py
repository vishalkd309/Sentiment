pip install GetOldTweets3

# Importing required Libraries

import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd
import GetOldTweets3 as got

# Fetching Tweets
a = input("Enter your keyword : ")
tweetCriteria = got.manager.TweetCriteria().setQuerySearch(a)\
                                           .setSince("2020-06-01")\
                                           .setUntil("2020-07-01")\
                                           .setNear("Bhopal,India")\
                                           .setWithin("1500km")\
                                           .setTopTweets (True)\
                                           .setMaxTweets(1000)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
text_tweets = [[tweet.text] for tweet in tweets]

# Printing first 5 tweets

for i in range(0,5):
  table = text_tweets[i][0]
  print(str(i+1)+'\t'+table)

# Making a DataFrame of the Tweets

df = pd.DataFrame([[tweet.text] for tweet in tweets], columns = ['Tweets'])
df.head()

# Cleaning the DataFrame

def clean(text):
  text = re.sub(r'@[A-Za-z0-9]+','',text)
  text = re.sub(r'#','',text)
  text = re.sub(r'RT[\s]+','',text)
  text = re.sub(r'https?\/\/\S+','',text)
  return text

df['Tweets'] = df['Tweets'].apply(clean)

# Assigning subjectivity and polarity

def getsubjectivity(text):
  return TextBlob(text).sentiment.subjectivity
def getpolarity(text):
  return TextBlob(text).sentiment.polarity

df['Subjectivity'] = df['Tweets'].apply(getsubjectivity)
df['Polarity'] = df['Tweets'].apply(getpolarity)
df

# Defining the Sentiments based on polarity

def getanalysis(score):
  if score < 0:
    return 'NEGATIVE'
  elif score == 0:
    return 'NEUTRAL'
  else:
      return 'POSITIVE'

df['Sentiments'] = df['Polarity'].apply(getanalysis)
df

# Plots

plt.title('Sentiment Analysis')
plt.xlabel('Sentiments')
plt.ylabel('Count of Tweets')
df['Sentiments'].value_counts().plot(kind='bar')
plt.savefig('Graph.png')
plt.show()

# Export your file 

df.to_csv('Twitter.csv')
