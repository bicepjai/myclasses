import java.util.ArrayList;
import java.util.Map.Entry;
import java.util.Map;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Scanner;
import java.util.Stack;
import java.util.Set;
import java.util.Arrays;
import java.util.Collections;
import java.util.stream.*;
import java.util.Comparator;

public class StronglyConnected {

   static HashMap<Integer, ArrayList<Integer>> adjacent_list;
   static HashMap<Integer, ArrayList<Integer>> reverse_adjacent_list;
   static HashMap<Integer, Boolean> explored_state;
   static int post_order_reverse_graph = 0;

   private static void formReverseAdjacencyList() {
      reverse_adjacent_list
         = new HashMap<Integer, ArrayList<Integer>>(adjacent_list.keySet().size());

      for (int u : adjacent_list.keySet()) {
         reverse_adjacent_list.put(u, new ArrayList<Integer>());
      }

      for (int u : adjacent_list.keySet()) {
         for (int v : adjacent_list.get(u)) {
            if (!reverse_adjacent_list.get(v).contains(u)) {
               reverse_adjacent_list.get(v).add(u);
            }
         }
      }
   }

   private static void getPostOrderForReverseGraph(HashMap<Integer, Integer> post_nos_map, int u) {
      explored_state.put(u, true);

      for (int v : reverse_adjacent_list.get(u)) {
         if (!explored_state.get(v)) {
            getPostOrderForReverseGraph(post_nos_map, v);
            post_order_reverse_graph++;
         }
      }
      post_nos_map.put(u, post_order_reverse_graph);
   }

   private static int numberOfStronglyConnectedComponents() {
      // create graph with reverse nodes
      formReverseAdjacencyList();

      // create post order numbers from reversed graph
      // the greatest numbers are the sinks in reverse graph
      // and sources in real graph
      HashMap<Integer, Integer> post_nos_map
         = new HashMap<Integer, Integer>(adjacent_list.keySet().size());

      // running DFS on reverse graph
      post_order_reverse_graph = 0;
      for (int u : reverse_adjacent_list.keySet()) {
         if (!explored_state.get(u)) {
            getPostOrderForReverseGraph(post_nos_map, u);
         }
      }

      // sort the nodes with post order numbers
      // giving all the sources to process in order for real graph
      Map<Integer, Integer> sorted_nodes =
         post_nos_map.entrySet().stream()
         .sorted(Entry.comparingByValue(Comparator.reverseOrder()))
         .collect(Collectors.toMap(Entry::getKey, Entry::getValue,
                                   (e1, e2) -> e1, LinkedHashMap::new));

      // debug
      System.out.println(adjacent_list);
      System.out.println(reverse_adjacent_list);
      System.out.println(post_nos_map);
      System.out.println(sorted_nodes);

      // counting components in real graph
      // resetting explored_state
      for (int u : explored_state.keySet()) {
         explored_state.put(u, false);
      }

      int scc = 0;
      for (int u : sorted_nodes.keySet()) {
         if (!explored_state.get(u)) {
            scc++;
            exploreConnectedComponents(u);
         }
      }



      return scc;
   }

   private static void exploreConnectedComponents(int u) {
      explored_state.put(u, true);
      for (int v : adjacent_list.get(u)) {
         if (!explored_state.get(v)) {
            explored_state.put(v, true);
            exploreConnectedComponents(v);
         }
      }
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new HashMap<Integer, ArrayList<Integer>>(n);
      explored_state = new HashMap<Integer, Boolean>(n);

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
      System.out.println(numberOfStronglyConnectedComponents());
   }
}

