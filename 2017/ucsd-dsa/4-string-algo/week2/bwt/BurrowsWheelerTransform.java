import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class BurrowsWheelerTransform {
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

   public static String rotate(String s, int offset) {
      int i = offset % s.length();
      return s.substring(i) + s.substring(0, i);
   }

   String BWT(String text) {
      StringBuilder result = new StringBuilder();
      ArrayList<String> rotations = new ArrayList<String>();

      // write your code here
      int length = text.length();
      for (int i = 0; i < length; i++) {
         rotations.add(rotate(text, i));
      }

      Collections.sort(rotations);

      for (int i = 0; i < length; i++) {
         result.append(rotations.get(i).charAt(length - 1));
      }

      return result.toString();
   }

   static public void main(String[] args) throws IOException {
      new BurrowsWheelerTransform().run();
   }

   public void run() throws IOException {
      FastScanner scanner = new FastScanner();
      String text = scanner.next();
      System.out.println(BWT(text));
   }
}
