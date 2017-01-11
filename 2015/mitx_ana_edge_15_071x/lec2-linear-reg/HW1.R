climate = read.csv("climate_change.csv")
str(climate)
summary(climate)
climateTrain = subset(Year <= 2006, climate)
?subset
climateTrain = subset(climate, Year <= 2006)
summary(climateTrain)
climateTest = subset(climate, Year > 2006)
summary(climateTest)
Reg1 = lm(Temp ~ MEI+CO2+CH4+N2O+CFC.11+CFC.12+TSI+Aerosols, data = climateTrain)
summary(Reg1)
plot(climate$Temp, climate$Year)
plot(climate$Year, climate$Temp)
cor(climateTrain)
cor(climateTrain$N2O)
Reg2 = lm(Temp ~ MEI+N2O+TSI+Aerosols, data = climateTrain)
summary(Reg2)
?step
ste(Reg1))))
ste(Reg1)
step(Reg1)
str(climate)
step(Reg)
step(Reg1)
Reg3 = lm(formula = Temp ~ MEI + CO2 + N2O + CFC.11 + CFC.12 + TSI +
Aerosols, data = climateTrain)
summary(Reg3)
TempPredictions = predict(Reg3, newdata=climateTest)
TempPredictions
SSE = sum((TempPredictions - climateTest$Temp)^2)
SSE
SST = sum((mean(climate$Temp) - climateTest$Temp)^2)
SST
R2 = 1 - SSE/SST
R2
Reg3 = lm(formula = Temp ~ MEI + CO2 + N2O + CFC.11 + CFC.12 + TSI +
Aerosols, data = climateTrain)
summary(Reg3)
step(Reg1)
TempPredictions = predict(Reg3, newdata=climateTest)
TempPredictions
summary(climateTest)
summary(climate)
TempPredictions = predict(Reg3, newdata=climateTest)
SSE = sum((TempPredictions - climateTest$Temp)^2)
SST = sum((mean(climateTrain$Temp) - climateTest$Temp)^2)
R2 = 1 - SSE/SST
R2
savehistory("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec2/HW1.R")
