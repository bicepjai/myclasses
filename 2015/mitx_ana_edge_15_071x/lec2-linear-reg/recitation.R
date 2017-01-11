setwd("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec2")
NBA = read.csv("NBA_train.csv")
str(NBA)
table(NBA$W, NBA$Playoffs)
NBA$PTSDiff = NBA$PTS - NBA$oppPTS
plot(NBA$PTSDiff, NBA$W)
WinsReg = lm(W ~ PTSDiff, data=NBA)
summary(WinsReg)
PointsReg = lm(PTS ~ X2PA + X3PA + FTA + AST + ORB + DRB + TOV + STL + BLK, data=NBA)
summary(PointsReg)
summary(PointsReg)
str(PointsReg)
PointsReg$residuals
SSE = sum(PointsReg$residuals^2)
SSE
RMSE = sqrt(SSE/nrows(NBA))
RMSE = sqrt(SSE/nrow(NBA))
RMSE
mean(NBA$PTS)
PointsReg1 = lm(PTS ~ X2PA + X3PA + FTA + AST + ORB + DRB + STL + BLK, data=NBA)
summary(PointsReg1)
SSE1 = sum(PointsReg1$residuals^2)
RMSE1 = sqrt(SSE1/nrow(NBA))
RMSE1
PointsReg2 = lm(PTS ~ X2PA + X3PA + FTA + AST + ORB + STL + BLK, data=NBA)
SSE2 = sum(PointsReg2$residuals^2)
RMSE2 = sqrt(SSE2/nrow(NBA))
RMSE2
summary(PointsReg2)
PointsReg4 = lm(PTS ~ X2PA + X3PA + FTA + AST + ORB + STL, data=NBA)
SSE4 = sum(PointsReg4$residuals^2)
RMSE4 = sqrt(SSE4/nrow(NBA))
RMSE4
summary(PointsReg4)
SSE4
NBATest = read.csv("NBA_test.csv")
str(NBATest)
PointsReg4 = lm(PTS ~ X2PA + X3PA + FTA + AST + ORB + STL, data=NBA)
summary(PointsReg4)
predict(PointsReg4, newdata = NBATest)
PointsPredictions = predict(PointsReg4, newdata = NBATest)
SSE = sum((PointsPredictions - NBATest$PTS)^2)
SST = sum((mean(NBA$PTS) - NBATest$PTS)^2)
R2 = 1 - SSE/SST
R2
RMSE = sqrt(SSE/nrow(NBATest))
RMSE
str(NBA)
str(NBATest)
savehistory("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec2/recitation.R")
