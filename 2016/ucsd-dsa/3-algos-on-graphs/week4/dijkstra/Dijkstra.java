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

public class Dijkstra {

   public static class MinIndexedPQ<Value extends Comparable<Value>> {
      private int       maxN;      // maximum number of elements on PQ
      private int       n;         // number of elements on PQ
      private int[]     pq;        // binary heap using 1-based indexing
      private int[]     qp;        // inverse of pq - qp[pq[i]] = pq[qp[i]] = i
      private Value[]   values;    // values[i] = priority of i

      // Initializes an empty indexed priority queue with indices between 0 and maxN - 1
      public MinIndexedPQ(int maxN) {
         if (maxN < 0) throw new IllegalArgumentException();
         this.maxN = maxN;
         n = 0;
         values = (Value[]) new Comparable[maxN + 1];    // make this of length maxN??
         pq   = new int[maxN + 1];
         qp   = new int[maxN + 1];                   // make this of length maxN??
         for (int i = 0; i <= maxN; i++)
            qp[i] = -1;
      }

      // Returns true if this priority queue is empty.
      public boolean isEmpty() {
         return n == 0;
      }

      // Is i an index on this priority queue?
      public boolean contains(int i) {
         if (i < 0 || i >= maxN) throw new IndexOutOfBoundsException();
         return qp[i] != -1;
      }

      // Returns the number of values on this priority queue.
      public int size() {
         return n;
      }

      // Associates value with index i
      public void insert(int i, Value value) {
         if (i < 0 || i >= maxN) throw new IndexOutOfBoundsException();
         if (contains(i)) throw new IllegalArgumentException("index is already in the priority queue");
         n++;
         qp[i] = n;
         pq[n] = i;
         values[i] = value;
         swim(n);
      }

      // Returns an index associated with a minimum value.
      public int minIndex() {
         if (n == 0) throw new NoSuchElementException("Priority queue underflow");
         return pq[1];
      }

      // Returns a minimum value.
      public Value minKey() {
         if (n == 0) throw new NoSuchElementException("Priority queue underflow");
         return values[pq[1]];
      }
      public int minKeyIndex() {
         if (n == 0) throw new NoSuchElementException("Priority queue underflow");
         return pq[1];
      }

      // Removes a minimum value and returns its associated index.
      public int delMin() {
         if (n == 0) throw new NoSuchElementException("Priority queue underflow");
         int min = pq[1];
         exch(1, n--);
         sink(1);
         assert min == pq[n + 1];
         qp[min] = -1;        // delete
         values[min] = null;    // to help with garbage collection
         pq[n + 1] = -1;      // not needed
         return min;
      }

      // Returns the value associated with index i
      public Value keyOf(int i) {
         if (i < 0 || i >= maxN) throw new IndexOutOfBoundsException();
         if (!contains(i)) throw new NoSuchElementException("index is not in the priority queue");
         else return values[i];
      }

      // Change the value associated with index i to the specified value.
      public void changeKey(int i, Value value) {
         if (i < 0 || i >= maxN) throw new IndexOutOfBoundsException();
         if (!contains(i)) throw new NoSuchElementException("index is not in the priority queue");
         values[i] = value;
         swim(qp[i]);
         sink(qp[i]);
      }

      // Remove the value associated with index i
      public void delete(int i) {
         if (i < 0 || i >= maxN) throw new IndexOutOfBoundsException();
         if (!contains(i)) throw new NoSuchElementException("index is not in the priority queue");
         int index = qp[i];
         exch(index, n--);
         swim(index);
         sink(index);
         values[i] = null;
         qp[i] = -1;
      }

      // add element with index i
      public void enqueue(int i, Value value) {
         if (contains(i)) {
            changeKey(i, value);
         } else {
            insert(i, value);
         }
      }

      // remove min element
      public int dequeue() {
         int min_key = minKeyIndex();
         delMin();
         return min_key;
      }

      // General helper functions.
      private boolean greater(int i, int j) {
         return values[pq[i]].compareTo(values[pq[j]]) > 0;
      }
      private boolean lesser(int i, int j) {
         return values[pq[i]].compareTo(values[pq[j]]) < 0;
      }

      private void exch(int i, int j) {
         int swap = pq[i];
         pq[i] = pq[j];
         pq[j] = swap;
         qp[pq[i]] = i;
         qp[pq[j]] = j;
      }

      // Heap helper functions.
      private void swim(int k) {
         while (k > 1 && greater(k / 2, k)) {
            exch(k, k / 2);
            k = k / 2;
         }
      }

      private void sink(int k) {
         while (2 * k <= n) {
            int j = 2 * k;
            if (j < n && greater(j, j + 1)) j++;
            if (!greater(k, j)) break;
            exch(k, j);
            k = j;
         }
      }

      // print pq in ascending order
      public void printPQ() {
         // create a new pq
         MinIndexedPQ<Value> copy;
         // add all elements to copy of heap
         // takes linear time since already in heap order so no values move
         copy = new MinIndexedPQ<Value>(pq.length - 1);
         for (int i = 1; i <= n; i++)
            copy.insert(pq[i], values[pq[i]]);

         while (!copy.isEmpty()) {
            Value min_key = copy.minKey();
            int min_i = copy.minKeyIndex();
            copy.delMin();
            System.out.print("(" + min_i + "," + min_key + ") ");
         }
         System.out.println();
      }
   }

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, ArrayList<Integer>> cost_adj_list;
   static int[] distances;

   private static int distance(int s, int t) {

      int n = adjacent_list.size();

      MinIndexedPQ<Integer> fringe = new MinIndexedPQ<Integer>(n);

      distances[s] = 0;
      fringe.enqueue(s, 0);

      // System.out.println("============================");
      // System.out.println(adjacent_list);
      // System.out.println(cost_adj_list);

      while (!fringe.isEmpty()) {
         // System.out.println("\n============================");
         // System.out.print("PQ=> ");
         // fringe.printPQ();
         // System.out.print("b4 dis=> ");
         // for (int i = 0; i < n; i++) System.out.print(i+"->"+distances[i] + " ");
         // System.out.println();

         int u = fringe.dequeue();
         // System.out.println("neigh of "+u + " => " + adjacent_list.get(u));

         for (int v_i = 0; v_i < adjacent_list.get(u).size(); v_i++) {
            int v = adjacent_list.get(u).get(v_i);

            // System.out.print("[" + u + "->" +v + "(" + cost_adj_list.get(u).get(v_i) + ")]");

            int new_dis_uv = distances[u] + cost_adj_list.get(u).get(v_i);

            if (distances[v] > distances[u] && distances[v] > new_dis_uv) {
               // System.out.println("update "+ u + "->" +v +" with "+new_dis_uv);
               fringe.enqueue(v, new_dis_uv);
               distances[v] = new_dis_uv;
            }
         }

         // System.out.println("aft dis=> ");
         // for (int i = 0; i < n; i++) System.out.print(i+"->"+distances[i] + " ");
         // System.out.println();

      }

      if (distances[t] == Integer.MAX_VALUE) {
         return -1;
      } else {
         return distances[t];
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

      int x = scanner.nextInt() - 1;
      int y = scanner.nextInt() - 1;
      System.out.println(distance(x, y));
   }
}

