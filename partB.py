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
import numpy
sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

data = sc.textFile("ratings.dat")
ratings = data.map(lambda l: l.split('::'))\
    .map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

training, testing = ratings.randomSplit(weights = [0.6, 0.4], seed=1)

rank = 20
numIterations = 20
model = ALS.train(training, rank, numIterations)

testdata = testing.map(lambda p: (p[0], p[1]))
predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = testing.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
MSE = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Mean Squared Error = " + str(MSE))
correctPredictionsCount = ratesAndPreds.filter(lambda r: r[1][0]==round(r[1][1])).count()
print(correctPredictionsCount, type(correctPredictionsCount))
# print("Correct Predictions -> ",ratesAndPreds.filter(lambda r: r[1][0]==round(r[1][1])).count())
totalPredictionsCount = ratesAndPreds.count()
print(totalPredictionsCount,type(totalPredictionsCount))
# print("Number of total predictions ->",ratesAndPreds.count())
accuracy = float(correctPredictionsCount)/totalPredictionsCount * 100
print("Accuracy = ", accuracy)
# correct = ratesAndPreds.map(lambda r: if (r[1][]))
