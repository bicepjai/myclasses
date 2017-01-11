import copy
import numpy as np
from collections import Counter, defaultdict
from itertools import combinations
import operator

# DO NOT MODIFY THIS FUNCTION
def convert_tree_as_set_to_adjacencies(tree):
    """
    This snippet of code converts between two representations we use for
    edges (namely, with Chow-Liu it suffices to just store edges as a set of
    pairs (i, j) with i < j), whereas when we deal with learning tree
    parameters and code Sum-Product it will be convenient to have an
    "adjacency list" representation, where we can query and find out the list
    of neighbors for any node. We store this "adjacency list" as a Python
    dictionary.

    Input
    -----
    - tree: a Python set of edges (where (i, j) being in the set means that we
        don't have to have (j, i) also stored in this set)

    Output
    ------
    - edges: a Python dictionary where `edges[i]` gives you a list of neighbors
        of node `i`
    """
    edges = {}
    for i, j in tree:
        if i not in edges:
            edges[i] = [j]
        else:
            edges[i].append(j)
        if j not in edges:
            edges[j] = [i]
        else:
            edges[j].append(i)
    return edges


# DO NOT MODIFY THIS CLASS
class UnionFind():
    def __init__(self, nodes):
        """
        Union-Find data structure initialization sets each node to be its own
        parent (so that each node is in its own set/connected component), and
        to also have rank 0.

        Input
        -----
        - nodes: list of nodes
        """
        self.parents = {}
        self.ranks = {}

        for node in nodes:
            self.parents[node] = node
            self.ranks[node] = 0

    def find(self, node):
        """
        Finds which set/connected component that a node belongs to by returning
        the root node within that set.

        Technical remark: The code here implements path compression.

        Input
        -----
        - node: the node that we want to figure out which set/connected
            component it belongs to

        Output
        ------
        the root node for the set/connected component that `node` is in
        """
        if self.parents[node] != node:
            # path compression
            self.parents[node] = self.find(self.parents[node])
        return self.parents[node]

    def union(self, node1, node2):
        """
        Merges the connected components of two nodes.

        Inputs
        ------
        - node1: first node
        - node2: second node
        """
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:  # only merge if the connected components differ
            if self.ranks[root1] > self.ranks[root2]:
                self.parents[root2] = root1
            else:
                self.parents[root1] = root2
                if self.ranks[root1] == self.ranks[root2]:
                    self.ranks[root2] += 1


def compute_empirical_distribution(values):
    """
    Given a sequence of values, compute the empirical distribution.

    Input
    -----
    - values: list (or 1D NumPy array or some other iterable) of values

    Output
    ------
    - distribution: a Python dictionary representing the empirical distribution
    """
    distribution = {}

    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #

    n = len(values)
    x_counter = Counter(values)
    for x in x_counter.keys():
        x_counter[x] = x_counter[x] / n
    distribution = x_counter # {k:x_counter[k] for k in x_counter.keys()}

    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------

    return distribution


def compute_empirical_mutual_info_nats(var1_values, var2_values):
    """
    Compute the empirical mutual information for two random variables given a
    pair of observed sequences of those two random variables.

    Inputs
    ------
    - var1_values: observed sequence of values for the first random variable
    - var2_values: observed sequence of values for the second random variable
        where it is assumed that the i-th entries of `var1_values` and
        `var2_values` co-occur

    Output
    ------
    The empirical mutual information *in nats* (not bits)
    """

    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #

    empirical_mutual_info_nats = 0.0
    emp_dist_var1 = compute_empirical_distribution(var1_values)
    emp_dist_var2 = compute_empirical_distribution(var2_values)

    joint_values = [(x,y) for x,y in zip(var1_values,var2_values)]
    emp_joint_dist_ordered = compute_empirical_distribution(joint_values)
        
    for joint_var in emp_joint_dist_ordered.keys():
        (var1,var2) = joint_var
        empirical_mutual_info_nats -= emp_joint_dist_ordered[joint_var] * np.log(emp_dist_var1[var1] * emp_dist_var2[var2])
        empirical_mutual_info_nats += emp_joint_dist_ordered[joint_var] * np.log(emp_joint_dist_ordered[joint_var])
        
    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------

    return empirical_mutual_info_nats


