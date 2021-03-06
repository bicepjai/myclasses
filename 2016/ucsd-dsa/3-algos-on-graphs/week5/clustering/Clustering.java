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
      int[] parents;
      int[] ranks;

      UF(int n) {
         this.parents = new int[n];
         this.ranks = new int[n];

         // Create V sets with single elements
         for (int u = 0; u < n; ++u) {
            this.parents[u] = u;
            this.ranks[u] = 0;
         }
      }

      // Find set of an element i
      // (uses path compression technique)
      public int find(int i) {
         // find root and make root as parent of i (path compression)
         if (this.parents[i] != i)
            this.parents[i] = find(this.parents[i]);

         return this.parents[i];
      }

      // union of two sets of x and y
      // (uses union by rank)
      public void union(int x, int y) {
         int xroot = this.find(x);
         int yroot = this.find(y);

         // Attach smaller rank tree under root of high rank tree
         // (Union by Rank)
         if (this.ranks[xroot] < this.ranks[yroot])
            this.parents[xroot] = yroot;
         else if (this.ranks[xroot] > this.ranks[yroot])
            this.parents[yroot] = xroot;

         // If ranks are same, then make one as root and increment
         // its rank by one
         else {
            this.parents[yroot] = xroot;
            this.ranks[xroot]++;
         }
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
      UF uf = new UF(n);

      // kruskals
      int i = 0;
      while (!edges.isEmpty()) {
         Edge e = edges.poll();
         int u_root = uf.find(e.u);
         int v_root = uf.find(e.v);
         if (u_root != v_root) {
            uf.union(e.u, e.v);
            // n-1 edge is the shortest edge connecting 2 clusters
            // n-1 and n-2 edge are the shortest edges connecting 3 clusters
            // and so on
            if (i++ == n - k) {
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

