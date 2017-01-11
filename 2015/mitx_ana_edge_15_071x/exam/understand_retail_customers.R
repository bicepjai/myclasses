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


houseHolds = read.csv("Households.csv",stringsAsFactors=FALSE)
str(houseHold)

onlymorn = subset(houseHolds, MorningPct == 100)
onlynoon = subset(houseHolds, AfternoonPct == 100)
str(onlymorn)
str(onlynoon)

spentgt150 = subset(houseHolds, AvgSalesValue >= 150)
str(spentgt150)

avgdiscgt25 = subset(houseHolds, AvgDiscount >= 25)
str(avgdiscgt25)

visitsgt300 = subset(houseHolds, NumVisits >= 300)
str(visitsgt300)

preproc = preProcess(houseHolds)
houseHoldsNorm = predict(preproc, houseHolds)

set.seed(200)
distances <- dist(houseHoldsNorm, method = "euclidean")
ClusterShoppers <- hclust(distances, method = "ward.D")
plot(ClusterShoppers, labels = FALSE)

set.seed(200)
k = 10
kmc10 = kmeans(houseHoldsNorm, centers = k, iter.max = 1000)
str(kmc10)
houseHoldsClusters10 = kmc10$cluster

clusters10 = list()
for(i in 1:k) {
  clusters10[[i]] = subset(houseHolds, houseHoldsClusters == i)
  print(nrow(clusters10[[i]]))
  print(summary(clusters10[[i]]))
}

set.seed(5000)
k = 5
kmc5 = kmeans(houseHoldsNorm, centers = k, iter.max = 1000)
str(kmc5)
houseHoldsClusters5 = kmc5$cluster

clusters5 = list()
for(i in 1:k) {
  clusters5[[i]] = subset(houseHolds, houseHoldsClusters5 == i)
  print(nrow(clusters5[[i]]))
  print(summary(clusters5[[i]]))
}
kmc5$centers

houseHolds_with5ClusterId = cbind(houseHolds, houseHoldsClusters5)

boxplot(houseHolds_with5ClusterId$NumVisits ~ houseHolds_with5ClusterId$houseHoldsClusters5)
ggplot(data = houseHolds_with5ClusterId, aes(x = houseHoldsClusters5, y = NumVisits)) + geom_histogram()
ggplot(houseHolds_with5ClusterId, aes(x = NumVisits, y = houseHoldsClusters5)) + geom_point()




