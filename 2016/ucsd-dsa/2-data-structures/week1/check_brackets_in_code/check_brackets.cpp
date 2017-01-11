#include <iostream>
#include <cassert>
// #include <ctime>
#include <vector>
#include <algorithm>
#include <tuple>
#include <map>
#include <set>
#include <iterator>
#include <climits>
#include <stack>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;

struct Bracket {

   Bracket(char type, int position):
      type(type),
      position(position)
   {}

   bool Matchc(char c) {
      if (type == '[' && c == ']')
         return true;
      if (type == '{' && c == '}')
         return true;
      if (type == '(' && c == ')')
         return true;
      return false;
   }

   char type;
   int position;
};

int main() {
   std::string text;
   getline(std::cin, text);
   // this variable is useful
   // when we have other characters in mix

   int last_bracet_position = -1;

   std::stack <Bracket> opening_brackets_stack;
   for (int position = 0; position < text.length(); ++position)
   {
      char next = text[position];

      if (next == '(' || next == '[' || next == '{') {
         // Process opening bracket
         Bracket bracket(next, position);
         opening_brackets_stack.push(bracket);
         last_bracet_position = position;
      }

      if (next == ')' || next == ']' || next == '}') {
         // Process closing bracket
         last_bracet_position = position;

         // unmatched first bracket
         if (opening_brackets_stack.empty())
         {
            // pushing bogus entry with right position
            // to make it non empty
            Bracket bracket(next, position);
            opening_brackets_stack.push(bracket);
            break;
         }

         Bracket bracket = opening_brackets_stack.top();
         // unmatched opening bracket
         if ( !bracket.Matchc(next) )
         {
            // cout << bracket.type << " != "<< next << endl;
            // pushing bogus entry with right position
            Bracket bracket(next, position);
            opening_brackets_stack.push(bracket);
            break;
         }
         opening_brackets_stack.pop();
      }
   }

   // Printing answer, write your code here
   if (opening_brackets_stack.empty())
   {
      cout << "Success" << endl;
   }
   else
   {
      Bracket bracket = opening_brackets_stack.top();
      // If its opening bracket, we deal with it first
      if (bracket.type == '(' ||
            bracket.type == '[' ||
            bracket.type == '{')
      {
         cout << bracket.position + 1 << endl;
      }
      else
      {
         cout << last_bracet_position + 1 << endl;
      }
   }
   return 0;
}
