import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Scanner;
import java.util.Stack;
import java.util.Set;
import java.util.Arrays;
import java.util.Collections;

public class Toposort {

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, Boolean> explored_state;

   private static ArrayList<Integer> toposort() {
      ArrayList<Integer> order = new ArrayList<Integer>();
      for (int u : adjacent_list.keySet()) {
         if (!explored_state.get(u)) {
            DfsExplore(order, u);
         }
      }
      return order;
   }

   private static void DfsExplore(ArrayList<Integer> order, int u) {
      explored_state.put(u, true);
      for (int v : adjacent_list.get(u)) {
         if (!explored_state.get(v)) {
            DfsExplore(order, v);
         }
      }
      order.add(u);
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      explored_state = new Hashtable<Integer, Boolean>(n);

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
         explored_state.put(i, false);
      }
      for (int i = 0; i < m; i++) {
         int x, y;
         x = scanner.nextInt();
         y = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
      }

      ArrayList<Integer> order = toposort();
      for (int i = order.size()-1; i >=0 ; i--) {
         System.out.print((order.get(i) + 1) + " ");
      }
   }
}