def chow_liu(observations):
    """
    Run the Chow-Liu algorithm.

    Input
    -----
    - observations: a 2D NumPy array where the i-th row corresponds to the
        i-th training data point

        *IMPORTANT*: it is assumed that the nodes in the graphical model are
        numbered 0, 1, ..., up to the number of variables minus 1, where the
        number of variables in the graph is determined from `observations` by
        looking at `observations.shape[1]`

    Output
    ------
    - best_tree: a Python set consisting of edges that are in a Chow-Liu tree
        (note that if edge (i, j) is in this set, then edge (j, i) should not
        be in the set; also, for grading purposes, please present the edges
        so that for an edge (i, j) in this set, i < j
    """
    best_tree = set()  # we will add in edges to this set
    num_obs, num_vars = observations.shape    
    
    # findind the tree from the nodes of the graph
    union_find = UnionFind(range(num_vars))

    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #
    
    edges = [edge for edge in combinations(range(num_vars),2)]
    edge_nats = {}
    for edge in edges:
        var1 = observations[:, edge[0]]
        var2 = observations[:, edge[1]]
        edge_nats[edge] = compute_empirical_mutual_info_nats(var1, var2)
    
    sorted_edges = sorted(edge_nats.items(), key=operator.itemgetter(1), reverse=True)
    
    best_tree_edges = 0
    for (edge,nats) in sorted_edges:
        start_node = edge[0]
        end_node = edge[1]
        if(union_find.find(start_node) != union_find.find(end_node)):
            best_tree.add(edge)
            best_tree_edges += 1
            union_find.union(start_node,end_node)
            
        if(best_tree_edges == num_vars):
            break

    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------

    return best_tree


def compute_empirical_conditional_distribution(var1_values, var2_values):
    """
    Given two sequences of values (corresponding to samples from two
    random variables), compute the empirical conditional distribution of
    the first variable conditioned on the second variable.

    Inputs
    ------
    - var1_values: list (or 1D NumPy array or some other iterable) of values
        sampled from, say, $X_1$
    - var2_values: list (or 1D NumPy array or some other iterable) of values
        sampled from, say, $X_2$, where it is assumed that the i-th entries of
        `var1_values` and `var2_values` co-occur
    Output
    ------
    - conditional_distributions: a dictionary consisting of dictionaries;
        `conditional_distributions[x_2]` should be the dictionary that
        represents the conditional distribution $X_1$ given $X_2 = x_2$
    """
    conditional_distributions = {x2: {} for x2 in set(var2_values)}

    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #

    xs = set(var1_values).union(set(var2_values))
    
    joint_values = [(x,y) for x,y in zip(var1_values,var2_values)]
    emp_joint_dist_ordered = compute_empirical_distribution(joint_values)
    
    
    for x2 in xs: # conditioning on rv1
        dist = {}
        norm_sum = 0
        for x1 in xs:
            dist[x1] = emp_joint_dist_ordered[(x1,x2)]
            norm_sum += dist[x1]
        normalised_dist = {k: dist[k]/norm_sum for k in dist.keys() }
        conditional_distributions[x2] = normalised_dist
        
    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------

    return conditional_distributions


