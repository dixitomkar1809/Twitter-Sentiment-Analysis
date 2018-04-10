from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

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
ssc = StreamingContext(sc, 2)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 900
dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)

######### your processing here ###################
dataStream.pprint()
words = dataStream.flatMap(lambda x: x.split(' '))
wordcount = words.map(lambda x: (x,1)).reduceByKey(lambda x,y: x+y)
wordcount.pprint()
#################################################

ssc.start()
ssc.awaitTermination()
