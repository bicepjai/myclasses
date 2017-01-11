elantra = read.csv("elantra.csv")
str(elantra)
elantraTrain = subset(elantra, year == 2013)
elantraTrain = subset(elantra, Year == 2013)
elantraTest = subset(elantra, Year == 2014)
str(elantraTrain)
str(elantraTest)
elantraTrain = subset(elantra, Year <= 2012)
elantraTest = subset(elantra, Year >= 2013)
str(elantraTrain)
str(elantraTest)
salesReg1 = lm(ElantraSales ~ Unemployment + CPI_all + CPI_energy + Queries, elantraTrain)
summary(salesReg1)
salesReg2 = lm(ElantraSales ~ Unemployment + CPI_all + CPI_energy + Queries + Month, elantraTrain)
summary(salesReg2)
110.69 * 3
110.69 * 5
110.69 * 2
110.69 * 4
elantraTrain$FMonth = as.factor(elantraTrain$Month)
?as.factor
str(elantraTrain)
salesReg3 = lm(ElantraSales ~ Unemployment + CPI_all + CPI_energy + Queries + Month, elantraTrain)
summary(salesReg3)
salesReg3 = lm(ElantraSales ~ Unemployment + CPI_all + CPI_energy + Queries + FMonth, elantraTrain)
summary(salesReg3)
cor(elantraTrain)
elantraTrain1 = subset(elantra, Year <= 2012)
cor(elantraTrain)
cor(elantraTrain1)
cor(ElantraTrain[c("Unemployment","Month","Queries","CPI_energy","CPI_all")])
salesReg4 = lm(ElantraSales ~ Unemployment + CPI_all + CPI_energy + Month, elantraTrain)
summary(salesReg4)
salesReg4 = lm(ElantraSales ~ Unemployment + CPI_all + CPI_energy + FMonth, elantraTrain)
summary(salesReg4)
predSales = predict(salesReg4, newdata = elantraTest)
elantraTest$FMonth = as.factor(elantraTest$Month)
predSales = predict(salesReg4, newdata = elantraTest)
SSE = sum((predSales - elantraTest$ElantraSales)^2)
SSE
SST = mean(elantraTrain$ElantraSales)
SST
SST = sum((mean(elantraTrain$ElantraSales) - elantraTest$ElantraSales)^2)
SST
mean(elantraTest$ElantraSales)
mean(elantraTrain$ElantraSales)
1 - SSE/SST
RMSE= sqrt(1 - SSE/SST)
RMSE
sqrt(SSE/nrow(elanTraTest))
sqrt(SSE/nrow(elantraTest))
sort(predSales - elantraTest$ElantraSales)
str(elantraTest)
predSales
elantraTest
savehistory("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec2/HW5.R")
