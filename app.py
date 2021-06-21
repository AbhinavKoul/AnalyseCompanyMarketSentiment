from TweetSentimentAnalyser import *

if __name__ == '__main__':
    analyser = TweetSentimentAnalyser()

    stats = analyser.getCompanySentiment("#TCS")

    print(stats)
    print("positive")
    analyser.seePositiveTweets()
    print("negative")
    analyser.seeNegativeTweets()