def learn_tree_parameters(observations, tree, root_node=0):
    """
    Learn a collection of node and edge potentials from observations that
    corresponds to a maximum likelihood estimate.

    Please use the approach presented in the course video/notes. Remember that
    the only node potential that isn't all 1's is the one corresponding to the
    root node chosen, and the edge potentials are set to be empirical
    conditional probability distributions.

    Inputs
    ------
    - observations: a 2D NumPy array where the i-th row corresponds to the
        i-th training data point

        *IMPORTANT*: it is assumed that the nodes in the graphical model are
        numbered 0, 1, ..., up to the number of variables minus 1, where the
        number of variables in the graph is determined from `observations` by
        looking at `observations.shape[1]`
    - tree: a set consisting of which edges are present (if (i, j) is in the
        set, then you don't have to also include (j, i)); note that the
        nodes must be as stated above
    - root_node: an integer specifying which node to treat as the root node

    Outputs
    -------
    - node_potentials: Python dictionary where `node_potentials[i]` is
        another Python dictionary representing the node potential table for
        node `i`; this means that `node_potentials[i][x_i]` should give the
        potential value for what, in the course notes, we call $\phi_i(x_i)$
    - edge_potentials: Python dictionary where `edge_potentials[(i, j)]` is
        a dictionaries-within-a-dictionary representation for a 2D potential
        table so that `edge_potentials[(i, j)][x_i][x_j]` corresponds to
        what, in the course notes, we call $\psi_{i,j}(x_i, x_j)$

        *IMPORTANT*: For the purposes of this project, please be sure to
        specify both `edge_potentials[(i, j)]` *and* `edge_potentials[(j, i)]`,
        where `edge_potentials[(i, j)][x_i][x_j]` should equal
        `edge_potentials[(j, i)][x_j][x_i]` -- we have provided a helper
        function `transpose_2d_table` below that, given edge potentials
        computed in one "direction" (i, j), computes the edge potential
        for the "other direction" (j, i)
    """
    nodes = set(range(observations.shape[1]))
    edges = convert_tree_as_set_to_adjacencies(tree)
    node_potentials = {}
    edge_potentials = {}

    def transpose_2d_table(dicts_within_dict_table):
        """
        Given a dictionaries-within-dictionary representation of a 2D table
        `dicts_within_dict_table`, computes a new 2D table that's also a
        dictionaries-within-dictionary representation that is the transpose of
        the original 2D table, so that:

            transposed_table[x1][x2] = dicts_within_dict_table[x2][x1]

        Input
        -----
        - dicts_within_dict_table: as described above

        Output
        ------
        - transposed_table: as described above
        """
        transposed_table = {}
        for x2 in dicts_within_dict_table:
            for x1 in dicts_within_dict_table[x2]:
                if x1 not in transposed_table:
                    transposed_table[x1] = \
                        {x2: dicts_within_dict_table[x2][x1]}
                else:
                    transposed_table[x1][x2] = \
                        dicts_within_dict_table[x2][x1]
        return transposed_table

    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #
    
    # node_potentials
    unique_rvs = np.unique(observations)
    all_1s_dict = {k:1 for k in unique_rvs}
    for node in nodes:
        node_potentials[node] = all_1s_dict

    # setting root_node node potential
    node_potentials[root_node] = \
        compute_empirical_distribution(observations[:, root_node])
     
    # calculating edge_potentials travering the tree BFS
    fringe = [root_node]  # this is a list of nodes queued up to be visited next
    visited = {node: False for node in nodes}  # track which nodes are visited
    while len(fringe) > 0:
        node = fringe.pop(0)  # removes the 0th element of `fringe` and returns it
        visited[node] = True  # mark `node` as visited
        for neighbor in edges[node]:
            if not visited[neighbor]:
                # do some processing that involves the edge `(neighbor, node)` here
                
                node_var = observations[:, node]
                neighbor_var = observations[:, neighbor]
                # P table neighbor_var | node_var
                edge_potential = compute_empirical_conditional_distribution(neighbor_var, node_var)
                # we are traversing from node to neighbour
                edge_potentials[(node,neighbor)] = edge_potential
                edge_potentials[(neighbor,node)] = transpose_2d_table(edge_potential)
                    
                    
                # finally after you do your processing, add `neighbor` to `fringe`
                fringe.append(neighbor)
        
    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------
    return node_potentials, edge_potentials


def sum_product(nodes, edges, node_potentials, edge_potentials):
    """
    Run the Sum-Product algorithm.

    Inputs
    ------
    - nodes: Python set that consists of the nodes
    - edges: Python dictionary where `edges[i]` is a list saying which nodes
        are neighbors of node `i`
    - node_potentials: Python dictionary where `node_potentials[i]` is
        another Python dictionary representing the node potential table for
        node `i`; this means that `node_potentials[i][x_i]` should give the
        potential value for what, in the course notes, we call $\phi_i(x_i)$

        *IMPORTANT*: For the purposes of this project, the alphabets of each
        random variable should be inferred from the node potentials, so each
        node potential's dictionary's keys should tell you what the alphabet is
        (or at least the subset of the alphabet for which the probability is
        nonzero); this means that you should not use collections.defaultdict
        to produce, for instance, a dictionary with no keys that outputs 1 for
        everything here since we cannot read off what the alphabet is for the
        random variable
    - edge_potentials: Python dictionary where `edge_potentials[(i, j)]` is
        a dictionaries-within-a-dictionary representation for a 2D potential
        table so that `edge_potentials[(i, j)][x_i][x_j]` corresponds to
        what, in the course notes, we call $\psi_{i,j}(x_i, x_j)$

        *IMPORTANT*: For the purposes of this project, please be sure to
        specify both `edge_potentials[(i, j)]` *and* `edge_potentials[(j, i)]`,
        where `edge_potentials[(i, j)][x_i][x_j]` should equal
        `edge_potentials[(j, i)][x_j][x_i]`

    Output
    ------
    - marginals: Python dictionary where `marginals[i]` gives the marginal
        distribution for node `i` represented as a dictionary; you do *not*
        need to store entries that are 0
    """
    marginals = {}
    messages = {}

    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #
