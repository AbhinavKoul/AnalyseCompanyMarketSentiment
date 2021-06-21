from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
# import pycountry
import re
import string
# from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize, WordNetLemmatizer
import pickle
from tqdm import tqdm
  
from config import *

class TweetSentimentAnalyser:
    def __init__(self):
        self.pcaFilename = "./Models/PCA.pkl"
        self.cvFilename = "./Models/CV.pkl"
        self.modelFilename = "./Models/SVC.pkl"
        self.lemma = WordNetLemmatizer()
        self.stopwordSet = set(stopwords.words('english'))
        self.tweetToAnalyse = 1000
        self.tweet_list = []
        self.negative_list = []
        self.positive_list = []

    def intitateTwitterAuthentication(self):
        self.auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        self.auth.set_access_token(accessToken, accessTokenSecret)
        self.api = tweepy.API(self.auth)  

    def loadModel(self):
        # save the model to disk
        self.pca = pickle.load(open(self.pcaFilename, 'rb'))
        self.cv = pickle.load(open(self.cvFilename, 'rb'))
        self.loaded_model = pickle.load(open(self.modelFilename, 'rb'))
    
    def pre_Processing(self, text_input:str)->int:
        
        text = re.sub('[^a-zA-Z]'," ",text_input) 
        text = text.lower()                            
        text = word_tokenize(text,language='english') 
        # text1 = [word for word in text if not word in stopwordSet] 
        # text2 = [lemma.lemmatize(word) for word in text]           
        text = [self.lemma.lemmatize(word) for word in text] 
        text = " ".join(text)                          
        #   print(text)

        text = [text]
        
        #use trained count vector and PCA to transform into reduced dimention
        x = self.cv.transform(text).toarray() 
        x = self.pca.transform(x)                        # fits 5001 columns to 256 with minimal loss
        
        #result from out model
        result = self.loaded_model.predict(x)
        return result

    def getCompanySentiment(self, company_name : str):
        self.intitateTwitterAuthentication()
        self.loadModel()
        tweets = tweepy.Cursor(self.api.search, q=company_name).items(self.tweetToAnalyse)
        
        positive = 0
        negative = 0
        tweet_set = set()
        #iterate over all the tweets scraped
        for tweet in tqdm(tweets,bar_format='{desc:<5.5}{percentage:3.0f}%|{bar:10}{r_bar}',total = self.tweetToAnalyse):
            # self.tweet_list.append(tweet.text)
            if(len(tweet.text.strip().split()) < 5):
                continue

            if(tweet.text in tweet_set):
                continue
        
            tweet_set.add(tweet.text)
            
            self.tweet_list.append(tweet.text)
            #Our model prediction
            svc_pred = self.pre_Processing(tweet.text)                             
            
            #VADER Prediction
            score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)  
            neg = score['neg']
            pos = score['pos']

            # our model gives bias towards positive, use vader to solve that part
            if(svc_pred == 0):
                self.negative_list.append(tweet.text)
                negative += 1
            else:
                if neg > pos:
                    self.negative_list.append(tweet.text)
                    negative += 1
                else:   #VADER nuetral or positive
                    self.positive_list.append(tweet.text)
                    positive += 1
            
        
        return {positive,negative,len(tweet_set)}

    def seePositiveTweets(self):
        print(pd.DataFrame(self.positive_list))
    def seeNegativeTweets(self):
        print(pd.DataFrame(self.negative_list))
