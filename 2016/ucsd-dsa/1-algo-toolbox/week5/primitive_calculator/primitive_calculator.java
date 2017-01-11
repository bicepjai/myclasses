
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
/**
 *
 * @author rpax - Answer to http://stackoverflow.com/a/22428375/3315914
 *
 */
class primitive_calculator {

   public static void main(String[] args) {

      long a = System.currentTimeMillis();
      Object[] sol = solve(932344253,
                           new ArrayList<Integer>(),
                           Integer.MAX_VALUE,
                           new HashMap<Integer, Integer>())
                     .toArray();
      // System.out.println("======ANS=======");
      System.out.println(sol.length);
      System.out.println(Arrays.toString(sol));
      // System.out.println((System.currentTimeMillis() - a));
   }


   public static ArrayList<Integer> solve(int n, ArrayList<Integer> moves, int bestMove, HashMap<Integer, Integer> memory) {

      if (moves.size() >= bestMove) return null;
      if (n == 1) {
         // for(Integer i : moves) System.out.print(i+" ");System.out.println();
         return moves;
      }
      Integer sizeOfPathN = memory.get(n);

      if (sizeOfPathN != null && sizeOfPathN <= moves.size()){
         // System.out.println("sizeOfPathN <= moves.size() ("+n+") sizeOfPathN: "+sizeOfPathN+" moves.size: "+moves.size());
         return null;
      }
      memory.put(n, moves.size());

      int size_1 = Integer.MAX_VALUE, size_2 = Integer.MAX_VALUE, size_3 = Integer.MAX_VALUE;
      ArrayList<Integer> moves3 = null, moves2 = null, moves1;

      if (n % 3 == 0) {
         // System.out.println("---BY_3: "+n);
         ArrayList<Integer> c = new ArrayList<Integer>(moves);
         c.add(n);
         moves3 = solve(n / 3, c, bestMove, memory);
         if (moves3 != null)
            size_3 = moves3.size();
      }

      bestMove = Math.min(bestMove, size_3);

      if (n % 2 == 0) {
         // System.out.println("--BY_2: "+n);
         ArrayList<Integer> c = new ArrayList<Integer>(moves);
         c.add(n);
         moves2 = solve(n / 2, c, bestMove, memory);
         if (moves2 != null)
            size_2 = moves2.size();
      }

      bestMove = Math.min(bestMove, size_2);


      // System.out.println("-BY_1: "+n);
      ArrayList<Integer> c = new ArrayList<Integer>(moves);
      c.add(n);
      moves1 = solve(n - 1, c, bestMove, memory);
      if (moves1 != null)
         size_1 = moves1.size();

      int r = Math.min(Math.min(size_1, size_2), size_3);
      if (r == size_1) return moves1;
      if (r == size_2) return moves2;

      return moves3;

   }


   public static int solve(int n,  int moves, int bestMove, HashMap<Integer, Integer> memory) {

      if (moves >= bestMove) return Integer.MAX_VALUE;
      if (n == 1) return moves;
      Integer sizeOfPathN = memory.get(n);

      if (sizeOfPathN != null && sizeOfPathN <= moves)return Integer.MAX_VALUE;
      memory.put(n, moves);

      int size_1 = Integer.MAX_VALUE;
      int size_2 = Integer.MAX_VALUE;
      int size_3 = Integer.MAX_VALUE;

      moves = moves + 1;

      if (n % 3 == 0) size_3 = solve(n / 3, moves, bestMove, memory);
      bestMove = Math.min(bestMove, size_3);

      if (n % 2 == 0) size_2 = solve(n >> 1, moves, bestMove, memory);
      bestMove = Math.min(bestMove, size_2);

      size_1 = solve(n - 1, moves, bestMove, memory);
      return  Math.min(Math.min(size_1, size_2), size_3);
   }

}