#    print("----------sum product--------------")
#    print("->nodes",nodes)
#    print("->edges",edges)
#    print("->node_potentials",node_potentials)
#    print("->edge_potentials",edge_potentials)

    # root_node can be anything
    root_node = list(nodes)[0]
    xlists = [node_potentials[node].keys() for node in node_potentials]
    Xs = list(set([item for sublist in xlists for item in sublist]))
#    print("->Xs",Xs)

    # computer paths DFS ============================================
    
    leaf_nodes = set([node for node in edges if len(edges[node]) == 1])
   
    visited, stack = set(), [root_node]
    parentMap = {}
    
    while stack:
      node = stack.pop()
      for neighbor in edges[node]:
        if neighbor not in visited:
          visited.add(neighbor)
          stack.append(neighbor)
          parentMap[neighbor] = node
    
    backward_paths = []
    for leaf in leaf_nodes:
      node = leaf
      path = []
      while node != root_node:
        path += [node]
        node = parentMap[node]
      path += [root_node]
      
      backward_paths.append(path)
     
    forward_paths = [path[::-1] for path in backward_paths]

    # print(backward_paths)
    # print(forward_paths)

    v_dot_v = lambda v1, v2, abc: {x: v1.get(x, 0) * v2.get(x, 0) for x in abc 
                            if v1.get(x, None) and v2.get(x, None)}

    vXa = lambda v, a, abc: {x: sum(v.get(y,0) * a.get(y,{}).get(x,0)  for y in abc)
                          for x in abc if sum(v.get(y,0) and a.get(y,{}).get(x,0) for y in abc)}
    normalize = lambda d: {x:d[x]/sum(list(d.values())) for x in d}
                           
    # Compute the backward messages leaves to root ===================================
#    print("backward pass  -------")
    calculated_messages = {node:[] for node in nodes}
    for path in backward_paths:
#        print("---- path",path)
        prev_msg = { x:1 for x in Xs }
        prev_node = path.pop(0)
        for next_node in path:
            edge = (prev_node, next_node)
            phi = node_potentials[prev_node]
            psi = edge_potentials[edge]

            # process the edge
#            print("-- edge",edge,"prev_msg",prev_msg)
            if edge not in messages:
                prev_msg_phi = v_dot_v(prev_msg,phi,Xs)
                messages[edge] = vXa(prev_msg_phi,psi,Xs)
                # marker to use if calculated messages for edges encountered
                calculated_messages[next_node] += [edge]
            else: # if edge already present
                # if message already exist we gather all the 
                # incoming edges and calculate the messages
#                print(edge," incoming-edges",calculated_messages[prev_node])
                msg_updates = { x:1 for x in Xs }
                for prev_edge in calculated_messages[prev_node]:
                    msg_updates = v_dot_v(msg_updates,messages[prev_edge],Xs)

                prev_msg_phi = v_dot_v(msg_updates,phi,Xs)
                messages[edge] = vXa(prev_msg_phi,psi,Xs)
                 
            prev_msg = messages[edge]
            
            prev_node = next_node

#    print("->backward messages")
#    for edge in messages:
#        print(edge,"->",messages[edge])
        
    # Compute the forward messages root to leaves DFS ===================================
#    print("forward pass --------")
    for path in forward_paths:
#        print("---- path",path)
        prev_node = path.pop(0)
        for next_node in path:
            edge = (prev_node, next_node)
            
            # taking all incoming edges into account while moving forward
            # for calculating the prev_msg for current node
            incoming_edges = list(set(edges[prev_node])-set([next_node]))
            
