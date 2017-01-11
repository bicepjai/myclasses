abstract class IntSet {
  def incl(x: Int): IntSet
  def contains(x: Int): Boolean
  def union(x: IntSet): IntSet
}

object Empty extends IntSet {
  def contains(x: Int): Boolean = false
  def incl(x: Int): IntSet = new NonEmpty(x, Empty, Empty)
  def union(x: IntSet): IntSet = x
  override def toString = "."
}

class NonEmpty(elem: Int, left: IntSet, right: IntSet) extends IntSet {
  def contains(x: Int): Boolean =
    if (x < elem) left contains x
    else if (x > elem) right contains x
    else true

  def incl(x: Int): IntSet =
    if (x < elem) new NonEmpty(elem, left incl x, right)
    else if (x > elem) new NonEmpty(elem, left, right incl x)
    else this

  override def toString = "{" + left + elem + right + "}"

  def union(x: IntSet): IntSet =
    ((left union right) union x) incl(elem)
}

val ne213 = Empty incl 2 incl 1 incl 3
val ne1 = Empty incl 1
val ne2 = Empty incl 2
val ne3 = Empty incl 3
val ne123 = ne1 union ne2 union ne3

ne1.contains(2)
ne1.contains(1)

(new NonEmpty(7, Empty, Empty)) contains 7


"abc" compareTo "aac"
"abc" < "aac"
"abc" == "aac"
"aaa" == "aaa"
"bac" > "abc"





