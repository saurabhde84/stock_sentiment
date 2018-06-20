# -*- coding: utf-8 -*-
from textblob import TextBlob
import xmltodict
import urllib
import datetime

# How does TextBlobl work?
# Command: TextBlob("not a very great calculation").sentiment
# Output: Sentiment(polarity=-0.3076923076923077, subjectivity=0.5769230769230769)
# This tells us that the English phrase “not a very great calculation” has a polarity of about -0.3, meaning it is slightly negative, and a subjectivity of about 0.6, meaning it is fairly subjective.

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
    try:
        return {'avg_sentiment': sum(total_sentiment)/len(total_sentiment), 'avg_subjectivity': sum(total_subjectivity)/len(total_subjectivity), 'details': market_sentiment, 'date': date, 'sources': len(market_sentiment)}
    except:
        # Nothing to be analyzed; No articles available
        return None


print get_stock_sentiment('AAPL', 'apple')
# Example Output:
# [{'2018-06-19': {'avg_subjectivity': 0.4447916666666667, 'date': '2018-06-19', 'avg_sentiment': 0.2802604166666667, 'details': [{'url': u'https://finance.yahoo.com/news/relm-wireless-reports-first-quarter-203000036.html?.tsrc=rss', 'title': u'RELM Wireless Reports First Quarter 2018 Results', 'sentiment': 0.1875, 'subjectivity': 0.25}, {'url': u'https://finance.yahoo.com/news/relm-wireless-host-first-quarter-203000565.html?.tsrc=rss', 'title': u'RELM Wireless to Host First Quarter 2018 Conference Call on Thursday, May 10, 2018', 'sentiment': 0.175, 'subjectivity': 0.23333333333333334}, {'url': u'https://finance.yahoo.com/news/buying-relm-wireless-corporation-nysemkt-132818757.html?.tsrc=rss', 'title': u'Is Buying RELM Wireless Corporation (NYSEMKT:RWC) For Its Upcoming $0.02 Dividend A Good Choice?', 'sentiment': 0.475, 'subjectivity': 0.675}, {'url': u'https://finance.yahoo.com/news/free-research-report-vocera-communications-112000478.html?.tsrc=rss', 'title': u'Free Research Report as Vocera Communications\u2019 Quarterly Revenue Surged 26%; Recorded Profit on Y-O-Y', 'sentiment': 0.4, 'subjectivity': 0.8}, {'url': u'https://finance.yahoo.com/news/does-relm-wireless-corporation-nysemkt-195923038.html?.tsrc=rss', 'title': u'How Does RELM Wireless Corporation (NYSEMKT:RWC) Affect Your Portfolio Returns?', 'sentiment': 0.25, 'subjectivity': 0.25}, {'url': u'https://finance.yahoo.com/news/major-shareholders-relm-wireless-corporation-170325171.html?.tsrc=rss', 'title': u'Who Are The Major Shareholders Of RELM Wireless Corporation (NYSEMKT:RWC)?', 'sentiment': 0.13791666666666666, 'subjectivity': 0.5083333333333333}, {'url': u'https://finance.yahoo.com/news/relm-wireless-corporation-nysemkt-rwc-123218853.html?.tsrc=rss', 'title': u'Is RELM Wireless Corporation (NYSEMKT:RWC) As Financially Strong As Its Balance Sheet Indicates?', 'sentiment': 0.36666666666666664, 'subjectivity': 0.5916666666666667}, {'url': u'https://finance.yahoo.com/news/income-investors-buy-relm-wireless-102507319.html?.tsrc=rss', 'title': u'Should Income Investors Buy RELM Wireless Corporation (NYSEMKT:RWC) Before Its Ex-Dividend?', 'sentiment': 0.25, 'subjectivity': 0.25}], 'sources': 8}}]
