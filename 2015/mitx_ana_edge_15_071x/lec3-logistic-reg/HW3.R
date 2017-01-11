loans1 = read.csv("loans.csv")
str(loans1)
table(loans1$not.fully.paid)
1533/(1533+8045)
summary(loans1)
library(mice)
library(caTools)
library(ROCR)
set.seed(144)
vars.for.imputation = setdiff(names(loans1), "not.fully.paid")
imputed = complete(mice(loans1[vars.for.imputation]))
vars.for.imputation
loans = loans1
loans[vars.for.imputation] = imputed
set.seed(144)
loans = read.csv("loans_imputed.csv")
split = sample.split(loans$not.fully.paid, SplitRatio = 0.7)
train = subset(loans, split == TRUE)
test = subset(loans, split == FALSE)
log1 = glm(not.fully.paid~., data=train, family="binomial")
summary(log1)
(700 - 710)* (-9.308e-03)
exp(700 * (-9.308e-03)) / exp (710 * (-9.308e-03))
pTest = predict(log1, type="response", newdata = test)
predicted.risk = predict(log1, type="response", newdata = test)
test_p$predicted.risk = predicted.risk
test_p = test
test_p$predicted.risk = predicted.risk
str(test_p)
table(test$not.fully.paid, pTest > 0.5)
table(test$not.fully.paid, pTest >= 0.5)
(2387 + 3) / (2387 + 3 + 12 + 455)
table(test$not.fully.paid)
2413/(2413 + 460)
ROCRpTest = prediction(pTest, test$not.fully.paid)
as.numeric(performance(ROCRpTest, "auc")@y.values)
log2 = glm(not.fully.paid~int.rate, data=train, family="binomial")
summary(log1)
summary(log2)
pTest2 = predict(log2, type="response", newdata = test)
ROCRpTest2 = prediction(pTest2, test$not.fully.paid)
as.numeric(performance(ROCRpTest2, "auc")@y.values)
max(pTest2)
table(test$not.fully.paid, pTest2  > 0.5)
table(test$not.fully.paid, pTest1  > 0.5)
table(test$not.fully.paid, pTest  > 0.5)
ROCRpTest2 = prediction(pTest2, test$not.fully.paid)
as.numeric(performance(ROCRpTest2, "auc")@y.values)
10 * exp(3 * 0.06)
test$profit = exp(test$int.rate*3) - 1
test$profit[test$not.fully.paid == 1] = -1
max(test$profit)
str(test)
highInterest = subset(test, int.rate >= 0.15)
str(highInterest)
summary(highInterest$profit)
table(highInterest$not.fully.paid)
110/437
pTest3 = predict(log1, type="response", newdata = highInterest)
highInterest$predicted.risk = pTest3
cutoff = sort(highInterest$predicted.risk, decreasing=FALSE)[100]
cutoff
