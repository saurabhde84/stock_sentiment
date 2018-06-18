# -*- coding: utf-8 -*-
from textblob import TextBlob
import xmltodict
import urllib

ticker = 'AAPL'
name = 'apple'

url = 'http://feeds.finance.yahoo.com/rss/2.0/headline?s='+ticker.lower()+'&region=US&lang=en-US'
print url
response = urllib.urlopen(url);
stocknews = xmltodict.parse(response.read())
news = []
for article in stocknews['rss']['channel']['item']:
    try:
        news.append(article)
    except:
        pass
for x in news:
    p = TextBlob(x['title']).sentiment
    y = TextBlob(x['description']).sentiment
    if (abs(p.polarity) > 0.2 or abs(y.polarity) > 0.2) and (name in x['title'].lower() or name in x['description'].lower()):
        print x['title']
        print p.polarity
        print y.polarity
