# -*- coding: utf-8 -*-
from textblob import TextBlob
import xmltodict
import urllib
import datetime


#How does TextBlobl work?
#Command: TextBlob("not a very great calculation").sentiment
#Output: Sentiment(polarity=-0.3076923076923077, subjectivity=0.5769230769230769)
#This tells us that the English phrase “not a very great calculation” has a polarity of about -0.3, meaning it is slightly negative, and a subjectivity of about 0.6, meaning it is fairly subjective.

def get_stock_sentiment(ticker, name):
    # Access financial news article for this stock from yahoo
    url = 'http://feeds.finance.yahoo.com/rss/2.0/headline?s='+ticker.lower()+'&region=US&lang=en-US'
    response = urllib.urlopen(url);
    stocknews = xmltodict.parse(response.read())

    news = []
    for article in stocknews['rss']['channel']['item']:
        try:
            news.append(article)
        except:
            print "Cannot parse article for some reason"
            pass

    market_sentiment = []
    total_sentiment = []
    total_subjectivity = []
    for x in news:
        # Check sentiment from title and description
        p = TextBlob(x['title']).sentiment
        y = TextBlob(x['description']).sentiment
        # Ensure that the polarity is significant and that the stock name appears in the title or description 
        if (abs(p.polarity) > 0.2 or abs(y.polarity) > 0.2) and (name in x['title'].lower() or name in x['description'].lower()):
            # Article polarity is the average of title and description polarities. Same for subjectivity
            sentiment = (p.polarity + y.polarity) / 2
            subjectivity = (p.subjectivity + y.subjectivity) / 2
            # Keep a running tally
            total_sentiment.append(sentiment)
            total_subjectivity.append(subjectivity)
            market_sentiment.append({'sentiment': sentiment, 'subjectivity': subjectivity, 'title': x['title'], 'url': x['link']})

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    stock_sentiment = {'avg_sentiment': sum(total_sentiment)/len(total_sentiment), 'avg_subjectivity': sum(total_subjectivity)/len(total_subjectivity), 'details': market_sentiment, 'date': date, 'sources': len(market_sentiment)}
    print stock_sentiment


get_stock_sentiment('AAPL', 'apple')
