import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Scanner;
import java.util.Stack;
import java.util.Set;
import java.util.Arrays;
import java.util.Collections;

public class Acyclicity {

   enum EXPLORE {
      UNKNOWN, // nil state
      WHITE, // not visited
      GRAY,  // currently being exploring
      BLACK, // visit completed
   };

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, EXPLORE> explored_state;

   private static int isAcyclic() {

      // initializing
      for (int u : adjacent_list.keySet())
      {
         explored_state.put(u, EXPLORE.WHITE);
      }

      // exploration of nodes
      for (int u : adjacent_list.keySet())
      {
         if(explored_state.get(u) == EXPLORE.WHITE)
         {
            if(DfsExplore(u))
            {
               return 1;
            }
         }
      }

      return 0;
   }

   private static boolean DfsExplore(int u) {

      explored_state.put(u, EXPLORE.GRAY);
      for (int v : adjacent_list.get(u))
      {
         if(explored_state.get(v) == EXPLORE.GRAY)
         {
            return true; // found cycle
         }
         if(explored_state.get(v) == EXPLORE.WHITE && DfsExplore(v))
         {
            return true;
         }
      }
      explored_state.put(u, EXPLORE.BLACK);

      return false;
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      explored_state = new Hashtable<Integer, EXPLORE>(n);
      // Collections.fill(explored_state, EXPLORE.UNKNOWN);

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
         explored_state.put(i, EXPLORE.UNKNOWN);
      }
      for (int i = 0; i < m; i++) {
         int x, y;
         x = scanner.nextInt();
         y = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
      }

      System.out.println(isAcyclic());
   }
}

