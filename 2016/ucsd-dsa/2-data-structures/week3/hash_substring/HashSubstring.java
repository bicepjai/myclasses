import java.io.*;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.StringTokenizer;
import java.util.Random;
import java.lang.Math;

public class HashSubstring {

   private static FastScanner in;
   private static PrintWriter out;
   // private int bucketCount = 0;
   private static long prime = 1000000007;
   // x in poly hash's a + b.x + c.x^2 + d.x^3 + ...
   private static long x_multiplier = 263;

   public static void main(String[] args) throws IOException {
      in = new FastScanner();
      out = new PrintWriter(new BufferedOutputStream(System.out));
      printOccurrences(getOccurrences(readInput()));
      // testingHashSubstring();
      out.close();

   }

   private static Data readInput() throws IOException {
      String pattern = in.next();
      String text = in.next();
      return new Data(pattern, text);
   }

   public static String generateString(Random rng, String characters, int length) {
      char[] text = new char[length];
      for (int i = 0; i < length; i++) {
         text[i] = characters.charAt(rng.nextInt(characters.length()));
      }
      return new String(text);
   }

   public static void testingHashSubstring() throws IOException {
      String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      while (true) {
         Random rand = new Random();
         long text_n = Math.abs(rand.nextLong() % 600000) + 1;
         long pattern_n = Math.abs(rand.nextLong() % text_n) + 1;
         // out.println(text_n + " " + pattern_n);
         String text = generateString(rand, characters , (int)text_n);
         String pattern = generateString(rand, characters , (int)pattern_n);
         // out.println("text: " + text);
         // out.println("pattern: " + pattern);
         long startTime = System.nanoTime();
         printOccurrences(getOccurrences(new Data(pattern, text)));
         long endTime = System.nanoTime();
         out.println("Time taken: " +  (endTime - startTime));
         out.println();
      }
   }

   private static void printOccurrences(List<Integer> ans) throws IOException {
      for (Integer cur : ans) {
         out.print(cur);
         out.print(" ");
      }
      out.println();
   }

   private static long hashFunc(String s) {
      long hash = 0;
      for (int i = s.length() - 1; i >= 0; --i)
         hash = (hash * x_multiplier + s.charAt(i)) % prime;
      return hash; // % bucketCount;
   }

   private static List<Integer> getOccurrences(Data input) {
      String pattern = input.pattern, text = input.text;
      int pattern_n = pattern.length(), text_n = text.length();
      List<Integer> occurrences = new ArrayList<Integer>();

      // precompute hashses ------------------------
      // compute the x_multiplier raised to the
      // power of length of the pattern and mod prime
      long x_raised_m_mod_p = 1;
      for (int i = 0; i < pattern_n; i++) {
         x_raised_m_mod_p = (x_raised_m_mod_p * x_multiplier) % prime;
      }

      // zero indexed array
      long[] hashArrayText = new long[text_n - pattern_n + 1];
      // store hash of last substring of pattern.length s
      hashArrayText[text_n - pattern_n] = hashFunc(text.substring(text_n - pattern_n, text_n));
      // out.println(text.substring(text_n - pattern_n, text_n));
      for (int i = text_n - pattern_n - 1; i >= 0; i--) {
         hashArrayText[i] = ((((x_multiplier * hashArrayText[i + 1]) % prime) + prime)
                             + ((text.charAt(i) % prime) + prime)
                             // since the ascii value for the character might be large than
                             // x_multiplier
                             - (((x_raised_m_mod_p * text.charAt(i + pattern_n)) % prime) + prime)
                            ) % prime;
         // out.println(i + " adding " + text.charAt(i) + " subtracting " + text.charAt(i + pattern_n) + "=> " + hashArrayText[i]);
      }

      //Rabin Karp Algo ----------------------------
      long patternHash = hashFunc(pattern);
      for (int i = 0; i <= text_n - pattern_n ; i++) {
         // out.println(i + ") " + "(" + hashArrayText[i] + ") ==? " + "(" + patternHash + ")");
         if (patternHash == hashArrayText[i]) {
            String sub_string = text.substring(i, i + pattern_n);
            if (sub_string.equals(pattern)) {
               // out.println(i + ") " + sub_string + "(" + hashArrayText[i] + ") ==? " + pattern + "(" + patternHash + ")");
               occurrences.add(i);
            }
         }
      }

      return occurrences;
   }

   static class Data {
      String pattern;
      String text;
      public Data(String pattern, String text) {
         this.pattern = pattern;
         this.text = text;
      }
   }

   static class FastScanner {
      private BufferedReader reader;
      private StringTokenizer tokenizer;

      public FastScanner() {
         reader = new BufferedReader(new InputStreamReader(System.in));
         tokenizer = null;
      }

      public String next() throws IOException {
         while (tokenizer == null || !tokenizer.hasMoreTokens()) {
            tokenizer = new StringTokenizer(reader.readLine());
         }
         return tokenizer.nextToken();
      }

      public int nextInt() throws IOException {
         return Integer.parseInt(next());
      }
   }
}

