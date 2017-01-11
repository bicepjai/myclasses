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
#include <queue>

typedef unsigned long long ull;
typedef long long ll;

using namespace std;


// Splay tree implementation

// Vertex of a splay tree
struct Vertex {
   ll key;
   // Sum of all the keys in the subtree - remember to update
   // it after each operation that changes the tree.
   long long sum;
   Vertex* left;
   Vertex* right;
   Vertex* parent;

   Vertex(ll key, long long sum, Vertex* left, Vertex* right, Vertex* parent)
      : key(key), sum(sum), left(left), right(right), parent(parent) {}
};

ll height(Vertex* root)
{
   if (root == NULL) return 0;
   return (max(height(root->left), height(root->right)) + 1);
}
// -------------------------------------------------------------------------------
ll _print_t(Vertex *tree, ll is_left, ll offset, ll depth, char s[20][255])
{
   char b[20];
   ll width = 5;

   if (!tree) return 0;

   sprintf(b, "(%03lld)", tree->key);

   ll left  = _print_t(tree->left,  1, offset,                depth + 1, s);
   ll right = _print_t(tree->right, 0, offset + left + width, depth + 1, s);

#ifdef COMPACT
   for (ll i = 0; i < width; i++)
      s[depth][offset + left + i] = b[i];

   if (depth && is_left) {

      for (ll i = 0; i < width + right; i++)
         s[depth - 1][offset + left + width / 2 + i] = '-';

      s[depth - 1][offset + left + width / 2] = '.';

   } else if (depth && !is_left) {

      for (ll i = 0; i < left + width; i++)
         s[depth - 1][offset - width / 2 + i] = '-';

      s[depth - 1][offset + left + width / 2] = '.';
   }
#else
   for (ll i = 0; i < width; i++)
      s[2 * depth][offset + left + i] = b[i];

   if (depth && is_left) {

      for (ll i = 0; i < width + right; i++)
         s[2 * depth - 1][offset + left + width / 2 + i] = '-';

      s[2 * depth - 1][offset + left + width / 2] = '+';
      s[2 * depth - 1][offset + left + width + right + width / 2] = '+';

   } else if (depth && !is_left) {

      for (ll i = 0; i < left + width; i++)
         s[2 * depth - 1][offset - width / 2 + i] = '-';

      s[2 * depth - 1][offset + left + width / 2] = '+';
      s[2 * depth - 1][offset - width / 2 - 1] = '+';
   }
#endif

   return left + width + right;
}

void print_t(Vertex *tree)
{
   char s[20][255];
   for (ll i = 0; i < 20; i++)
      sprintf(s[i], "%80s", " ");

   _print_t(tree, 0, 0, 0, s);

   for (ll i = 0; i < 2 * height(tree); i++)
      printf("%s\n", s[i]);
}
// -------------------------------------------------------------------------------

void update(Vertex* v) {
   if (v == NULL) return;
   v->sum = v->key + (v->left != NULL ? v->left->sum : 0ll) + (v->right != NULL ? v->right->sum : 0ll);
   if (v->left != NULL) {
      v->left->parent = v;
   }
   if (v->right != NULL) {
      v->right->parent = v;
   }
}

void small_rotation(Vertex* v) {
   Vertex* parent = v->parent;
   if (parent == NULL) {
      return;
   }
   Vertex* grandparent = v->parent->parent;
   if (parent->left == v) {
      Vertex* m = v->right;
      v->right = parent;
      parent->left = m;
   } else {
      Vertex* m = v->left;
      v->left = parent;
      parent->right = m;
   }
   update(parent);
   update(v);
   v->parent = grandparent;
   if (grandparent != NULL) {
      if (grandparent->left == parent) {
         grandparent->left = v;
      } else {
         grandparent->right = v;
      }
   }
}

void big_rotation(Vertex* v) {
   if (v->parent->left == v && v->parent->parent->left == v->parent) {
      // Zig-zig
      small_rotation(v->parent);
      small_rotation(v);
   } else if (v->parent->right == v && v->parent->parent->right == v->parent) {
      // Zig-zig
      small_rotation(v->parent);
      small_rotation(v);
   } else {
      // Zig-zag
      small_rotation(v);
      small_rotation(v);
   }
}

// Makes splay of the given vertex and makes
// it the new root.
void splay(Vertex*& root, Vertex* v) {
   if (v == NULL) return;
   // if(v->parent == NULL) cout << "parent null during splaying" << endl;
   while (v->parent != NULL) {
      if (v->parent->parent == NULL) {
         small_rotation(v);
         break;
      }
      big_rotation(v);
   }
   root = v;
}

// Searches for the given key in the tree with the given root
// and calls splay for the deepest visited node after that.
// If found, returns a pointer to the node with the given key.
// Otherwise, returns a pointer to the node with the smallest
// bigger key (next value in the order).
// If the key is bigger than all keys in the tree,
// returns NULL.
Vertex* find(Vertex*& root, ll key) {
   Vertex* v = root;
   Vertex* last = root;
   Vertex* next = NULL;
   while (v != NULL) {
      if (v->key >= key && (next == NULL || v->key < next->key)) {
         next = v;
      }
      last = v;
      if (v->key == key) {
         break;
      }
      if (v->key < key) {
         v = v->right;
      } else {
         v = v->left;
      }
   }
   // if(last != NULL)
   //    cout << "last= " << last->key << endl;
   splay(root, last);
   // if(next != NULL)
   //    cout << "next= " << next->key << endl;
   return next;
}

