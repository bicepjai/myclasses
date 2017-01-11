
clinical = read.csv("clinical_trial.csv", stringsAsFactors = F)
str(clinical)
max(nchar(clinical$abstract))
noabstrct = subset(clinical, nchar(clinical$abstract) == 0)
noabstrct$abstract
smallTitle = subset(clinical, nchar(clinical$title) == min(nchar(clinical$title)))
smallTitle
min(nchar(clinical$title))

library(tm)
corpusTitle = Corpus(VectorSource(clinical$title))
corpusTitle = tm_map(corpusTitle, tolower)
corpusTitle = tm_map(corpusTitle, PlainTextDocument)
corpusTitle = tm_map(corpusTitle, removePunctuation)
corpusTitle = tm_map(corpusTitle, removeWords, stopwords("english"))
corpusTitle = tm_map(corpusTitle, stemDocument)
dtmTitle = DocumentTermMatrix(corpusTitle)
dtmTitle
dtmTitle = removeSparseTerms(dtmTitle, 0.95)
dtmTitle
dtmTitle = as.data.frame(as.matrix(dtmTitle))
str(dtmTitle)

corpusAbstract = Corpus(VectorSource(clinical$abstract))
corpusAbstract = tm_map(corpusAbstract, tolower)
corpusAbstract = tm_map(corpusAbstract, PlainTextDocument)
corpusAbstract = tm_map(corpusAbstract, removePunctuation)
corpusAbstract = tm_map(corpusAbstract, removeWords, stopwords("english"))
corpusAbstract = tm_map(corpusAbstract, stemDocument)
dtmAbstract = DocumentTermMatrix(corpusAbstract)
dtmAbstract
dtmAbstract = removeSparseTerms(dtmAbstract, 0.95)
dtmAbstract
dtmAbstract = as.data.frame(as.matrix(dtmAbstract))
str(dtmAbstract)

max(colSums(dtmAbstract))
colSums(dtmAbstract)

colnames(dtmTitle) = paste0("T", colnames(dtmTitle))
colnames(dtmAbstract) = paste0("A", colnames(dtmAbstract))

dtm = cbind(dtmTitle, dtmAbstract)
str(dtm)
dtm$trial = clinical$trial
str(dtm)
str(clinical)

library(caTools)
set.seed(144)
spl = sample.split(dtm$trial, 0.7)
train = subset(dtm, spl == TRUE)
test = subset(dtm, spl == FALSE)

table(train$trial)
313/nrow(test)

library(rpart)
library(rpart.plot)
dtmCART = rpart(trial~., data=train, method="class")
prp(dtmCART)

