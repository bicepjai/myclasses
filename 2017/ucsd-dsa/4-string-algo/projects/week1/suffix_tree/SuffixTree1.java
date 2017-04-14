import java.util.*;
import java.io.*;
import java.util.zip.CheckedInputStream;

class Node1 {
   public static final int Letters =  5;
   public static final int NA      = -1;
   public int next [];
   public String edge_string [];

   public boolean[] pattern_end;
   Node1 () {
      next = new int [Letters];
      edge_string = new String [Letters];
      Arrays.fill (next, NA);
      pattern_end = new boolean[Letters];
      Arrays.fill (pattern_end, Boolean.FALSE);
   }
}

public class SuffixTree1 {

   class FastScanner {
      StringTokenizer tok = new StringTokenizer("");
      BufferedReader in;

      FastScanner() {
         in = new BufferedReader(new InputStreamReader(System.in));
      }

      String next() throws IOException {
         while (!tok.hasMoreElements())
            tok = new StringTokenizer(in.readLine());
         return tok.nextToken();
      }

      int nextInt() throws IOException {
         return Integer.parseInt(next());
      }
   }

   public static boolean isLeaf (Node1 node) {
      if ( (node.next[0] == Node1.NA &&
            node.next[1] == Node1.NA &&
            node.next[2] == Node1.NA &&
            node.next[3] == Node1.NA &&
            node.next[4] == Node1.NA)) {
         return true;
      } else {
         return false;
      }
   }

   public static int letterToIndex (char letter) {
      switch (letter) {
      case 'A': return 0;
      case 'C': return 1;
      case 'G': return 2;
      case 'T': return 3;
      case '$': return 4;
      default: assert (false); return Node1.NA;
      }
   }

   public static char indexToLetter (int index) {
      switch (index) {
      case 0: return 'A';
      case 1: return 'C';
      case 2: return 'G';
      case 3: return 'T';
      case 4: return '$';
      default: return 'X';
      }
   }

   // Build a suffix tree of the string text and return a list
   // with all of the labels of its edges (the corresponding
   // substrings of the text) in any order.
   public static ArrayList<String> computeSuffixTreeEdges(String text) {
      ArrayList<String> result = new ArrayList<String>();

      // Implement this function yourself
      formTrie(text);

      //**--System.out.println("=================== suffix tree ===================");
      // printTrie();
      //**--System.out.println("=================================================");

      for (int i = 0; i < trie.size(); ++i) {
         Node1 node = trie.get(i);
         for (int j = 0; j < 5; ++j) {
            if (node.next[j] != Node1.NA) {
               result.add(node.edge_string[j]);
            }
         }
      }

      return result;
   }

   // forming the trie
   static Map<Integer, Node1> trie;

