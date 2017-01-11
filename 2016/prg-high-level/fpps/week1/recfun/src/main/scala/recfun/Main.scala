package recfun

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
    * Exercise 1
    */
  def pascal(c: Int, r: Int): Int = {
    if (c <= 0 || r <= 0 || c == r) 1
    else pascal(c - 1, r - 1) + pascal(c, r - 1)
  }

  /**
    * Exercise 2
    */
  def balance(chars: List[Char]): Boolean = {

    def matchingBraces(chars: List[Char], stack: List[Char]): Boolean = {
      if (chars.isEmpty) stack.isEmpty
      else if (chars.head == '(') matchingBraces(chars.tail, stack :+ '(')
      else if (chars.head == ')') stack.nonEmpty && stack.head == '(' && matchingBraces(chars.tail, stack.tail)
      else matchingBraces(chars.tail, stack)
    }

    matchingBraces(chars, "".toList)
  }

  /**
    * Exercise 3
    */
  def countChange(money: Int, coins: List[Int]): Int = {

    def denomination(coins: List[Int], noItems: Int, money: Int): Int = {
      if (money == 0) 1
      else if (money < 0) 0
      else if (noItems <= 0 && money >= 1) 0
      else denomination(coins, noItems, money - coins(noItems - 1)) +
        denomination(coins, noItems - 1, money)
    }

    denomination(coins, coins.size, money)
  }
}
