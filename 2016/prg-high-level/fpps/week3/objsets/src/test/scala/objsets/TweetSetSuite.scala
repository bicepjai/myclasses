package objsets

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class TweetSetSuite extends FunSuite {
  trait TestSets {
    val set1 = new Empty
    val set2 = set1.incl(new Tweet("a", "a body", 20))
    val set3 = set2.incl(new Tweet("b", "b body", 20))
    val c = new Tweet("c", "c body", 7)
    val d = new Tweet("d", "d body", 9)
    val set4c = set3.incl(c)
    val set4d = set3.incl(d)
    val set5 = set4c.incl(d)

    var i = 0
    var jayTwSet = new Empty incl new Tweet("jay", "jay-tweet0", 0)
    for (i <- 1 to 4) jayTwSet = jayTwSet incl new Tweet("jay", "jay-tweet" + i, i)
    var micTwSet = new Empty incl new Tweet("mic", "mic-tweet0", 0)
    for (i <- 1 to 4) micTwSet = micTwSet incl new Tweet("mic", "mic-tweet" + i, i)
    var unkTwSet = new Empty incl new Tweet("unk", "unk-tweet0", 0)
    for (i <- 1 to 2) unkTwSet = unkTwSet incl new Tweet("unk", "unk-tweet" + i, i)

    var twts = new Empty incl new Tweet("user", "user-tweet0", 0)
    for (i <- 1 to 100) twts = twts incl new Tweet("user", "user-tweet" + i, i)
    for (i <- 101 to 200) twts = twts incl new Tweet("user", "user-tweet" + i, i)
    for (i <- 201 to 300) twts = twts incl new Tweet("user", "user-tweet" + i, i)
    for (i <- 301 to 500) twts = twts incl new Tweet("user", "user-tweet" + i, i)

    val jaymic = jayTwSet union micTwSet
  }

  def asSet(tweets: TweetSet): Set[Tweet] = {
    var res = Set[Tweet]()
    tweets.foreach(res += _)
    res
  }

  def size(set: TweetSet): Int = asSet(set).size

  test("filter: on empty set") {
    new TestSets {
      assert(size(set1.filter(tw => tw.user == "a")) === 0)
    }
  }

  test("filter: a on set5") {
    new TestSets {
      assert(size(set5.filter(tw => tw.user == "a")) === 1)
    }
  }

  test("filter: 20 on set5") {
    new TestSets {
      assert(size(set5.filter(tw => tw.retweets == 20)) === 2)
    }
  }

  test("union: set4c and set4d") {
    new TestSets {
      assert(size(set4c.union(set4d)) === 4)
    }
  }

  test("union: with empty set (1)") {
    new TestSets {
      assert(size(set5.union(set1)) === 4)
    }
  }

  test("union: with empty set (2)") {
    new TestSets {
      assert(size(set1.union(set5)) === 4)
    }
  }

  test("descending: set5") {
    new TestSets {
      val trends = set5.descendingByRetweet
      assert(!trends.isEmpty)
      assert(trends.head.user == "a" || trends.head.user == "b")
    }
  }

  test("jayTests: union") {
    new TestSets {
      assert(jayTwSet contains new Tweet("jay", "jay-tweet0", 0))
      assert(micTwSet contains new Tweet("mic", "mic-tweet0", 0))
      assert(!(jayTwSet contains new Tweet("unk", "unk-tweet0", 0)))
    }
  }

  test("jayTests: filter") {
    new TestSets {
      val jf = jaymic filter ((x: Tweet) => if (x.user == "jay") true else false)
      val mf = jaymic filter ((x: Tweet) => if (x.user == "mic") true else false)
      val uf = twts filter ((x: Tweet) => if (x.text == "user-tweet300" || x.text == "user-tweet89") true else false)

      assert(jf contains new Tweet("jay", "jay-tweet0", 0))
      assert(mf contains new Tweet("mic", "mic-tweet0", 0))
      assert(!(jf contains new Tweet("unk", "unk-tweet0", 0)))
      assert(!(jf contains new Tweet("mic", "mic-tweet0", 0)))

      assert(twts contains new Tweet("user", "user-tweet399", 0))
      assert(twts contains new Tweet("user", "user-tweet500", 0))

      assert(uf contains new Tweet("user", "user-tweet89", 0))
      assert(!(uf contains new Tweet("mic", "mic-tweet90", 0)))
    }
  }

  test("jayTests: mostRetweeted") {
    new TestSets {

      assert(twts contains  new Tweet("user", "user-tweet100", 100))
      assert(twts.mostRetweeted.retweets == 500)
      for (i <- 401 to 500) {
        val twt = twts.mostRetweeted
        twts = twts remove twt
      }
      assert(twts.mostRetweeted.retweets == 400)
      val twts1 = twts remove new Tweet("user", "user-tweet400", 400)
      assert(twts1.mostRetweeted.retweets == 399)
    }
  }

  test("jayTests: descendingByRetweet") {
    new TestSets {
      val twtsList = twts.descendingByRetweet
      assert(twtsList.head.retweets == 500)
    }
  }


  }