#            print("---- edge",edge,"incoming_edges",incoming_edges)
            prev_msg = { x:1 for x in Xs }
            for in_edge in incoming_edges:
#                print("--",(in_edge,prev_node))
                prev_msg = v_dot_v(prev_msg,messages[(in_edge,prev_node)],Xs)
                
            phi = node_potentials[prev_node]
            psi = edge_potentials[edge]

            # process the edge, if it already exist we dont care
#            print("prev_msg",prev_msg)
            if edge not in messages:
                prev_msg_phi = v_dot_v(prev_msg,phi,Xs)
                messages[edge] = vXa(prev_msg_phi,psi,Xs)

                 
            prev_msg = messages[edge]
            
            prev_node = next_node
    
#    print("->forward messages")
#    for edge in messages:
#        print(edge,"->",messages[edge])
    
    # Compute the marginals ===================================
    
    for node in nodes:
        incoming_edges = list(set(edges[node]))
        marginal = node_potentials[node] # phi
        for in_edge in incoming_edges:
            marginal = v_dot_v(marginal,messages[(in_edge,node)],Xs)
        
        marginals[node] = normalize(marginal)

#    print("------------------------")

    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------

    return marginals

def test_sum_product_proj():

    nodes = {1, 2, 3, 4, 5}
    edges = {1: [2, 3], 2: [1, 4, 5], 3: [1], 4: [2], 5: [2]}
    node_potentials = { 1: {'green': 0.9, 'blue': 0.3}, 
                        2: {'green': 0.2, 'blue': 0.1}, 
                        3: {'green': 0.6, 'blue': 0.4}, 
                        4: {'green': 0.5, 'blue': 0.1}, 
                        5: {'green': 0.3, 'blue': 0.5}}
    edge_potentials = {(1, 2): {'green': {'green': 0.1, 'blue': 1}, 'blue': {'green': 1, 'blue': 0.1}}, 
                       (1, 3): {'green': {'green': 0, 'blue': 10}, 'blue': {'green': 10, 'blue': 0}}, 
                       (4, 2): {'green': {'green': 0.1, 'blue': 1}, 'blue': {'green': 1, 'blue': 0.1}}, 
                       (2, 5): {'green': {'green': 1, 'blue': 3}, 'blue': {'green': 3, 'blue': 1}}, 
                       (3, 1): {'green': {'green': 0, 'blue': 10}, 'blue': {'green': 10, 'blue': 0}}, 
                       (5, 2): {'green': {'green': 1, 'blue': 3}, 'blue': {'green': 3, 'blue': 1}},
                       (2, 4): {'green': {'green': 0.1, 'blue': 1}, 'blue': {'green': 1, 'blue': 0.1}}, 
                       (2, 1): {'green': {'green': 0.1, 'blue': 1}, 'blue': {'green': 1, 'blue': 0.1}}}
    marginals = sum_product(nodes, edges, node_potentials, edge_potentials)
    print('Your output:', marginals)
    
def test_sum_product1():
    """
    Below is the example from
    "Exercise: The Sum-Product Algorithm - A Numerical Calculation"
    where we have conditioned on $X_1 = 0$ (conditioning can be done by setting
    the node potential to be all 0's except for at the observed value -- see
    below in the code for how this is done with `node_potentials[1]`)
    """
    nodes = {1, 2, 3}
    edges = {1: [2], 2: [1, 3], 3: [2]}
    print("test_sum_product1")

    node_potentials = {1: {0: 1, 1: 0}, 2: {0: 1, 1: 1}, 3: {0: 1, 1: 1}}
    edge_potentials = {(1, 2): {0: {0: 5, 1: 1}, 1: {0: 1, 1: 5}},
                       (2, 1): {0: {0: 5, 1: 1}, 1: {0: 1, 1: 5}},
                       (2, 3): {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}},
                       (3, 2): {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}}}

    marginals = sum_product(nodes, edges, node_potentials, edge_potentials)
    print('Your output:', marginals)
    print('Expected output:',
          {1: {0: 1.0},
           2: {0: 0.8333333333333334, 1: 0.16666666666666666},
           3: {0: 0.16666666666666666, 1: 0.8333333333333334}})

    node_potentials = {1: {0: 1, 1: 1}, 2: {0: 1, 1: 1}, 3: {0: 1, 1: 1}}
    print(compute_marginals_given_observations(nodes, edges,
                                               node_potentials,
                                               edge_potentials,
                                               observations={1: 0}))


