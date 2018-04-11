from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pycorenlp import StanfordCoreNLP

ScNLP = StanfordCoreNLP('http://localhost:3000')

def sentimentalAnalysis(tuple):
    result = ScNLP.annotate(tuple[0], properties = {'annotators':'sentiment', 'outputFormat': 'json'})
    sentiment = result['sentences'][0]['sentiment']
    location = tuple[1]
    latitude, longitude = location.split(';;;;')
    return sentiment.location

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
# dataStream.pprint()
words = dataStream.flatMap(lambda x: x.split('||#||'))
tokens = words.filter(lambda x: len(x.split('::::')) == 2)
processed = tokens.map(lambda x: x.split('::::'))
# wordcount = words.map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
# wordcount.pprint()
sentiments = processed.map(lambda x: sentimentalAnalysis(x))
sentiments.pprint()
#################################################

ssc.start()
ssc.awaitTermination()
