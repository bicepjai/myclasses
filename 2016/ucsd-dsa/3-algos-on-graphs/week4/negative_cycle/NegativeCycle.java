import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Stack;
import java.util.Set;
import java.util.Collections;
import java.util.Comparator;
import java.util.Map.Entry;
import java.util.AbstractMap;
import java.util.NoSuchElementException;

public class NegativeCycle {

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, ArrayList<Integer>> cost_adj_list;
   static int[] distances;

   private static int negativeCycle() {

      int n = adjacent_list.keySet().size();
      distances[0] = 0;
      boolean last_v_update = false;

      // System.out.println("============================");
      // System.out.println(adjacent_list);
      // System.out.println(cost_adj_list);

      // running V iteration one more than V - 1 :)
      for (int i = 0; i < n ; i++) {
         // System.out.println("\n============================ "+n);
         // System.out.print("b4 dis=> ");
         // for (int j = 0; j < n; j++) System.out.print(j + "->" + distances[j] + " ");
         // System.out.println();

         // going thru all the edges
         for (int u = 0; u < n; u++) {
            for (int v_i = 0; v_i < adjacent_list.get(u).size(); v_i++) {
               int v = adjacent_list.get(u).get(v_i);
               int new_dis_uv = cost_adj_list.get(u).get(v_i);
               if ( distances[u] != Integer.MAX_VALUE) {
                  new_dis_uv += distances[u];
               }

               // System.out.print("[" + u + "->" + v + "(" + distances[u] + " + " + cost_adj_list.get(u).get(v_i) + " = " + new_dis_uv + ")]");
               if (distances[v] > new_dis_uv) {
                  // System.out.print(" update " + u + "->" + v + " with " + new_dis_uv);
                  distances[v] = new_dis_uv;
                  if (i == n-1) {
                     // System.out.println("\n*** last_v_update ***");
                     last_v_update = true;
                  }
               }
               // System.out.println();
            }
            // System.out.print("aftr dis=> ");
            // for (int j = 0; j < n; j++) System.out.print(j + "->" + distances[j] + " ");
            // System.out.println();
         }
      }

      // System.out.println("\n============================");
      if (last_v_update) {
         return 1;
      } else {
         return 0;
      }
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      cost_adj_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      distances     = new int[n];

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
         cost_adj_list.put(i, new ArrayList<Integer>());
         distances[i] = Integer.MAX_VALUE;
      }
      for (int i = 0; i < m; i++) {
         int x, y, w;
         x = scanner.nextInt();
         y = scanner.nextInt();
         w = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
         cost_adj_list.get(x - 1).add(w);
      }
      System.out.println(negativeCycle());
   }
}

