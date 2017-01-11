pisa = read.csv("pisa2009train.csv")
str(pisa)
summary(pisa)
pisaTrain = read.csv("pisa2009train.csv")
tapply(pisaTrain$readingScore, pisaTrain$male, mean)
is.na(pisaTrain$raceeth)
summary(pisaTrain)
pisaTrain = na.omit(pisaTrain)
pisaTest = read.csv("pisa2009test.csv")
pisaTest = na.omit(pisaTest)
str(pisaTrain)
str(pisaTest)
summary(pisaTrain)
table(pisaTrain$raceeth)
sapply(pisa, function(x)all(is.na(x)))
sapply(pisa, function(x)any(is.na(x)))
pisaTrain$raceeth = relevel(pisaTrain$raceeth, "White")
pisaTest$raceeth = relevel(pisaTest$raceeth, "White")
str(pisaTrain)
str(pisa)
str(pisaTrain)
lmScore = lm(readingScore ~. , data = pisaTrain )
summary(lmScore)
sqrt(0.3251)
SSE = mean((lmScore$residuals)^2)
SSE
RMSE = sqrt(SSE/nrow(pisaTrain))
RMSE
mean(pisaTest$readingScore)
SSE/nrow(pisaTrain)
SSE = sum(lmScore$residuals^2)
RMSE = sqrt(SSE/nrow(pisaTrain))
RMSE
SSE
plot(pisaTrain$readingScore, pisaTrain$raceeth)
plot(pisaTrain$raceeth, pisaTrain$readingScore)
table(pisaTrain$raceeth)
?relevel
lmScore1 = lm(readingScore ~. , data = pisa )
summary(lmScore1)
summary(lmScore1)
summary(lmScore)
table(pisa$raceeth)
predTest = predict(lmScore, pisaTest)
summary(predTest)
637.7 - 353.2
SSE = sum( (predTest - pisaTest$readingScore)^2)
SSE
SST = sum( (mean(pisaTrain$readingScore) - pisaTest$readingScore)^2)
1 - SSE/SST
R2 = 1 - SSE/SST
RMSE = sqrt(SSE/nrow(pisaTest))
RMSE
mean(pisaTrain$readingScore)
SST
summary(lmScore)
R2
savehistory("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec2/HW2.R")
