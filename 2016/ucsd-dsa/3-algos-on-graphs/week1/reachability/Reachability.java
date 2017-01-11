import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Scanner;
import java.util.Stack;
import java.util.Arrays;
import java.util.Collections;

public class Reachability {

   static Hashtable<Integer, ArrayList<Integer>> neighbors;
   static ArrayList<Boolean> visited;

   private static int reach(int u, int v) {

      // System.out.println(neighbors);
      // System.out.println(visited);

      int result = 0;
      Stack<Integer> stack = new Stack<Integer>();
      stack.push(u);
      visited.set(u, Boolean.TRUE);

      while (!stack.empty()) {
         int current = stack.pop();
         for (int i = 0; i < neighbors.get(current).size(); i++) {
            int neighbor = neighbors.get(current).get(i);
            if (visited.get(neighbor) == Boolean.FALSE) {
               if ( neighbor == v) {
                  result = 1;
                  break;
               }
               visited.set(neighbor, Boolean.TRUE);
               stack.push(neighbor);
            }
            if (result == 1) {
               break;
            }
         }
      }

      return result;

   }


   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      neighbors = new Hashtable<Integer, ArrayList<Integer>>(n);
      visited = new ArrayList<Boolean>(Arrays.asList(new Boolean[n]));
      Collections.fill(visited, Boolean.FALSE);

      for (int i = 0; i < n; i++) {
         neighbors.put(i, new ArrayList<Integer>());
      }
      for (int i = 0; i < m; i++) {
         int x, y;
         x = scanner.nextInt();
         y = scanner.nextInt();
         neighbors.get(x - 1).add(y - 1);
         neighbors.get(y - 1).add(x - 1);
      }

      int u = scanner.nextInt() - 1;
      int v = scanner.nextInt() - 1;

      System.out.println(reach(u, v));
   }
}

