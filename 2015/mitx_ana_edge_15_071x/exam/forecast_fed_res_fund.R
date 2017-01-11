library(rpart)
library(rpart.plot)
library(randomForest)
library(caret)
library(e1071)
library(verification)
library(caTools)
library(ROCR)
library(glmnet)
library(MASS)
library(pROC)
library(ggplot2)

#text
library(SnowballC)
library(NLP)
library(tm)
library(wordcloud)
library(RColorBrewer)

#sentiment
library(plyr)
library(stringr)
library(stringi)
library(topicmodels)
library(syuzhet)
library(LDAvis)
library(dplyr)
library(qdap)

library(gbm)
library(doParallel)
#library(doMC)

library(nnet)


fedFunds = read.csv("federalFundsRate.csv",stringsAsFactors=FALSE)


fedFunds$Date = as.Date(fedFunds$Date)
fedFunds$Chairman = as.factor(fedFunds$Chairman)
fedFunds$DemocraticPres = as.factor(fedFunds$DemocraticPres)
fedFunds$RaisedFedFunds = as.factor(fedFunds$RaisedFedFunds)
str(fedFunds)

set.seed(201)
fedFunds.split = sample.split(fedFunds$RaisedFedFunds, 0.7)
fedFunds.glm.train = subset(fedFunds, fedFunds.split==TRUE)
fedFunds.glm.test = subset(fedFunds, fedFunds.split==FALSE)

fedFunds.glm = glm(RaisedFedFunds~PreviousRate+Streak+Unemployment+HomeownershipRate+DemocraticPres+MonthsUntilElection, data=fedFunds.glm.train, family="binomial")
summary(fedFunds.glm)

fedFunds.glm.test.pred = predict(fedFunds.glm, newdata=fedFunds.glm.test, type="response")
table(fedFunds.glm.test$RaisedFedFunds, fedFunds.glm.test.pred >= 0.5)

fedFunds.glm.ROCR = prediction(fedFunds.glm.test.pred, fedFunds.glm.test$RaisedFedFunds)
as.numeric(performance(fedFunds.glm.ROCR, "auc")@y.values)
fedFunds.glm.ROCRperf = performance(fedFunds.glm.ROCR, "tpr", "fpr")
plot(fedFunds.glm.ROCRperf, colorize=TRUE)
plot(fedFunds.glm.ROCRperf, colorize=TRUE, print.cutoffs.at=seq(0,1,by=0.1), text.adj=c(-0.2,1.7))

set.seed(201)
numFolds = trainControl( method = "cv", number = 10 )
cpGrid = expand.grid( .cp = seq(0.001,0.05,0.001))

train(RaisedFedFunds~PreviousRate+Streak+Unemployment+HomeownershipRate+DemocraticPres+MonthsUntilElection, data = fedFunds.glm.train, method = "rpart", trControl = numFolds, tuneGrid = cpGrid )

fedFunds.cart = rpart(RaisedFedFunds~PreviousRate+Streak+Unemployment+HomeownershipRate+DemocraticPres+MonthsUntilElection, data = fedFunds.glm.train, method="class", cp = 0.016)
prp(fedFunds.cart)

fedFunds.cart.test.pred = predict(fedFunds.cart, newdata = fedFunds.glm.test, type = "class")
table(fedFunds.glm.test$RaisedFedFunds, fedFunds.cart.test.pred)



