import datetime
from flask import jsonify
from flask.globals import request
from SentimentAnalyser.TweetSentimentAnalyser import *


def analyse_company_tweets():
    companyName=request.args['name']
    print(type(companyName))
    #companyName=get_company_name(id)
    analyser = TweetSentimentAnalyser()
    stats = analyser.getCompanySentiment(companyName)
    return jsonify(stats)




#analyse_company_tweets()