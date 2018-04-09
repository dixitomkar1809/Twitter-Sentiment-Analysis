# Part B: Recommendation System
# Use Collaborative fltering fnd the accuracy of ALS model accuracy. Use ratings.dat
# fle. It contains
# User id :: movie id :: ratings :: timestamp.
# Your program should report the accuracy of the model.
# For details follow the link: https://spark.apache.org/docs/latest/mllib-collaborativefltering.
# html
# Please use 60% of the data for training and 40% for testing and report the
# MSE of the model.


from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark.context import SparkContext
from pyspark import SparkConf
sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
import numpy
data = sc.textFile("D:/PycharmProjects/BigDataAssignment3/ratings.dat")
ratings = data.map(lambda l: l.split("::")).map(lambda l: Rating(int(l[0]), int(l[1]), int(l[2]), int(l[3])))

#building the recommendation model using ALS
rank= 10
numIterations = 10
model = ALS.train(ratings, rank, numIterations)

#Evaluate the model on training data
testdata = ratings.map(lambda p: (p[0], p[1]))
predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error = " + str(MSE))

# Save and load model
model.save(sc, "target/tmp/myCollaborativeFilter")
sameModel = MatrixFactorizationModel.load(sc, "target/tmp/myCollaborativeFilter")