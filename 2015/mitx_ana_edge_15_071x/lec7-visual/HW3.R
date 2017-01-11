
tweets = read.csv("tweets.csv", stringsAsFactors=FALSE)
tweets$Negative = as.factor(tweets$Avg <= -1)
str(tweets)

library(tm)
corpusTweets = Corpus(VectorSource(tweets$Tweet))
corpusTweets = tm_map(corpusTweets, PlainTextDocument)
# corpusTweets = tm_map(corpusTweets, tolower)
corpusTweets <- tm_map(corpusTweets, content_transformer(tolower))
corpusTweets = tm_map(corpusTweets, removePunctuation)
corpusTweets = tm_map(corpusTweets, removeWords, stopwords("english"))
# corpusTweets = tm_map(corpusTweets, stemDocument)
# corpusTweets = removeSparseTerms(corpusTweets, 0.95)
tweetDtm = DocumentTermMatrix(corpusTweets)
allTweets = as.data.frame(as.matrix(tweetDtm))

library(wordcloud)

wordcloud(colnames(allTweets), as.numeric(colSums(allTweets)), scale=c(3, 0.5))

corpusTweets = tm_map(corpusTweets, removeWords, c("apple", stopwords("english")))
tweetDtm = DocumentTermMatrix(corpusTweets)
allTweets = as.data.frame(as.matrix(tweetDtm))
allTweets$Negative = tweets$Negative
negAllTweets = subset(allTweets, Negative == TRUE)
allTweets$Negative = NULL
negAllTweets$Negative = NULL

# word cloud A
wordcloud(colnames(allTweets), as.numeric(colSums(allTweets)), scale=c(3, 0.5))

# word cloud B
wordcloud(colnames(allTweets), as.numeric(colSums(allTweets)), scale=c(3, 0.5), min.freq = 10, random.order = FALSE, rot.per = 0.05)

# wordcloud C
wordcloud(colnames(negAllTweets), as.numeric(colSums(negAllTweets)), scale=c(3, 0.5), colors = "blue", rot.per = 0.5)

# wordcloud D
wordcloud(colnames(allTweets), as.numeric(colSums(allTweets)), scale=c(3, 0.5), random.order = FALSE, min.freq = 10, colors=c("purple1", "purple4"))

library(RColorBrewer)
display.brewer.all()
wordcloud(colnames(allTweets), as.numeric(colSums(allTweets)), scale=c(3, 0.5), colors = brewer.pal(9, "Blues"))