def test_sum_product2():
    """
    Below is the example from
    "Homework Problem: Blue Green Tree" and
    "Homework Problem: Blue Green Tree, Continued"
    """
    nodes = {1, 2, 3, 4, 5}
    edges = {1: [2, 3], 2: [1, 4, 5], 3: [1], 4: [2], 5: [2]}
    print("test_sum_product2")

    node_potentials = {1: {'blue': 0.5, 'green': 0.5},
                       2: {'blue': 0.5, 'green': 0.5},
                       3: {'blue': 0.6, 'green': 0.4},
                       4: {'blue': 0.8, 'green': 0.2},
                       5: {'blue': 0.8, 'green': 0.2}}
    edge_potentials = {(1, 2): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (2, 1): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (1, 3): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (3, 1): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (2, 4): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (4, 2): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (2, 5): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}},
                       (5, 2): {'blue': {'blue': 0, 'green': 1},
                                'green': {'blue': 1, 'green': 0}}}
    marginals = sum_product(nodes, edges, node_potentials, edge_potentials)
    print('Your output:', marginals)
    print('Expected output:',
          {1: {'blue': 0.9142857142857144, 'green': 0.08571428571428572},
           2: {'blue': 0.08571428571428569, 'green': 0.9142857142857143},
           3: {'blue': 0.08571428571428572, 'green': 0.9142857142857144},
           4: {'blue': 0.9142857142857143, 'green': 0.0857142857142857},
           5: {'blue': 0.9142857142857143, 'green': 0.0857142857142857}})


def compute_marginals_given_observations(nodes, edges, node_potentials,
                                         edge_potentials, observations):
    """
    For a given choice of nodes, edges, node potentials, and edge potentials,
    and also observed values for specific nodes, we can compute marginals
    given the observations. This can actually be done by just modifying the
    node potentials and then calling the Sum-Product algorithm.

    Inputs
    ------
    - nodes, edges, node_potentials, edge_potentials: see documentation for
        sum_product()
    - observations: a dictionary where each key is a node and the value for
        the key is what the observed value for that node is (for example,
        `{1: 0}` means that node 1 was observed to have value 0)

    Output
    ------
    marginals, given the observations (see documentation for the output of
    sum_product())
    """
    new_node_potentials = {}
    
    # -------------------------------------------------------------------------
    # YOUR CODE HERE
    #
    
    xlists = [node_potentials[node].keys() for node in node_potentials]
    Xs = list(set([item for sublist in xlists for item in sublist]))
    zero_node_potentials = {x:0 for x in Xs}

    new_node_potentials = copy.copy(node_potentials)
    for node in new_node_potentials:
        if node in observations:
            new_node_potentials[node] = copy.copy(zero_node_potentials)
            new_node_potentials[node][observations[node]] = 1.0
        
    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------

    return sum_product(nodes,
                       edges,
                       new_node_potentials,
                       edge_potentials)


def main():
    # get coconut oil data
    observations = []
    with open('coconut.csv', 'r') as f:
        for line in f.readlines():
            pieces = line.split(',')
            if len(pieces) == 5:
                observations.append([int(pieces[1]),
                                     int(pieces[2]),
                                     int(pieces[3]),
                                     int(pieces[4])])
    observations = np.array(observations)

    best_tree = chow_liu(observations)
    print(best_tree)

    node_potentials, edge_potentials = learn_tree_parameters(observations,
                                                             best_tree)
    print(node_potentials)
    print(edge_potentials)

    marginals = compute_marginals_given_observations(
        {0, 1, 2, 3},
        convert_tree_as_set_to_adjacencies(best_tree),
        node_potentials,
        edge_potentials,
        observations={1: +1, 2: +1})
    print(marginals)
    print()

    print('[Sum-Product tests based on earlier course material]')
    test_sum_product1()
    test_sum_product2()
#    test_sum_product_proj()


if __name__ == '__main__':
    main()