   public static void formTrie (String text) {
      trie = new HashMap<Integer, Node1>();
      int trie_size = 0;

      // root node index 0
      // first leaf node index 1
      trie.put(trie_size++, new Node1());
      trie.put(trie_size++, new Node1());
      Node1 root = trie.get(0);
      root.edge_string[letterToIndex(text.charAt(0))] = text;
      root.next[letterToIndex(text.charAt(0))] = 1; // first leaf node


      for (int s_i = text.length() - 1 ; s_i >= 1 ; s_i--) {
         // for (int s_i = 1 ; s_i < text.length() ; s_i++) {

         String suffix = text.substring(s_i);

         //**--System.out.println("-for---------------- " + suffix + " ------------------");
         // print(trie);

         // always start from the root index
         int  cur_node_i = 0;
         Node1 cur_node   = trie.get(cur_node_i);

         // while loop to traverse thru the existing tree
         while (!isLeaf(cur_node)) {
            // printTrie();
            //**--System.out.println("--while------------");

            // get current node
            //**--System.out.println("cur_node_i: " + cur_node_i);
            cur_node = trie.get(cur_node_i);
            // getting branch string details
            Character suffix_start_sym = suffix.charAt(0);
            int       cur_node_acgt_i  = letterToIndex(suffix_start_sym);
            String    edge_string      = cur_node.edge_string[cur_node_acgt_i];

            // get the next node index from the array of 5 chars
            int next_node_i = cur_node.next[cur_node_acgt_i];

            //**--System.out.println("suffix_start_sym: " + suffix_start_sym);
            //**--System.out.println("cur_node_acgt_i: " + cur_node_acgt_i);
            //**--System.out.println("edge_string: " + edge_string);

            // node already exists if cur_node.next index is not Node1.NA
            if (next_node_i != Node1.NA) {

               //**--System.out.println("found edge string: " + edge_string);
               // check for suffix match in the edge_string
               Node1 next_node = trie.get(next_node_i);

               // same pattern condition
               if (edge_string == suffix) {
                  // suffix exist in the suffix tree already
                  // move on to processing the next suffix
                  //**--System.out.println("edge_string == suffix ( " + suffix + " )");
                  break;
               } else {

                  // find the mismatch point between the suffix and edge_string
                  int mismatch_i = 0;
                  while (mismatch_i < suffix.length() &&
                         mismatch_i < edge_string.length() &&
                         suffix.charAt(mismatch_i) == edge_string.charAt(mismatch_i)) {
                     mismatch_i++;
                  }

                  // when mismatch happens and the edge_string
                  // has all the matched characters in the suffix
                  // we set the cur_node_i to the next pointer from the next_node
                  // and continue
                  //**--System.out.println("mismatch_i: " + mismatch_i + " comparing " + suffix + " <> " + edge_string);
                  if (mismatch_i >= edge_string.length()) {
                     cur_node_i = next_node.next[letterToIndex(suffix.charAt(mismatch_i))];
                     String new_suffix = suffix.substring(mismatch_i);
                     suffix = new_suffix;
                     //**--System.out.println("edge string pattern matches " + new_suffix);

                     Character new_suffix_start_sym = suffix.charAt(0);
                     int next_node_acgt_i  = letterToIndex(new_suffix_start_sym);
                     int viable_path_next_node_i = next_node.next[next_node_acgt_i];

                     // checking if the next node has entries for new suffix
                     // start symbol to move on
                     if (viable_path_next_node_i != Node1.NA) {
                        //**--System.out.println("found viable path to continue " + next_node_i);
                        cur_node_i = next_node_i;
                        // suffix = new_suffix;
                     } else {
                        //**--System.out.println("no edge branch with new suffix start symbol exist");

                        //                                  new_suffix
                        //           top_edge_str        /---------------- new_node
                        // cur_node -------------- next_node
                        //                               \---------------- exist
                        //
                        // remaining part in the suffix forms new edge
                        //**--System.out.println("new_suffix:" + new_suffix);

                        // dealing with new_suffix
                        if (new_suffix.length() > 0) {

                           trie.put(trie_size++, new Node1());
                           int new_node_i = trie_size - 1;
                           Node1 new_node  = trie.get(new_node_i);

                           // update next_node next array indices
                           next_node.next[letterToIndex(new_suffix_start_sym)] = new_node_i;
                           // update next_node edge_string array
                           next_node.edge_string[letterToIndex(new_suffix_start_sym)] = new_suffix;

                           cur_node = new_node;
                        }
                     }
                     continue;

                  }

                  int [] next_node_next_pointers = next_node.next.clone();
                  String [] next_node_edge_string_pointers = next_node.edge_string.clone();

                  // the portion matched is same in both suffix and the
                  // edge_string
                  String top_edge_str = suffix.substring(0, mismatch_i);

                  // set current current node edge_string array
                  cur_node.edge_string[cur_node_acgt_i] = top_edge_str;

                  // remaining part in both the suffix and edge_string
                  // forms 2 new branches from the next_node
                  String new_suffix_bottom1_edge_str = suffix.substring(mismatch_i);
                  String new_bottom2_edge_str = edge_string.substring(mismatch_i);

                  //**--System.out.println("new_suffix_bottom1_edge_str:" + new_suffix_bottom1_edge_str);
                  //**--System.out.println("new_bottom2_edge_str:" + new_bottom2_edge_str);

                  //                                  new_suffix_bottom1_edge_str
                  //           top_edge_str        /----------------------- new_suffix_bottom1_node
                  // cur_node -------------- next_node
                  //                               \----------------------- new_bottom2_node
                  //                                  new_bottom2_edge_str

                  // making next_node leaf since its getting updated anyways
                  Arrays.fill(next_node.next, Node1.NA);

                  // dealing with new_suffix_bottom1_edge_str
                  if (new_suffix_bottom1_edge_str.length() > 0) {
                     // get the starting symbol from 2 new branch strings
                     Character new_suffix_bottom1_start_sym = new_suffix_bottom1_edge_str.charAt(0);

                     // for either condition suffix.length() > edge_string.length()
                     // of vice versa we need 2 new nodes
                     trie.put(trie_size++, new Node1());
                     int new_node_suffix_bottom1_edge_i = trie_size - 1;
                     Node1 new_node_suffix_bottom1  = trie.get(new_node_suffix_bottom1_edge_i);

                     // update next_node next array indices
                     next_node.next[letterToIndex(new_suffix_bottom1_start_sym)] = new_node_suffix_bottom1_edge_i;
                     // update next_node edge_string array
                     next_node.edge_string[letterToIndex(new_suffix_bottom1_start_sym)] = new_suffix_bottom1_edge_str;
                  }

                  // dealing with non suffix new_bottom2_edge_str
                  if (new_bottom2_edge_str.length() > 0) {
                     // get the starting symbol from 2 new branch strings
                     Character new_bottom2_start_sym = new_bottom2_edge_str.charAt(0);

                     // for either condition suffix.length() > edge_string.length()
                     // of vice versa we need 2 new nodes
                     trie.put(trie_size++, new Node1());
                     int new_node_bottom2_edge_i = trie_size - 1;
                     Node1 new_node_bottom2  = trie.get(new_node_bottom2_edge_i);


                     // hooking up the next_node branch matching suffix
                     // we dont look into the new_bottom2_edge_str caz u know why
                     // new branches start character and hence acgt_i
                     System.arraycopy( next_node_next_pointers, 0,
                                       new_node_bottom2.next , 0, Node1.Letters );
                     System.arraycopy( next_node_edge_string_pointers, 0,
                                       new_node_bottom2.edge_string , 0, Node1.Letters );

                     // update next_node next array indices
                     next_node.next[letterToIndex(new_bottom2_start_sym)] = new_node_bottom2_edge_i;

                     // update next_node edge_string array
                     next_node.edge_string[letterToIndex(new_bottom2_start_sym)] = new_bottom2_edge_str;

                  }

                  // reached a node where branching was necessary and hence terminate
                  // and deal with new suffix
                  break;
               }

            }
            // node doesnt exist if node.next index is -1
            // add the suffix and move on to the next suffix
            else {
               // if there is no edge to new suffix_start_symbol
               // we create a new node and add it to the trie
               // making edge by putting the new node index in the cur_node_i next array
               // also adding the suffix to the edge_string
               //**--System.out.println("pattern doesnt exists adding new leaf node");
               //**--System.out.println("---------");
               trie.put(trie_size++, new Node1());
               int new_node_added_i = trie_size - 1;
               cur_node.next[cur_node_acgt_i] = new_node_added_i;
               cur_node.edge_string[cur_node_acgt_i] = suffix;
               break;
            }
         } // while

         // printTrie();
      }
   }

   public static void printTrie() {
      for (int i = 0; i < trie.size(); ++i) {
         Node1 node = trie.get(i);
         for (int j = 0; j < 5; ++j) {
            if (node.next[j] != Node1.NA) {
               System.out.print(i + " -> " + indexToLetter(j) + " : " + node.next[j] + " : " + node.edge_string[j]);
               if (isLeaf(node)) {
                  System.out.print(" leaf");
               }
               System.out.println();
            }
         }
      }
   }

   static public void main(String[] args) throws IOException {
      new SuffixTree1().run();
   }

   public void print(List<String> x) {
      for (String a : x) {
         System.out.println(a);
      }
   }

   public void run() throws IOException {
      FastScanner scanner = new FastScanner();
      String text = scanner.next();
      List<String> edges = computeSuffixTreeEdges(text);
      print(edges);
   }
}
