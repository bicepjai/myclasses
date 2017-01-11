import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class Trie {
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

   List<Map<Character, Integer>> buildTrie(ArrayList<String> patterns) {
      List<Map<Character, Integer>> trie = new ArrayList<Map<Character, Integer>>();
      trie.add(new HashMap<Character, Integer>()); // empty root at index 0

      for (int p_i = 0; p_i < patterns.size() ; p_i++) {
         int current_node = 0; // 0 is root
         String pattern = patterns.get(p_i);

         for (int i = 0; i < pattern.length() ; i++) {
            Character current_symbol = pattern.charAt(i);
            Map<Character, Integer> adj_list = trie.get(current_node);
            if (adj_list.containsKey(current_symbol)) {
               // if it already exist just make the current node
               // to the other side of the edge
               current_node = adj_list.get(current_symbol);
            } else {
               // if there is no edge to new symbol
               // we create a new node and put new edge from the current node
               // to newly created node
               trie.add(new HashMap<Character, Integer>());
               current_node = trie.size()-1;
               adj_list.put(current_symbol, current_node);
            }
         }
      }

      return trie;
   }

   static public void main(String[] args) throws IOException {
      new Trie().run();
   }

   public void print(List<Map<Character, Integer>> trie) {
      for (int i = 0; i < trie.size(); ++i) {
         Map<Character, Integer> node = trie.get(i);
         for (Map.Entry<Character, Integer> entry : node.entrySet()) {
            System.out.println(i + "->" + entry.getValue() + ":" + entry.getKey());
         }
      }
   }

   public void run() throws IOException {
      FastScanner scanner = new FastScanner();
      int patternsCount = scanner.nextInt();
      ArrayList<String> patterns = new ArrayList<String>();
      for (int i = 0; i < patternsCount; ++i) {
         patterns.add(scanner.next());
      }
      List<Map<Character, Integer>> trie = buildTrie(patterns);
      print(trie);
   }
}
