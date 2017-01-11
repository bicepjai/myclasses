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

public class ShortestPaths {

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, ArrayList<Integer>> cost_adj_list;
   static long[] distances;
   static int[] parents;
   static boolean[] incycle, unreachable, visited;

   private static void shortestPaths(int s) {

      int n = adjacent_list.keySet().size();
      distances[s] = 0;
      parents[s] = s;
      int last_updated_v = -1;

      // System.out.println("============================");
      // System.out.println(adjacent_list);
      // System.out.println(cost_adj_list);

      // identifying reachability
      Queue<Integer> fringe = new LinkedList<Integer>();
      fringe.offer(s);
      unreachable[s] = false;

      while (!fringe.isEmpty()) {
         int u = fringe.poll();
         for (int v : adjacent_list.get(u)) {
            // visited same as unreachable array
            if (unreachable[v] == true) {
               fringe.offer(v);
               unreachable[v] = false;
            }
         }
      }

      // running V iteration one more than V - 1 :)
      for (int i = 0; i < n - 1; i++) {

         // System.out.println("\n============================ " + i);
         // System.out.print("b4 dis=> ");
         // for (int j = 0; j < n; j++) System.out.print(j + "->" + distances[j] + " ");
         // System.out.println();

         // going thru all the edges n-1
         for (int u = 0; u < n; u++) {
            for (int v_i = 0; v_i < adjacent_list.get(u).size(); v_i++) {
               int v = adjacent_list.get(u).get(v_i);

               // dont update s
               if ( v == s ) {
                  continue;
               }

               int new_dis_uv = cost_adj_list.get(u).get(v_i);

               if ( distances[u] != Integer.MAX_VALUE) {
                  new_dis_uv += distances[u];
               }

               // System.out.print("[" + u + "->" + v + "(" + distances[u] + " + " + cost_adj_list.get(u).get(v_i) + " = " + new_dis_uv + ")]");

               if (distances[v] > new_dis_uv) {
                  parents[v] = u;
                  // System.out.print(" update " + u + "->" + v + " with " + new_dis_uv);
                  distances[v] = new_dis_uv;
               }
               // System.out.println();
            }

            // System.out.print("aftr dis=> ");
            // for (int j = 0; j < n; j++) System.out.print(j + "->" + distances[j] + " ");
            // System.out.println();
         }
      }

      // getting last edge updated
      // running one extra time to find last_updated_v
      for (int u = 0; u < n; u++) {
         for (int v_i = 0; v_i < adjacent_list.get(u).size(); v_i++) {
            int v = adjacent_list.get(u).get(v_i);

            if ( v == s ) {
               continue;
            }

            int new_dis_uv = cost_adj_list.get(u).get(v_i);

            if ( distances[u] != Integer.MAX_VALUE) {
               new_dis_uv += distances[u];
            }

            if (distances[v] > new_dis_uv) {
               distances[v] = new_dis_uv;
               last_updated_v = v;
            }
         }
      }

      // System.out.println("\n============================ " + last_updated_v);

      boolean[] incycle = new boolean[n];
      for (int i = 0; i < n ; i++) {
         incycle[i] = false;
      }

      // to process marking nodes that are reachable from cycle
      fringe = new LinkedList<Integer>();

      // getting a node in cycle
      int node_in_cycle = last_updated_v;
      for (int i = 0; i < n ; i++) {
         node_in_cycle = parents[node_in_cycle];
      }
      // marking nodes in cycle
      int c = parents[node_in_cycle];
      incycle[c] = true;
      fringe.offer(c);
      while ( node_in_cycle != c) {
         c = parents[c];
         incycle[c] = true;
         fringe.offer(c);
      }

      // to mark nodes that are reachable from cycle
      // System.out.println("fringe: " + (fringe));
      while (!fringe.isEmpty()) {
         int u = fringe.poll();
         for (int v : adjacent_list.get(u)) {
            // visited in this bfs
            if (incycle[v] == false) {
               fringe.offer(v);
               incycle[v] = true;
            }
         }
      }

      // System.out.println("parents: " + Arrays.toString(parents));
      // System.out.println("distances: " + Arrays.toString(distances));
      // System.out.println("distances_cycles: " + Arrays.toString(distances_cycles));
      // System.out.println("incycle: " + Arrays.toString(incycle));

      // System.out.println("\n============================");

      // printing output
      for (int u = 0; u < n ; u++) {
         // unreachable
         if (unreachable[u]) {
            System.out.println("*");
         }
         //if in cycle
         else if (incycle[u]) {
            System.out.println("-");
         }
         //if source
         else if (u == s) {
            System.out.println("0");
         }
         // reachable
         else {
            System.out.println(distances[u]);
         }
      }


   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      cost_adj_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      distances     = new long[n];
      parents           = new int[n];
      incycle           = new boolean[n];
      unreachable       = new boolean[n];
      visited       = new boolean[n];

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
         cost_adj_list.put(i, new ArrayList<Integer>());
         distances[i] = Integer.MAX_VALUE;
         parents[i] = -1;
         incycle[i] = false;
         unreachable[i] = true;
         visited[i] = false;
      }
      for (int i = 0; i < m; i++) {
         int x, y, w;
         x = scanner.nextInt();
         y = scanner.nextInt();
         w = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
         cost_adj_list.get(x - 1).add(w);
      }
      int s = scanner.nextInt();
      shortestPaths(s - 1);
   }
}


