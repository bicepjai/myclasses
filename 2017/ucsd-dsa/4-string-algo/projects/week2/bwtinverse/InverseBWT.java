import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class InverseBWT {
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

   String inverseBWT(String bwt) {
      StringBuilder result = new StringBuilder();

      // mapping of characters to integer to index into
      // arrays of variables matching characters
      Map<Character, Integer> letter2Index = new HashMap<Character, Integer>();
      letter2Index.put('$', 0);
      letter2Index.put('A', 1);
      letter2Index.put('C', 2);
      letter2Index.put('G', 3);
      letter2Index.put('T', 4);

      // converting character to index
      Character[] chars = {'$', 'A', 'C', 'G', 'T'};

      // this map returns total number of occurrence of
      // each character in the bwt string, this can be used as
      // rank of the character in the first column of BW matrix
      Map<Character, Integer> charCountOnL = new HashMap<Character, Integer>();
      for (int i = 0; i < bwt.length(); i++) {
         Character ch = bwt.charAt(i);
         if (charCountOnL.containsKey(ch)) {
            int rank = charCountOnL.get(ch);
            charCountOnL.put(ch, rank + 1);
         } else {
            charCountOnL.put(ch, 1);
         }
      }

      // building count of the character till the character
      // first occurrence in F
      Map<Character, Integer> countsB4rankOnF = new HashMap<Character, Integer>();
      int prev_chars_count = 0;
      for (Character ch : chars) {
         if (charCountOnL.containsKey(ch)) {
            countsB4rankOnF.put(ch, prev_chars_count);
            prev_chars_count += charCountOnL.get(ch);
         }
      }

      // this array to track which rank among the similar characters are
      // currently processed on L
      int[] current_char_indices_on_L = {0, 0, 0, 0, 0};

      // get the rank of the characters in the bwt i.e., L
      int[] rankL = new int[bwt.length()];
      for (int i = 0; i < bwt.length(); i++) {
         Character ch = bwt.charAt(i);
         rankL[i] = current_char_indices_on_L[letter2Index.get(ch)];
         current_char_indices_on_L[letter2Index.get(ch)]++;
      }

      // System.out.println(Arrays.toString(rankL));
      // System.out.println(countsB4rankOnF);

      // result will have inverse of required string
      result.append('$');

      // this is the character pointed by $ in F to current_ch in L
      Character current_ch = bwt.charAt(0);

      int current_char_rank_on_L = 0;
      int current_char_countsb4_on_F = 0;
      int prev_ch_index_on_L = 0;

      while (current_ch != '$') {
         // System.out.println("\n======== " + result.toString());
         // System.out.println("\n------current_ch " + current_ch);

         result.append(current_ch);

         current_char_rank_on_L = rankL[prev_ch_index_on_L];
         current_char_countsb4_on_F = countsB4rankOnF.get(current_ch);

         // System.out.println("current_char_rank_on_L " + rankL[prev_ch_index_on_L]);
         // System.out.println("current_char_countsb4_on_F " + countsB4rankOnF.get(current_ch));

         prev_ch_index_on_L = current_char_rank_on_L + current_char_countsb4_on_F;
         current_ch = bwt.charAt(prev_ch_index_on_L);

      }

      return result.reverse().toString();
   }

   static public void main(String[] args) throws IOException {
      new InverseBWT().run();
   }

   public void run() throws IOException {
      FastScanner scanner = new FastScanner();
      String bwt = scanner.next();
      System.out.println(inverseBWT(bwt));
   }
}