void split(Vertex* root, ll key, Vertex*& left, Vertex*& right) {
   right = find(root, key);
   splay(root, right);
   if (right == NULL) {
      left = root;
      return;
   }
   left = right->left;
   right->left = NULL;
   if (left != NULL) {
      left->parent = NULL;
   }
   update(left);
   update(right);
}

Vertex* merge(Vertex* left, Vertex* right) {
   if (left == NULL) return right;
   if (right == NULL) return left;
   Vertex* min_right = right;
   while (min_right->left != NULL) {
      min_right = min_right->left;
   }
   splay(right, min_right);
   right->left = left;
   update(right);
   return right;
}

// Code that uses splay tree to solve the problem

Vertex* root = NULL;

void insert(ll x) {
   Vertex* v = root;
   while (v != NULL) {
      if (v->key == x) {
         // cout << "-- insert didnt go thru" << endl;
         return;
      }
      if (v->key < x) {
         v = v->right;
      } else {
         v = v->left;
      }
   }

   Vertex* left = NULL;
   Vertex* right = NULL;
   Vertex* new_vertex = NULL;
   split(root, x, left, right);
   if (right == NULL || right->key != x) {
      new_vertex = new Vertex(x, x, NULL, NULL, NULL);
   }
   root = merge(merge(left, new_vertex), right);
}

void inorder(Vertex* temp)
{
   if (temp == NULL) return;
   inorder(temp->left);
   cout << temp->key << " ";
   inorder(temp->right);
}

void erase(ll x) {
   // Implement erase yourself
   Vertex* v = root;
   bool found = false;
   while (v != NULL) {
      if (v->key == x) {
         found = true;
         break;
      }
      if (v->key < x) {
         v = v->right;
      } else {
         v = v->left;
      }
   }

   if (found)
   {
      // cout << "erase " << x << " == " << v->key << endl;
      // print_t(root);
      // inorder(root); cout << endl;
      // cout << "---splaying--" << endl;
      splay(root, v);
      // print_t(root);
      // inorder(root); cout << endl;
      // cout << "-------------" << endl;
      Vertex* left = root->left;
      Vertex* right = root->right;
      // cout << "---deleteing--" << root->key << endl;
      if (root != NULL)
         delete(root);
      root = merge(left, right);
      if (root != NULL)
      {
         // cout << " went thru--" << endl;
         root->parent = NULL; // finding this missing link took 3 hours
         // cout << "---aftr merge--" << root->key << endl;
      }
   }
}

bool find(ll x) {
   // Implement find yourself
   Vertex* v = find(root, x);
   if (v == NULL) {
      return false;
   } else {
      return true;
   }
}

long long sum(ll from, ll to) {
   Vertex* left = NULL;
   Vertex* middle = NULL;
   Vertex* right = NULL;

   ll from1 = min(from, to);
   ll to1 = max(from, to);

   split(root, from1, left, middle);
   split(middle, to1 + 1, middle, right);
   long long ans = 0;
   // Complete the implementation of sum
   // cout << "key: " << middle->key << " sum: " << middle->sum << endl;
   if (middle != NULL)
   {
      ans = middle->sum;
   }
      // cout << "++++++ left subtree" << endl;
      // print_t(left);
      // inorder(left); cout << endl;

      // cout << "++++++ middle subtree" << endl;
      // print_t(middle);
      // inorder(middle); cout << endl;

      // cout << "++++++ right subtree" << endl;
      // print_t(right);
      // inorder(right); cout << endl;

      // Vertex* i1 = merge(left, middle);
      // cout << "++++++ after merge subtree" << endl;
      // print_t(i1);
      // inorder(i1); cout << endl;

      // root = merge(i1, right);
   root = merge(merge(left, middle), right);

   return ans;
}

const ll MODULO = 1000000001;

int main() {
   ll n;
   scanf("%lld", &n);
   ll last_sum_result = 0;
   for (ll i = 0; i < n; i++) {
      char buffer[10];
      scanf("%s", buffer);
      char type = buffer[0];
      switch (type) {
      case '+' : {
         ll x;
         scanf("%lld", &x);
         // cout << "-insert------------------------" << (x + last_sum_result) % MODULO << endl;
         insert((x + last_sum_result) % MODULO);
         // print_t(root);
         // inorder(root); cout << endl;
      } break;
      case '-' : {
         ll x;
         scanf("%lld", &x);
         // cout << "-erase-------------------------" << (x + last_sum_result) % MODULO << endl;
         erase((x + last_sum_result) % MODULO);
         // print_t(root);
         // inorder(root); cout << endl;
      } break;
      case '?' : {
         ll x;
         scanf("%lld", &x);
         // cout << "-find--------------------------" << (x + last_sum_result) % MODULO << endl;
         printf(find((x + last_sum_result) % MODULO) ? "Found\n" : "Not found\n");
         // print_t(root);
         // inorder(root); cout << endl;
      } break;
      case 's' : {
         ll l, r;
         scanf("%lld %lld", &l, &r);
         // cout << "-sum--------------------------- " << (l + last_sum_result) % MODULO << " to " << (r + last_sum_result) % MODULO << endl;
         long long res = sum((l + last_sum_result) % MODULO, (r + last_sum_result) % MODULO);
         printf("%lld\n", res);
         last_sum_result = ll(res % MODULO);
         // print_t(root);
         // inorder(root); cout << endl;
      }
      }
   }
   return 0;
}
