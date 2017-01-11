import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Stack;
import java.util.Set;
import java.util.Collections;

public class BFS {

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, Integer> distances;

   private static int distance(int s, int t) {

      Queue<Integer> fringe = new LinkedList<Integer>();
      fringe.offer(s);
      distances.put(s, 0);

      while (!fringe.isEmpty()) {
         int u = fringe.poll();
         for (int v : adjacent_list.get(u)) {
            if (distances.get(v) == Integer.MAX_VALUE) {
               fringe.offer(v);
               distances.put(v, distances.get(u) + 1);
            }
         }
      }

      if (distances.get(t) == Integer.MAX_VALUE) {
         return -1;
      } else {
         return distances.get(t);
      }
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      distances = new Hashtable<Integer, Integer>(n);

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
         distances.put(i, Integer.MAX_VALUE);
      }
      for (int i = 0; i < m; i++) {
         int x, y;
         x = scanner.nextInt();
         y = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
         adjacent_list.get(y - 1).add(x - 1);
      }
      int x = scanner.nextInt() - 1;
      int y = scanner.nextInt() - 1;
      System.out.println(distance(x, y));
   }
}

