setwd("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec6")
stocks = read.csv("StocksCluster.csv")
str(stocks)
table(stocks$PositiveDec)
6324/nrow(stocks)
cor(stocks)
max(cor(stocks))
colMeans(stocks)

library(caTools)
library(rpart)
library(rpart.plot)

spl = sample.split(stocks$PositiveDec, SplitRatio = 0.7)
stocksTrain = subset(stocks, spl == TRUE)
stocksTest = subset(stocks, spl == FALSE)

library(mice)
# Logistic Regression Model
stockLogR = glm(PositiveDec~., data=stocksTrain, family="binomial")
summary(stockLogR)

# Training set predictions
predTrainLogR = predict(stockLogR, type="response")
table(stocksTrain$PositiveDec, predTrainLogR >= 0.5)
(3640+990)/nrow(stocksTrain)

# Test set predictions
predTestLogR = predict(stockLogR, newdata=stocksTest, type="response")
table(stocksTest$PositiveDec, predTestLogR >= 0.5)
(417 + 1553)/nrow(stocksTest)

# Smart baseline accuracy
table(stocksTrain$PositiveDec)
table(stocksTest$PositiveDec)
1897/nrow(stocksTest)

# Cluster Analysis
limitedTrain = stocksTrain
limitedTrain$PositiveDec = NULL
limitedTest = stocksTest
limitedTest$PositiveDec = NULL

# normalizing
library(caret)
preproc = preProcess(limitedTrain)
normTrain = predict(preproc, limitedTrain)
normTest = predict(preproc, limitedTest)
colMeans(normTrain)
colMeans(normTest)

# kmeans clusters
k = 3
set.seed(144)
km = kmeans(normTrain, centers = k, iter.max = 1000)
str(km)

library(flexclust)
km.kcca = as.kcca(km, normTrain)
clusterTrain = predict(km.kcca)
clusterTest = predict(km.kcca, newdata=normTest)

str(clusterTest)
table(clusterTest)

stocksTrain1 = subset(stocksTrain, clusterTrain == 1)
stocksTrain2 = subset(stocksTrain, clusterTrain == 2)
stocksTrain3 = subset(stocksTrain, clusterTrain == 3)
stocksTest1 = subset(stocksTest, clusterTest == 1)
stocksTest2 = subset(stocksTest, clusterTest == 2)
stocksTest3 = subset(stocksTest, clusterTest == 3)

mean(stocksTrain1$PositiveDec)
mean(stocksTrain2$PositiveDec)
mean(stocksTrain3$PositiveDec)

stockLogR1 = glm(PositiveDec~., data=stocksTrain1, family="binomial")
summary(stockLogR1)
predTrainLogR1 = predict(stockLogR1, type="response")
table(stocksTrain1$PositiveDec, predTrainLogR1 >= 0.5)

stockLogR2 = glm(PositiveDec~., data=stocksTrain2, family="binomial")
summary(stockLogR2)
predTrainLogR2 = predict(stockLogR2, type="response")
table(stocksTrain2$PositiveDec, predTrainLogR2 >= 0.5)

stockLogR3 = glm(PositiveDec~., data=stocksTrain3, family="binomial")
summary(stockLogR3)
predTrainLogR3 = predict(stockLogR3, type="response")
table(stocksTrain3$PositiveDec, predTrainLogR3 >= 0.5)

predTestLogR1 = predict(stockLogR1, newdata=stocksTest1, type="response")
table(stocksTest1$PositiveDec, predTestLogR1 >= 0.5)
predTestLogR2 = predict(stockLogR2, newdata=stocksTest2, type="response")
table(stocksTest2$PositiveDec, predTestLogR2 >= 0.5)
predTestLogR3 = predict(stockLogR3, newdata=stocksTest3, type="response")
table(stocksTest3$PositiveDec, predTestLogR3 >= 0.5)

AllPredictions = c(predTestLogR1, predTestLogR2, predTestLogR3)
AllOutcomes = c(stocksTest1$PositiveDec, stocksTest2$PositiveDec, stocksTest3$PositiveDec)

