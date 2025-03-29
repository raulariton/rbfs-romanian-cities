# Recursive best-first search visualization

This Python program aims to provide a solution to the Romanian cities problem proposed in 
[[S. Russell and P. Norvig, Artificial intelligence: A Modern Approach](https://books.google.ro/books?id=XS9CjwEACAAJ&dq=Russel+Norvig&hl=en&newbks=1&newbks_redir=0&sa=X&ved=2ahUKEwiC_rjC562MAxW9AxAIHVvXDMQQ6AF6BAgFEAM)]
(_Chapter II: Problem Solving_) using the recursive best-first search (RBFS) algorithm. 

The program, however, can also be used to visualize the RBFS algorithm on any graph pathfinding problem. 
  See [Using your own graphs and problems](#using-your-own-graphs-and-problems) for details.

## The Romanian cities problem

The problem consists of finding the optimal path from *Arad* to *Bucharest* by using a searching algorithm on a graph containing various Romanian cities.

### Solution with RBFS

[//]: # (Add friendly explanation of the algorithm)

The RBFS algorithm is a recursive version of the best-first search algorithm. It is used to find the 
optimal path in a graph by exploring the nodes in a best-first order. To view the implementation of the 
algorithm, see [`recursive_best_first_search.py`](src/algorithms/recursive_best_first_search.py).

#### Maximum nodes in memory limitation

Since the RBFS algorithm expands nodes recursively, it keeps a lot of nodes in memory.
As an attempt to improve performance, the program limits the number of nodes in memory. When the limit is 
reached, the algorithm _**prunes**_ the least promising node from memory. This node is the node with the 
highest $f$-value.

## Usage

[//]: # (Explanation of how to run the program, and a short explanation of the code in main.py)

## Using your own graphs and problems
