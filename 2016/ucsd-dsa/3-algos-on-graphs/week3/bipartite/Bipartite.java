import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Arrays;
import java.util.Hashtable;
import java.util.Stack;
import java.util.Set;
import java.util.Collections;

public class Bipartite {

   enum COLOR {
      WHITE,
      BLACK,
      RED,
   };

   static Hashtable<Integer, ArrayList<Integer>> adjacent_list;
   static Hashtable<Integer, COLOR> node_color;

   private static int isBiparite() {

      Queue<Integer> fringe = new LinkedList<Integer>();
      fringe.offer(0);
      node_color.put(0, COLOR.BLACK);

      while (!fringe.isEmpty()) {
         int u = fringe.poll();
         for (int v : adjacent_list.get(u)) {
            if (node_color.get(u) == COLOR.RED) {
               if(node_color.get(v) == COLOR.RED) {
                  return 0;
               }
               if(node_color.get(v) == COLOR.WHITE) {
                  fringe.offer(v);
                  node_color.put(v, COLOR.BLACK);
               }
            }
            else if (node_color.get(u) == COLOR.BLACK) {
               if(node_color.get(v) == COLOR.BLACK) {
                  return 0;
               }
               if(node_color.get(v) == COLOR.WHITE) {
                  fringe.offer(v);
                  node_color.put(v, COLOR.RED);
               }
            }
         }
      }

      return 1;
   }

   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in);
      int n = scanner.nextInt();
      int m = scanner.nextInt();

      adjacent_list = new Hashtable<Integer, ArrayList<Integer>>(n);
      node_color = new Hashtable<Integer, COLOR>(n);

      for (int i = 0; i < n; i++) {
         adjacent_list.put(i, new ArrayList<Integer>());
         node_color.put(i, COLOR.WHITE);
      }
      for (int i = 0; i < m; i++) {
         int x, y;
         x = scanner.nextInt();
         y = scanner.nextInt();
         adjacent_list.get(x - 1).add(y - 1);
         adjacent_list.get(y - 1).add(x - 1);
      }
      System.out.println(isBiparite());
   }
}

