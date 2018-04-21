from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import re
from textblob import TextBlob
from elasticsearch import Elasticsearch
import json
#from pycorenlp import StanfordCoreNLP
#nlp = StanfordCoreNLP('http://localhost:9000')

def get_tweet_sentiment(tweet):
        # create TextBlob object of passed tweet text
        # analysis = TextBlob(tweet["tweet"])
        analysis = TextBlob(tweet["text"])
        # set sentiment
        if analysis.sentiment.polarity > 0:
            tweet['sentiment'] = 'positive'
            return tweet
        elif analysis.sentiment.polarity == 0:
            tweet['sentiment'] = 'neutral'
            return tweet
        else:
            tweet['sentiment'] = 'negative'
            return tweet

def ES_connector(partition):
    tweets = list(partition)
    print(tweets,len(tweets))
    mapping = None
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    if(es.indices.exists(index = "location")):
		if(len(tweets) != 0):
			for tweet in tweets:
				doc = {
					# "text": tweet['tweet'],
                    "text": tweet['text'],
					"location": {
							"lat": tweet['coordinates'][0],
							"lon": tweet['coordinates'][1]
							},
					"sentiment":tweet['sentiment']
				}
				if(tweet['coordinates'][0] != 0 and tweet['coordinates'][1] !=0 ):
					es.index(index="location", doc_type='request-info', body=doc)
		else:
			print("No tweets")
    else:
		mapping = {
			"mappings": {
				"request-info": {
					"properties": {
						"text": {
							"type": "text"
						},
						"location": {
							"type": "geo_point"
						},
						"sentiment": {
							"type": "text"
						}
					}
				}
			}
		}

def load_json(x):
    x = json.loads(x)
    return x

TCP_IP = 'localhost'
TCP_PORT = 9001

# Pyspark
# create spark configuration
conf = SparkConf()
conf.setAppName('TwitterApp')
conf.setMaster('local[2]')
# create spark context with the above configuration
sc = SparkContext(conf=conf)

# create the Streaming Context from spark context with interval size 2 seconds
ssc = StreamingContext(sc, 4)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 900
dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)

######### your processing here ###################
#dataStream.pprint()

dataStream = dataStream.map(lambda t: load_json(t))
dataStream = dataStream.map(lambda t: get_tweet_sentiment(t))
output = dataStream.foreachRDD(lambda t: t.foreachPartition(lambda x: ES_connector(x)))
#################################################

ssc.start()
ssc.awaitTermination()
