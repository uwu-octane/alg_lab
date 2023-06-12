# Modeling of the Degree Constrained Bottleneck Spanning Tree with Mixed Integer Programming.

As we did for [SAT](../../03_card_sat/DBST/) and [CP-SAT](../../02_cpsat/DBST), we again model the *Degree Constrained Bottleneck Spanning Tree* as an example.
However, we extend the problem as follows:
Among all spanning trees with minimal bottleneck, return the one with minimal weight (sum of weights of used edges).

You can find the code again attached.

## Approach for the objective function

Despite the support of objective functions in Mixed Integer Programming, we cannot model the lexicographic objective directly.
We now have (at least) two options:
1. Use the minimum weight as objective and use a binary search as with SAT to find the minimum bottleneck.
2. Use a first Mixed Integer Program to find the minimum bottleneck, and then a separate one to find the minimum weight spanning tree in the restricted graph.

We are going with the second approach, because based on my experience, I expect it to be much faster.

## Variables and Constraints

For every undirected edge, $\{u,v\}\in E$ we introduce a boolean variable $x_{u,v} \in \mathbb{B}$ that is $1$ if we use the edge, and $0$ otherwise.

The degree constraint of a maximal degree of $d$ can be expressed for every vertex $v\in V$ by
$$\forall v\in V: \quad \sum\limits_{e \in \delta(\{v\})}x_e \leq d$$

Here, $\delta(S)$ defines for a set of vertices $S\subset V$ the edges with one end in $S$ and one end in $V\setminus S$, thus, the edges leaving $S$.

Next let us enforce that every vertex has at least one neighbor (assuming that $|V|\geq 2$)
$$\sum\limits_{e \in \delta(\{v\})}x_e \geq 1$$


As we want a tree, we additionally state
$$\sum\limits_{e \in E}x_e = n-1$$

The last, and most complicated constraint, is again enforcing the connectivity.
This can be done by the following set of constraints.
$$\forall S\subsetneq V, S\not=\emptyset: \quad \sum\limits_{e \in \delta(S)} x_e \geq 1$$

As these are exponentially many, we add them via lazy constraints.
For this, we need to write a function that checks a solution if any of these constraints is violated.
We can do this efficiently by just looking at the connected components in the provided solution and add the constraint for every component (if there are more than one).
Note that while the set of constraints is exponential, we can derive the missing constraints in linear time (worst case, we have to do this exponentially often, but this rarely happens).

## Finding the minimum bottleneck

For finding the minimum bottleneck, we introduce an additional variable $\ell \in \mathbb{R}^+_0$, that represent the length of the longest edge.
The objective function can be expressed easily as

$$\min \ell$$

To prohibit all edges larger than $\ell$, we add for every edge the constraint
$$\forall e\in E: \ell \leq c_e \cdot x_e$$
where $c_e$ represents the length of the edge $e$.

## Finding the minimum weight spanning tree

After we have determined $\ell$, we look for the spanning tree with the lowest weight on the edges that have at most the length $\ell$.
We can do so with nearly the same model, just delete $\ell$ and all $x_e$ with $c_e > \ell$.
Let $E'$ represent the remaining edges.
As objective function, we can use
$$\min \sum_{e\ in E'} c_e \cdot x_e$$
which is simply the sum of the weight of the used edges.

