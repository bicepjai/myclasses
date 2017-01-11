import objsets._

//import TweetReader._

var i = 0
var jayTwSet = new Empty incl new Tweet("jay", "jay-tweet0", 0)
for (i <- 1 to 4) jayTwSet = jayTwSet incl new Tweet("jay", "jay-tweet" + i, i)
var micTwSet = new Empty incl new Tweet("mic", "mic-tweet0", 0)
for (i <- 1 to 4) micTwSet = micTwSet incl new Tweet("mic", "mic-tweet" + i, i)
var unkTwSet = new Empty incl new Tweet("unk", "unk-tweet0", 0)
for (i <- 1 to 2) unkTwSet = unkTwSet incl new Tweet("unk", "unk-tweet" + i, i)
val jaymic = (jayTwSet union micTwSet) union unkTwSet
var twts = new Empty incl new Tweet("user", "user-tweet0", 0)
val end = 101
for (i <- 1 to end) twts = twts incl new Tweet("user", "user-tweet" + i, i)
println(twts)

//
//jayTwSet contains new Tweet("jay", "jay-tweet0", 0)
//micTwSet contains new Tweet("mic", "mic-tweet0", 0)
//jayTwSet contains new Tweet("unk", "unk-tweet0", 0)
//jayTwSet foreach println
//micTwSet foreach println
//jaymic foreach println
//
//
//val jf = jaymic filter ((x: Tweet) => if (x.user == "jay") true else false)
//jf foreach println
//val unkf = jaymic filter ((x: Tweet) => if (x.user == "unk") true else false)
//unkf foreach println
//val mf = jaymic filter ((x: Tweet) => if (x.user == "mic") true else false)
//mf foreach println
//
//val ftwt = twts filter ((x: Tweet) => if (x.text == "user-tweet18") true else false)
//ftwt foreach println
//
//println (twts.mostRetweeted)
//twts = twts remove new Tweet("user", "user-tweet"+end, 399)
//println (twts.mostRetweeted)
//twts = twts remove new Tweet("user", "user-tweet"+(end-1), 399)
//println (twts.mostRetweeted)
