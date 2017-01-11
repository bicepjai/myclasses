poll = read.csv("AnonymityPoll.csv")
str(poll)
table(poll$Smartphone)
is.na(poll$Smartphone)
table(is.na(poll$Smartphone))
table(poll$Smartphone, na.rm=TRUE)
table(poll$Smartphone != "NA")
table(poll$Smartphone)
t = subset(poll$Smartphone, na.rm=TRUE
)
summary(poll$Smartphone)
str(poll$Smartphone)
sum(poll$Smartphone)
sum(poll$Smartphone, na.rm=TRUE)
summary(poll)
table(poll$State, poll$Region)
summary(poll)
table(poll$Internet.Use, poll$Smartphone)
table(is.na(poll$Internet.Use))
table(is.na(poll$Smartphone))
limited =subset(poll, Internet.Use == 1 | Smrtphone == 1)
limited =subset(poll, Internet.Use == 1 | Samrtphone == 1)
limited =subset(poll, Internet.Use == 1 | Smartphone == 1)
str(limietd)
str(limited)
table(is.na(poll$Internet.Use))
table(is.na(poll$Smartphone))
table(is.na(poll$Sex))
table(is.na(poll$Age))
table(is.na(poll$State))
summary(limited)
table(limited$Info.On.Internet)
table(limited$Worry.About.Info)
386/790
table(limited$Anonymity.Possible)
278/753
table(limited$Tried.Masking.Identity)
128/784
table(limited$Privacy.Laws.Effective)
186/727
hist(limited$Age)
plot(limited$Age, limited$Info.On.Internet).
plot(limited$Age, limited$Info.On.Internet)
lines(limited$Age, limited$Info.On.Internet, col="green")
table(limited$Age)
sort(table(limited$Age))
table(tapply(limited$Age == 60, limited$Info.On.Internet))
table(limited$Info.On.Internet)
table(limited$Age == 60, limited$Info.On.Internet)
table(limited$Age == 62, limited$Info.On.Internet)
table(limited$Age, limited$Info.On.Internet)
jitter(c(1, 2, 3))
jitter(c(1, 2, 3))
jitter(c(1, 2, 3))
jitter(c(1, 2, 3))
plot(jitter(limited$Age), jitter(limited$Info.On.Internet))
plot(limited$Age, limited$Info.On.Internet)
plot(limited$Age, limited$Info.On.Internet)
plot(jitter(limited$Age), jitter(limited$Info.On.Internet))
tapply(limited$Smartphone, limited$Info.On.Internet)
tapply(limited$Smartphone, limited$Info.On.Internet, mean)
tapply(limited$Smartphone, limited$Info.On.Internet, mean, na.rm=TRUE)
tapply(limited$Info.On.Internet, limited$Smartphone, mean, na.rm=TRUE)
tapply(limited$Tried.Masking.Identity, limited$Smartphone, mean, na.rm=TRUE)
tapply(limited$Tried.Masking.Identity, limited$Smartphone, na.rm=TRUE)
table(tapply(limited$Tried.Masking.Identity, limited$Smartphone, na.rm=TRUE))
table(tapply(limited$Tried.Masking.Identity, limited$Smartphone, sum, na.rm=TRUE))
table(tapply(limited$Tried.Masking.Identity, limited$Smartphone, nrow, na.rm=TRUE))
285/(285+487)
487/(285+487)
table(tapply(limited$Tried.Masking.Identity, limited$Smartphone))
tapply(limited$Tried.Masking.Identity, limited$Smartphone, mean, na.rm=TRUE)
tapply(limited$Tried.Masking.Identity, limited$Smartphone, mean)
0.1174377/(0.1174377+0.1925466)
0.1925466/(0.1174377+0.1925466)
tapply(limited$Tried.Masking.Identity, limited$Smartphone, na.rm=TRUE)
summary(limited$Smartphone)
summary(limited$Tried.Masking.Identity)
table(tapply(limited$Smartphone, limited$Tried.Masking.Identity, na.rm=TRUE))
table(tapply(limited$Smartphone, limited$Tried.Masking.Identity))
table(limited$Tried.Masking.Identity)
table(limited$Smartphone)
table(tapply(limited$Smartphone, limited$Tried.Masking.Identity == 1))
table(tapply(limited$Smartphone, limited$Tried.Masking.Identity == 0))
table(tapply(limited$Smartphone == 1, limited$Tried.Masking.Identity == 1))
summary(limited$Smartphone)
summary(limited$Tried.Masking.Identity)
table(limited$Smartphone)
table(limited$Tried.Masking.Identity)
table(limited$Smartphone, limited$Tried.Masking.Identity)
str(limited$Tried.Masking.Identity)
summary(limited$Tried.Masking.Identity)
ncol(limited$Tried.Masking.Identity)
nrow(limited$Tried.Masking.Identity)
length(limited$Tried.Masking.Identity)
248+390 + 33 + 93
?table
length(limited$Smartphone)
483/772
281/772
tapply(limited$Tried.Masking.Identity, limited$Smartphone, table)
tapply(limited$Tried.Masking.Identity, limited$Smartphone, summary)
table(limited$Age, limited$Info.On.Internet)
table(limited$Age==18, limited$Info.On.Internet)
data = subset(limited, Age == 18, na.rm=TRUE)
table(data, data$Info.On.Internet)
table(data$Age, data$Info.On.Internet)
table(data$Age, data$Info.On.Internet) > 1
sum(table(data$Age, data$Info.On.Internet) > 1)
data = subset(limited, Age == 19, na.rm=TRUE)
sum(table(data$Age, data$Info.On.Internet) > 1)
data = subset(limited, Age == 20, na.rm=TRUE)
sum(table(data$Age, data$Info.On.Internet) > 1)
for(age in 18:93) {}
for(age in 18:93) {
data = subset(limited, Age == 19, na.rm=TRUE)
}
for(age in 18:93) {
data = subset(limited, Age == age, na.rm=TRUE)
sum(table(data$Age, data$Info.On.Internet) > 1)
}
s = 0
for(age in 18:93) {
data = subset(limited, Age == age, na.rm=TRUE)
s = s + sum(table(data$Age, data$Info.On.Internet) > 1)
}
s
for(age in 18:93) {
data = subset(limited, Age == age, na.rm=TRUE)
s = s + sum(table(data$Age, data$Info.On.Internet) > 1)
s
}
for(age in 18:93) {
data = subset(limited, Age == age, na.rm=TRUE)
s = s + sum(table(data$Age, data$Info.On.Internet) > 1)
print(s)
}
s =0
for(age in 18:93) {
data = subset(limited, Age == age, na.rm=TRUE)
s = s + sum(table(data$Age, data$Info.On.Internet) > 1)
print(s)
}
for(age in 18:93) {
s = s + sum(table(data$Age, data$Info.On.Internet) >= 1)
}
s = 0
for(age in 18:93) {
data = subset(limited, Age == age, na.rm=TRUE)
s = s + sum(table(data$Age, data$Info.On.Internet) >= 1)
print(s)
}
table(limited$Age, limited$Info.On.Internet)
max(table(limited$Age, limited$Info.On.Internet))
savehistory("~/Projects/edx/AnalyticsEdge_MITx15_071x/lec1/HW1_4.R")
