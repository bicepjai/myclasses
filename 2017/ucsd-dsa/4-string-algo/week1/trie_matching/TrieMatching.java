import java.io.*;
import java.util.*;

class Node {
   public static final int Letters =  4;
   public static final int NA      = -1;
   public int next [];

   Node () {
      next = new int [Letters];
      Arrays.fill (next, NA);
   }
}

public class TrieMatching implements Runnable {
   int letterToIndex (char letter) {
      switch (letter) {
      case 'A': return 0;
      case 'C': return 1;
      case 'G': return 2;
      case 'T': return 3;
      default: assert (false); return Node.NA;
      }
   }

   char indexToLetter (int index) {
      switch (index) {
      case 0: return 'A';
      case 1: return 'C';
      case 2: return 'G';
      case 3: return 'T';
      default: return 'X';
      }
   }

   Map<Integer, Node> trie;
   List <Integer> solve (String text, int n, List <String> patterns) {
      List <Integer> result = new ArrayList <Integer> ();

      // forming the trie
      trie = new HashMap<Integer, Node>();
      int trie_size = 0;
      trie.put(trie_size++, new Node()); // root at index 0

      for (int p_i = 0; p_i < patterns.size() ; p_i++) {
         int current_node_index = 0; // 0 is root index
         String pattern = patterns.get(p_i);

         for (int i = 0; i < pattern.length() ; i++) {
            Character current_symbol = pattern.charAt(i);

            Node node = trie.get(current_node_index);
            // get the next node index from the array or 4 chars
            int next_node_index = node.next[letterToIndex(current_symbol)];
            // already exists if node.next index is non -1
            if (next_node_index != Node.NA) {
               // if it already exist just make the current node
               // to the other side of the edge
               current_node_index = next_node_index;
            }
            // doesnt exist if node.next index is -1
            else {
               // if there is no edge to new symbol
               // we create a new node and add it to the trie
               // making edge by putting the new node index in the current_node next array
               trie.put(trie_size++, new Node());
               node.next[letterToIndex(current_symbol)] = trie_size - 1;
               current_node_index = trie_size - 1;
            }
         }
      }
      // print();

      // matching patterns
      for (int i = 0; i < text.length(); i++) {
         // System.out.println("-------------------------------");
         // System.out.println(text.substring(i));
         if (prefixTrieMatching(text.substring(i))) {
            result.add(i);
            // System.out.println(" -> found " + i);
         }
      }

      return result;
   }

   boolean prefixTrieMatching(String text) {
      if (text.isEmpty())
         return false;
      int current_symbol_index = 0;
      int current_node_index = 0; // root
      char current_symbol = text.charAt(current_symbol_index);

      while (true) {
         Node node = trie.get(current_node_index);

         if (current_symbol_index < text.length()) {
            current_symbol = text.charAt(current_symbol_index);
            // System.out.println(" checked " + current_symbol + " at " + current_symbol_index + " ");
            // current_symbol_index++;
         }

         // leaf node
         if (node.next[0] == Node.NA &&
               node.next[1] == Node.NA &&
               node.next[2] == Node.NA &&
               node.next[3] == Node.NA) {
            // System.out.println(" reached leaf");
            // in case the text length got over before the leaf
            if(current_symbol_index > text.length())
               return false;
            else
               return true;
         }
         // there is an edge to the current_symbol from current node
         else if ( node.next[letterToIndex(current_symbol)] != Node.NA) {
            // made the current node to the new node found
            current_node_index = node.next[letterToIndex(current_symbol)];
            current_symbol_index++;
            // System.out.println(" matched");
         } else {
            // System.out.println(" done");
            break;
         }



      }

      return false;
   }

   public void print() {
      for (int i = 0; i < trie.size(); ++i) {
         Node node = trie.get(i);
         for (int j = 0; j < 4; ++j) {
            if (node.next[j] != Node.NA)
               System.out.println(i + "->" + indexToLetter(j) + ":" + node.next[j]);
         }
      }
   }

   public void run () {
      try {
         BufferedReader in = new BufferedReader (new InputStreamReader (System.in));
         String text = in.readLine ();
         int n = Integer.parseInt (in.readLine ());
         List <String> patterns = new ArrayList <String> ();
         for (int i = 0; i < n; i++) {
            patterns.add (in.readLine ());
         }

         List <Integer> ans = solve (text, n, patterns);

         for (int j = 0; j < ans.size (); j++) {
            System.out.print ("" + ans.get (j));
            System.out.print (j + 1 < ans.size () ? " " : "\n");
         }
      } catch (Throwable e) {
         e.printStackTrace ();
         System.exit (1);
      }
   }

   public static void main (String [] args) {
      new Thread (new TrieMatching ()).start ();
   }
}
