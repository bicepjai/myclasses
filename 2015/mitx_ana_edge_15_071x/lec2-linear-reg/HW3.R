FluTrain = read.csv("FluTrain.csv")
str(FluTrain)
summary(FluTrain)
subset(FluTrain, ILI == max(FluTrain$ILI))
subset(FluTrain, Queries == max(FluTrain$Queries))
hist(FluTrain$ILI, break=mean(FluTrain$ILI))
hist(FluTrain$ILI)
plot(log(FluTrain$ILI, FluTrain$Queries))
plot(log(FluTrain$ILI), FluTrain$Queries)
lr1 = lm(ILI ~ Queries, data=FluTrain)
lr2 = lm(Queries ~ ILI, data=FluTrain)
summary(lr1)
summary(lr2)
lrl1 = lm(log(ILI) ~ Queries, data=FluTrain)
lrl2 = lm(Queries ~ log(ILI), data=FluTrain)
summary(lrl1)
summary(lrl2)
FluTrend1 = lr1
summary(FluTrend1)
FluTrend1 = lrl1
summary(FluTrend1)
cor(FluTrain)
cor(FluTrend1)
cor(FluTrain)
cor(FluTrain$ILI, FluTrain$Queries)
cor(log(FluTrain$ILI), FluTrain$Queries)
0.8142115 * 0.8142115
log(1/0.8420333)
exp(-0.5 * 0.8420333)
log(1/0.8142115)
exp(-0.5 * 0.8142115)
0.8420333 * 0.8420333
FluTest = read.csv("FluTest.csv")
PredTest1 = predict(FluTrend1, newdata=FluTest)
summary(PredTest1)
PredTest1 = exp(predict(FluTrend1, newdata=FluTest))
summary(PredTest1)
summary(FluTrend1)
summary(FluTest)
type(FluTest$Week)
?which
which(FluTest$Week == "2012-02-11 - 2012-03-11" )
which(FluTest$Week == "2012-03-11 - 2012-04-11" )
str(FluTest)
FluTest
FluTest[11]
FluTest[11,]
PredTest1
2.293422 - 2.187378
(2.293422 - 2.187378)/2.293422
SSE = sum(FluTrend1$residuals^2)
SSE
SST = sum((mean(FluTrain$ILI) - FluTest$ILI)^2)
SSE = sum((PredTest1 - FluTest$ILI)^2)
1 - SSE/SST
sqrt(SSE/nrow(FluTest))
install.packages("zoo")
library(zoo)
ILILag2 = lag(zoo(FluTrain$ILI), -2, na.pad=TRUE)
FluTrain$ILILag2 = coredata(ILILag2)
str(FluTrain)
Flu = read.csv("FluTrain.csv")
str(Flu)
summary(Flu)
summary(FluTrain)
str(FluTrain)
plot(FluTrain$ILILag2,FluTrain$ILI)
plot(FluTrain$ILILag2,log(FluTrain$ILI)
)
FluTrend2 = lm(log(ILI) ~ log(ILILag2), Queries, data=FluTrain)
FluTrend2 = lm(log(ILI) ~ log(ILILag2) + Queries, data=FluTrain)
summary(FluTrend2)
summary(FluTrend1)
cor(FluTrain)
cor(FluTrain$ILI, FluTrain$ILILag2)
cor(FluTrain$ILI, FluTrain$ILILag2, rm.na=FALSE)
cor(FluTrain$ILI, FluTrain$ILILag2)
?cor
cor(FluTrain$ILI, FluTrain$ILILag2, na.rm=FALSE)
cor(FluTrain$ILI, FluTrain$ILILag2, na.rm=TRUE)
cor(FluTrain$ILI, FluTrain$ILILag2, na.rm=TRUE, use)
var(FluTrain$ILI, FluTrain$ILILag2, na.rm=TRUE, use)
var(FluTrain$ILI, FluTrain$ILILag2, na.rm=TRUE)
var(log(FluTrain$ILI), log(FluTrain$ILILag2), na.rm=TRUE)
ILILag2 = lag(zoo(FluTest$ILI), -2, na.pad=TRUE)
FluTest$ILILag2 = coredata(ILILag2)
FluTrain
FluTrain$ILI[417]
FluTrain$ILI[416]
FluTest$ILILag2[0]
FluTest$ILILag2[1]
FluTest$ILILag2[2]
FluTest$ILILag2[2]
FluTest$ILILag2[2] = FluTrain$ILI[417]
FluTest$ILILag2[1] = FluTrain$ILI[416]
summary(FluTrend2)
PredTest2 = exp(predict(FluTrend2, newdata=FluTest))
SSE = sum((PredTest2 - FluTest$ILI)^2)
SST = sum((mean(FluTrain$ILI) - FluTest$ILI)^2)
sqrt(SSE/nrow(FluTest))
?arima
savehistory("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec2/HW3.R")
