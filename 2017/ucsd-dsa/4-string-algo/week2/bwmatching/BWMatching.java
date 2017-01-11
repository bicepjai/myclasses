import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class BWMatching {
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

   // Preprocess the Burrows-Wheeler Transform bwt of some text
   // and compute as a result:
   //   * starts - for each character C in bwt, starts[C] is the first position
   //       of this character in the sorted array of
   //       all characters of the text.
   //   * occ_count_before - for each character C in bwt and each position P in bwt,
   //       occ_count_before[C][P] is the number of occurrences of character C in bwt
   //       from position 0 to position P inclusive.
   private void PreprocessBWT(String bwt, Map<Character, Integer> starts, Map<Character, int[]> occ_counts_before) {

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

      //------------------ starts --------------
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
      int prev_chars_count = 0;
      for (Character ch : chars) {
         if (charCountOnL.containsKey(ch)) {
            starts.put(ch, prev_chars_count);
            prev_chars_count += charCountOnL.get(ch);
         }
         else {
            starts.put(ch, 0);
         }
      }

      //------------------ occ_count_before --------------
      int counts = 0;
      int bwt_length = bwt.length();
                       // accounting counts including the position of 1st occurrence
      for (Character ch : chars) {
         counts = 0;
         occ_counts_before.put(ch, new int[bwt_length + 1]);
         occ_counts_before.get(ch)[0] = 0;

         for (int bwt_i = 1; bwt_i < bwt_length + 1; bwt_i++) {
            // update before condn checking is necessary
            if (bwt.charAt(bwt_i-1) == ch) {
               counts++;
            }
            occ_counts_before.get(ch)[bwt_i] = counts;
         }
      }

      // System.out.println(bwt);
      // System.out.println(starts);
      // for (Character ch : occ_counts_before.keySet()) {
      //    System.out.println(ch + " -> " + Arrays.toString(occ_counts_before.get(ch)));
      // }
   }

   // Compute the number of occurrences of string pattern in the text
   // given only
   // Burrows-Wheeler Transform bwt of the text and additional
   // information we get from the preprocessing stage - starts and occ_counts_before.
   int CountOccurrences(String pattern, String bwt, Map<Character, Integer> starts, Map<Character, int[]> occ_counts_before) {

      // System.out.println("-------- " + pattern + " -------");
      int top = 0;
      int bottom = bwt.length() - 1;
      String patern = pattern;
      Character ch;
      while (top <= bottom) {
         if (!patern.isEmpty()) {
            ch = patern.charAt(patern.length() - 1);
            patern = patern.substring(0, patern.length() - 1);

            // System.out.println("ch:" + ch + " b4   top:" + top + " bottom:" + bottom);
            top = starts.get(ch) + occ_counts_before.get(ch)[top];
            bottom = starts.get(ch) + occ_counts_before.get(ch)[bottom + 1] - 1;
            // System.out.println("ch:" + ch + " aftr top:" + top + " bottom:" + bottom);

         } else {
            return bottom - top + 1;
         }

      }
      return 0;
   }

   static public void main(String[] args) throws IOException {
      new BWMatching().run();
   }

   public void print(int[] x) {
      for (int a : x) {
         System.out.print(a + " ");
      }
      System.out.println();
   }

   public void run() throws IOException {
      FastScanner scanner = new FastScanner();
      String bwt = scanner.next();
      // Start of each character in the sorted list of characters of bwt,
      // see the description in the comment about function PreprocessBWT
      Map<Character, Integer> starts = new HashMap<Character, Integer>();
      // Occurrence counts for each character and each position in bwt,
      // see the description in the comment about function PreprocessBWT
      Map<Character, int[]> occ_counts_before = new HashMap<Character, int[]>();
      // Preprocess the BWT once to get starts and occ_count_before.
      // For each pattern, we will then use these precomputed values and
      // spend only O(|pattern|) to find all occurrences of the pattern
      // in the text instead of O(|pattern| + |text|).
      PreprocessBWT(bwt, starts, occ_counts_before);
      int patternCount = scanner.nextInt();
      String[] patterns = new String[patternCount];
      int[] result = new int[patternCount];
      for (int i = 0; i < patternCount; ++i) {
         patterns[i] = scanner.next();
         result[i] = CountOccurrences(patterns[i], bwt, starts, occ_counts_before);
      }
      print(result);
   }
}
