import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Stack;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.HashMap;
import java.util.Collections;
import java.util.Comparator;
import java.lang.Math;

public class Clustering {


   public static class Edge {
      int u, v;
      double distance;

      Edge(int u, int v) {
         this.u = u;
         this.v = v;
      }

      public String toString() {
         return (this.u + "->" + this.v + "(" + distance + ")");
      }

   }

   // A class to represent a subset for union-find
   public static class UF {
      int parent, rank;
   };

   static UF sets[];

   // Find set of an element i
   // (uses path compression technique)
   private static int find(int i) {
      // find root and make root as parent of i (path compression)
      if (sets[i].parent != i)
         sets[i].parent = find(sets[i].parent);

      return sets[i].parent;
   }

   // union of two sets of x and y
   // (uses union by rank)
   private static void union(int x, int y) {
      int xroot = find(x);
      int yroot = find(y);

      // Attach smaller rank tree under root of high rank tree
      // (Union by Rank)
      if (sets[xroot].rank < sets[yroot].rank)
         sets[xroot].parent = yroot;
      else if (sets[xroot].rank > sets[yroot].rank)
         sets[yroot].parent = xroot;

      // If ranks are same, then make one as root and increment
      // its rank by one
      else {
         sets[yroot].parent = xroot;
         sets[xroot].rank++;
      }
   }

   private static double clustering(int[] x, int[] y, int k) {
      double result = 0.;
      int n = x.length;

      // priority queue the return all the edges by minimum distance
      PriorityQueue<Edge> edges =
      new PriorityQueue<Edge>(n, new Comparator<Edge>() {
         public int compare(Edge e1, Edge e2) {
            return (e1.distance > e2.distance ? 1 : -1);
         }
      });

      // forming edges
      for (int i = 0; i < n; i++) {
         for (int j = i; j < n; j++) {
            // avoid self loop
            if (i == j) {
               continue;
            }

            Edge e = new Edge(i, j);
            e.distance = Math.sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
            edges.add(e);
         }
      }

      // System.out.println(edges);

      // Creating sets
      sets = new UF[n];
      for (int i = 0; i < n; i++)
         sets[i] = new UF();

      // Create V sets with single elements
      for (int u = 0; u < n; ++u) {
         sets[u].parent = u;
         sets[u].rank = 0;
      }

      // kruskals
      int i = 0;
      while (!edges.isEmpty()) {
         Edge e = edges.poll();
         int u_root = find(e.u);
         int v_root = find(e.v);
         if (u_root != v_root) {
            union(e.u, e.v);
            // n-1 edge is the shortest edge connecting 2 clusters
            // n-1 and n-2 edge are the shortest edges connecting 3 clusters
            // and so on
            if (i++ == n-k) {
               result = e.distance;
            }
         }
      }

      return result;
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int[] x = new int[n];
      int[] y = new int[n];
      for (int i = 0; i < n; i++) {
         x[i] = scanner.nextInt();
         y[i] = scanner.nextInt();
      }
      int k = scanner.nextInt();
      System.out.println(clustering(x, y, k));
   }
}

