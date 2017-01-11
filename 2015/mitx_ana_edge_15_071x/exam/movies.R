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


movies = read.csv("Movies.csv")
str(movies)
movies.lm.train = subset(movies, Year < 2010)
movies.lm.test = subset(movies, Year >= 2010)

movies.lm1 = lm(Worldwide ~.-Name-Year,data = movies.lm.train)
summary(movies.lm1)
cor(movies.lm.train[c("Runtime","Crime","Horror","Animation","History","Nominations","Production.Budget")])
cor(movies.lm.train[c("Production.Budget", "Worldwide")])

movies.lm = lm(Worldwide ~ Runtime +Crime+Horror+Animation+History+Nominations+Production.Budget,data = movies.lm.train)
summary(movies.lm)

movies.lm.pred = predict(movies.lm, newdata = movies.lm.test)
SSE = sum((movies.lm.pred - movies.lm.test$Worldwide)^2)
SST = SST = sum((mean(movies.lm.train$Worldwide) - movies.lm.test$Worldwide)^2)
RSQ = (1 - SSE/SST)
RMSE= sqrt(RSQ)


movies$Performance = factor(ifelse(movies$Worldwide > quantile(movies$Worldwide, .75), "Excellent", ifelse(movies$Worldwide > quantile(movies$Worldwide, .25), "Average", "Poor")))
movies$Worldwide = NULL

set.seed(15071)
movies.split = sample.split(movies$Performance, SplitRatio = 0.7)
movies.cart.train = subset(movies, movies.split==TRUE)
movies.cart.test = subset(movies, movies.split==FALSE)

movies.cart = rpart(Performance ~. , data = movies.cart.train[,3:ncol(movies.cart.train)], method="class")
prp(movies.cart)

movies.cart.train.pred = predict(movies.cart, newdata = movies.cart.train, type = "class")
table(movies.cart.train$Performance, movies.cart.train.pred)

movies.cart.test.pred = predict(movies.cart, newdata = movies.cart.test, type = "class")
table(movies.cart.test$Performance, movies.cart.test.pred)





