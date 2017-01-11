import java.io.*;
import java.util.*;
import java.lang.*;

class Node {
   public static final int Letters =  4;
   public static final int NA      = -1;
   public int next [];
   public boolean[] pattern_end;
   Node () {
      next = new int [Letters];
      Arrays.fill (next, NA);
      pattern_end = new boolean[Letters];
      Arrays.fill (pattern_end, Boolean.FALSE);
   }
}

public class TrieMatchingExtended implements Runnable {
   public static int letterToIndex (char letter) {
      switch (letter) {
      case 'A': return 0;
      case 'C': return 1;
      case 'G': return 2;
      case 'T': return 3;
      default: assert (false); return Node.NA;
      }
   }

   public static char indexToLetter (int index) {
      switch (index) {
      case 0: return 'A';
      case 1: return 'C';
      case 2: return 'G';
      case 3: return 'T';
      default: return 'X';
      }
   }

   public static boolean stressTest() {

      int MAX_TEXT_LEN = 20; //10000;
      int MAX_PATTERN_LEN = 10; //100;
      int MAX_NOF_PATTERNS = 10; ////5000;
      Random random = new Random();

      // randomly generate text
      String acgt = "ACGT";

      int rand_text_len = random.nextInt(MAX_TEXT_LEN) + 1;
      System.out.println("MAX_TEXT_LEN: " + rand_text_len);
      String text = "";
      for (int i = 0; i < rand_text_len; ++i) {
         text += acgt.charAt(random.nextInt(acgt.length()));
      }
      System.out.println("Text:" + text);

      // randomly generate patterns
      List <String> patterns = new ArrayList <String> ();
      int rand_nof_patterns = random.nextInt(MAX_NOF_PATTERNS) + 1;
      System.out.println("MAX_NOF_PATTERNS: " + rand_nof_patterns);

      for (int i = 0; i < rand_nof_patterns; ++i) {
         int rand_pattern_len = random.nextInt(MAX_PATTERN_LEN + 1) + 1;
         String pattern = "";
         for (int j = 0; j < rand_pattern_len; ++j) {
            pattern += acgt.charAt(random.nextInt(acgt.length()));
         }
         patterns.add(pattern);
      }
      System.out.println(patterns);

      List <Integer> indices = new ArrayList <Integer> ();
      for (String pattern : patterns) {
         int index = text.indexOf(pattern);
         while (index >= 0) {
            if (!indices.contains(index)) {
               indices.add(index);
            }
            index = text.indexOf(pattern, index + 1);
         }
      }

      Collections.sort(indices);
      List <Integer> result = solve (text, rand_nof_patterns, patterns);

      boolean status = false;
      System.out.println("\n----Stress Test Result-----------------------");
      if (indices.equals(result)) {
         System.out.println("Test Passed");
         status = true;
      } else {
         System.out.println(text);
         System.out.println(patterns.size());
         for (String pattern : patterns) {
            System.out.println(pattern);
         }
         System.out.println("Answer:" + indices);
         System.out.println("Ours  :" + result);
         System.out.println("Test Failed");
         status = false;
      }
      System.out.println("---------------------------------------------");
      return status;
   }


   public static List <Integer> solve (String text, int n, List <String> patterns) {

      Map<Integer, Node> trie;
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
            int acgt_index = letterToIndex(current_symbol);

            if (i == pattern.length() - 1) {
               node.pattern_end[acgt_index] = true;
            }

            // get the next node index from the array or 4 chars
            int next_node_index = node.next[acgt_index];
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
               node.next[acgt_index] = trie_size - 1;
               current_node_index = trie_size - 1;
            }
         }
      }
      // print(trie);

      // matching patterns
      for (int i = 0; i < text.length(); i++) {
         // System.out.println("-------------------------------");
         // System.out.println("At " + i + " " + text.substring(i));
         if (prefixTrieMatching(text.substring(i), trie)) {
            result.add(i);
            // System.out.println(" -> found " + i);
         }
      }

      return result;
   }

   public static boolean prefixTrieMatching(String text, Map<Integer, Node> trie) {
      if (text.isEmpty())
         return false;
      int current_symbol_index = 0;
      int current_node_index = 0; // root
      char current_symbol = text.charAt(current_symbol_index);

      Node node;
      Node prev_node = null;
      int acgt_index = Node.NA;
      while (true) {
         node = trie.get(current_node_index);

         if (current_symbol_index < text.length()) {
            current_symbol = text.charAt(current_symbol_index);
            acgt_index = letterToIndex(current_symbol);
            // System.out.println(" checked " + current_symbol + " at " + current_symbol_index + " ");
         } else {
            break;
         }

         // leaf node
         if ( (node.next[0] == Node.NA &&
               node.next[1] == Node.NA &&
               node.next[2] == Node.NA &&
               node.next[3] == Node.NA)) {
            // System.out.println(" reached leaf");
            return true;
         }
         // there is an edge to the current_symbol from current node
         else if ( node.next[acgt_index] != Node.NA) {

            // if ther3 is some pattern matched on the way to leaf node
            // or mismatch
            if (prev_node == null && node.pattern_end[acgt_index]) {
               // System.out.println(" marked pattern_end");
               prev_node = node;
            }

            // made the current node to the new node found
            // System.out.println(" matched, going to " + node.next[acgt_index]);

            current_node_index = node.next[acgt_index];
            current_symbol_index++;

         }
         // didnt match
         else {
            // System.out.println(" done");
            break;
         }
      }

      if (prev_node != null) {
         // System.out.println(" some pattern matched before");
         return true;
      }

      return false;
   }

   public static void print(Map<Integer, Node> trie) {
      for (int i = 0; i < trie.size(); ++i) {
         Node node = trie.get(i);
         for (int j = 0; j < 4; ++j) {
            if (node.next[j] != Node.NA) {
               System.out.print(i + "->" + indexToLetter(j) + ":" + node.next[j]);
               if (node.pattern_end[j]) {
                  System.out.print(" marking_end");
               }
               System.out.println();
            }
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
      new Thread (new TrieMatchingExtended ()).start ();
      // while (stressTest());
   }
}
