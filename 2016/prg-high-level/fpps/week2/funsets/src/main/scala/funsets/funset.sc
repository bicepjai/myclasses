
//The bounds for `forall` and `exists` are +/- 1000.
val bound = 1000

type Set = Int => Boolean

def toString(s: Set): String = {
  val xs = for (i <- -bound to bound if contains(s, i)) yield i
  xs.mkString("{", ",", "}")
}

def contains(s: Set, elem: Int): Boolean = s(elem)

def singletonSet(elem: Int): Set =  (x: Int) => if(x == elem) true else false

val s1 = singletonSet(1)
val s2 = singletonSet(2)
val s3 = singletonSet(3)
val s8 = singletonSet(8)

def union(s: Set, t: Set): Set = (x: Int) => contains(s,x) || contains(t,x)

def intersect(s: Set, t: Set): Set = (x: Int) => contains(s,x) && contains(t,x)

def diff(s: Set, t: Set): Set = (x: Int) => contains(s,x) && !contains(t,x)

def even(x: Int):Boolean = x%2.0 == 0
def even3(x: Int):Boolean = x%2.0 == 0 || x == 3

val u11 = union(s1, s1)
val u12 = union(s1, s2)
val u23 = union(s2, s3)
val u13 = union(s1, s3)
val u31 = union(s3, s1)
val u123 = union(union(s1, s2), s3)
val u121 = union(union(s1, s2), s1)
val u211 = union(union(s2, s1), s1)
val u111 = union(union(s1, s1), s1)
val u3218 = union(union(s3, s2), union(s1, s8))

toString(u123)

contains(union(s1, s2), 2)
contains(union(s1, s2), 3)
contains(union(s2, s3), 3)

contains(intersect(u12, u23), 2)
contains(intersect(u11, u23), 2)

contains(diff(u12, u23), 1)
contains(diff(u13, u12), 3)

// Returns the subset of `s` for which `p` holds.
def filter(s: Set, p: Int => Boolean): Set = {
  def iter(a: Int, u: Set): Set = {
    if (a > bound) u
    else if (contains(s, a) && p(a)) iter(a+1, union(u, singletonSet(a)))
    else iter(a+1, u)
  }
  iter(-bound, singletonSet(bound+1))
}

contains(filter(u12, s2), 2)
contains(filter(u12, s3), 3)
contains(filter(u123, s3), 3)
contains(filter(u123, u12), 1)
contains(filter(u123, u13), 1)
contains(filter(u123, u23), 1)
contains(filter(u123, u23), 2)
contains(filter(u123, u23), 3)
toString(filter(u123, u23))
toString(filter(u123, s1))
toString(filter(u3218, even3))


//Returns whether all bounded integers within `s` satisfy `p`.

def forall(s: Set, p: Int => Boolean): Boolean = {
  def iter(a: Int): Boolean = {
    if (a > bound) true
    else if (contains(s, a) && !p(a)) false
    else iter(a+1)
  }
  iter(-bound)
}

val s1000 = singletonSet(1000)

forall(u123, s1000)

forall(u12, s3)
forall(u123, u12)
forall(u23, u12)
forall(u23, u23)

forall(u121, s1)
forall(u111, s1)

def map(s: Set, f: Int => Int): Set = {
  def iter(a: Int, u: Set): Set = {
    if (a > bound) u
    else if (contains(s, a)) iter(a+1, union(u, singletonSet(f(a))))
    else iter(a+1, u)
  }
  iter(-bound, singletonSet(bound+1))
}

toString(map(u123, (x:Int) => x*2))

def exists(s: Set, p: Int => Boolean): Boolean = forall(p,s)


even(8) && !contains(s8, 8)

!even(8)

exists(u31, s1)
forall(u31, s1)
exists(u23, even3)
