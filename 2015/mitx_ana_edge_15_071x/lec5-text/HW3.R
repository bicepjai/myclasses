emails = read.csv("emails.csv", stringsAsFactors = F)
max(nchar(emails$text))
which.min(nchar(emails$text))

library(tm)
corpusText = Corpus(VectorSource(emails$text))
corpusText = tm_map(corpusText, tolower)
corpusText = tm_map(corpusText, PlainTextDocument)
corpusText = tm_map(corpusText, removePunctuation)
corpusText = tm_map(corpusText, removeWords, stopwords("english"))
corpusText = tm_map(corpusText, stemDocument)
emailsText = DocumentTermMatrix(corpusText)
emailsText
emailsText = removeSparseTerms(emailsText, 0.95)
emailsText
emailsSparse = as.data.frame(as.matrix(emailsText))
str(emailsSparse)
max(colSums(emailsSparse))

# colnames(emailsSparse) = paste0("N", colnames(emailsSparse))
colnames(emailsSparse) = make.names(colnames(emailsSparse))

emailsSparse$spam = emails$spam

hams = subset(emailsSparse, spam == 0)
table(colSums(hams) >= 5000)
spams = subset(emailsSparse, spam == 1)
spams$spam = NULL
table(colSums(spams) >= 1000)

library(mice)
library(caTools)
set.seed(123)

spl = sample.split(emailsSparse$spam, SplitRatio = 0.7)
train = subset(emailsSparse, spl == TRUE)
test = subset(emailsSparse, spl == FALSE)

spamLog = glm(spam~., data=train, family="binomial")

library(rpart)
library(rpart.plot)
spamCART = rpart(spam~., data=train, method="class")
prp(spamCART)

library(randomForest)
set.seed(123)
spamRF = randomForest(spam~., data=train)

library(ROCR)

#Logistic Regression
#train
predTrainLog = predict(spamLog, type="response")
table(train$spam, predTrainLog > 0.00001)
table(train$spam, predTrainLog > 0.99999)
table(train$spam, predTrainLog < 0.00001)
summary(spamLog)
table(train$spam, predTrainLog > 0.5)
(3052+954)/nrow(train)
predROCR = prediction(predTrainLog, train$spam)
perfROCR = performance(predROCR, "tpr", "fpr")
plot(perfROCR, colorize=TRUE)
performance(predROCR, "auc")@y.values
#test
predTestLog = predict(spamLog, newdata = test, type="response")
table(test$spam, predTestLog > 0.5)
predROCR = prediction(predTestLog, test$spam)
perfROCR = performance(predROCR, "tpr", "fpr")
plot(perfROCR, colorize=TRUE)
performance(predROCR, "auc")@y.values

#CART
#train
PredictTrainCART = predict(spamCART)[,2]
PredictTrainCARTclass = predict(spamCART, type="class")
table(train$spam, PredictTrainCART > 0.5)
table(train$spam, PredictTrainCARTclass)
predROCR = prediction(PredictTrainCART, train$spam)
perfROCR = performance(predROCR, "tpr", "fpr")
plot(perfROCR, colorize=TRUE)
performance(predROCR, "auc")@y.values
#test
PredictTestCART = predict(spamCART, newdata = test, type = "prob")[,2]
table(test$spam, PredictTestCART > 0.5)
predROCR = prediction(PredictTestCART, test$spam)
perfROCR = performance(predROCR, "tpr", "fpr")
plot(perfROCR, colorize=TRUE)
performance(predROCR, "auc")@y.values


#RF
#train
PredictTrainRF = predict(spamRF)
table(train$spam, PredictTrainRF > 0.5)
predROCR = prediction(PredictTrainRF, train$spam)
perfROCR = performance(predROCR, "tpr", "fpr")
plot(perfROCR, colorize=TRUE)
performance(predROCR, "auc")@y.values
#test
PredictTestRF = predict(spamRF, newdata = test)
table(test$spam, PredictTestRF > 0.5)
predROCR = prediction(PredictTestRF, test$spam)
perfROCR = performance(predROCR, "tpr", "fpr")
plot(perfROCR, colorize=TRUE)
performance(predROCR, "auc")@y.values

library(slam)
wordCount = rollup(emailsText, 2, FUN=sum)$v
wordCount = rowSums(as.matrix(emailsText))
hist(wordCount)
hist(log(wordCount))
logWordCount = log(wordCount)
emailsSparse$logWordCount = logWordCount
boxplot(emailsSparse$logWordCount~emailsSparse$spam)

set.seed(123)
spl = sample.split(emailsSparse$spam, SplitRatio = 0.7)
train2 = subset(emailsSparse, spl == TRUE)
test2 = subset(emailsSparse, spl == FALSE)

#CART
spamCART2 = rpart(spam~., data=train2, method="class")
prp(spamCART2)
#train
PredictTrainCART2 = predict(spamCART2)[,2]
PredictTrainCARTclass2 = predict(spamCART2, type="class")
table(train2$spam, PredictTrainCART2 > 0.5)
table(train2$spam, PredictTrainCARTclass2)
predROCR2 = prediction(PredictTrainCART2, train2$spam)
perfROCR2 = performance(2, "tpr", "fpr")
plot(perfROCR2, colorize=TRUE)
performance(predROCR2, "auc")@y.values
#test
PredictTestCART2 = predict(spamCART2, newdata = test2, type = "prob")[,2]
table(test2$spam, PredictTestCART2 > 0.5)
predROCR2 = prediction(PredictTestCART2, test2$spam)
perfROCR2 = performance(predROCR2, "tpr", "fpr")
plot(perfROCR2, colorize=TRUE)
performance(predROCR2, "auc")@y.values


#RF
set.seed(123)
spamRF2 = randomForest(spam~., data=train2)
#train
PredictTrainRF2 = predict(spamRF2)
table(train2$spam, PredictTrainRF2 > 0.5)
predROCR2 = prediction(PredictTrainRF2, train2$spam)
perfROCR2 = performance(predROCR2, "tpr", "fpr")
plot(perfROCR2, colorize=TRUE)
performance(predROCR2 "auc")@y.values
#test
PredictTestRF2 = predict(spamRF2, newdata = test2)
table(test2$spam, PredictTestRF2 > 0.5)
predROCR2 = prediction(PredictTestRF2, test2$spam)
perfROCR2 = performance(predROCR2, "tpr", "fpr")
plot(perfROCR2, colorize=TRUE)
performance(predROCR2, "auc")@y.values

install.packages("RTextTools")
install.packages("tau")
install.packages("textcat")
install.packages("RWeka")

