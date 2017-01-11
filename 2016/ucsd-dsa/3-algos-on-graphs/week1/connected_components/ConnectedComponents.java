import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Scanner;
import java.util.Stack;
import java.util.Set;
import java.util.Arrays;
import java.util.Collections;

public class ConnectedComponents {
   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static ArrayList<Boolean> visited;
   static int cc_rec = 0;

   private static int numberOfComponents() {

      // System.out.println(adjacent_list);
      // System.out.println(visited);

      int cc = 0;
      Stack<Integer> stack;
      Set<Integer> nodes = adjacent_list.keySet();
      for (Integer node : nodes) {

         if (visited.get(node) == Boolean.FALSE) {
            cc++;
            stack = new Stack<Integer>();
            stack.push(node);
            visited.set(node, Boolean.TRUE);

            while (!stack.empty()) {
               int current = stack.pop();
               for (int i = 0; i < adjacent_list.get(current).size(); i++) {
                  int neighbor = adjacent_list.get(current).get(i);
                  if (visited.get(neighbor) == Boolean.FALSE) {
                     visited.set(neighbor, Boolean.TRUE);
                     stack.push(neighbor);
                  }

               }
            }
         }
      }
      return cc;
   }

   private static int numberOfComponentsRecursion() {

      // System.out.println(adjacent_list);
      // System.out.println(visited);

      Set<Integer> nodes = adjacent_list.keySet();
      for (Integer node : nodes) {

         if (visited.get(node) == Boolean.FALSE) {
            cc_rec++;
            exploreConnectedComponents(node);
         }
      }
      return cc_rec;
   }

   private static void exploreConnectedComponents(int node) {
      for (int i = 0; i < adjacent_list.get(node).size(); i++) {
         int neighbor = adjacent_list.get(node).get(i);
         if (visited.get(neighbor) == Boolean.FALSE) {
            visited.set(neighbor, Boolean.TRUE);
            exploreConnectedComponents(neighbor);
         }
      }
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      visited = new ArrayList<Boolean>(Arrays.asList(new Boolean[n]));
      Collections.fill(visited, Boolean.FALSE);

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
      }
      for (int i = 0; i < m; i++) {
         int x, y;
         x = scanner.nextInt();
         y = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
         adjacent_list.get(y - 1).add(x - 1);
      }

      // System.out.println(numberOfComponents());
      System.out.println(numberOfComponentsRecursion());
   }
}

