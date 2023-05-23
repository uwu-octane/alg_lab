# Solving the Degree-Constrained Bottleneck Spanning Tree Problem with a (cardinality) SAT solver

## Problem Definition

In the NP-hard *Degree-Constrained Bottleneck Spanning Tree (DBST)*,
we are given a complete graph $G=(V,E)$ with distance/weight function $dist: E \rightarrow \mathbb{N}^+_0$.
The set $V$ can be a set of point on the plane, and $dist(v,w)$ the euclidean distance between $v\in V$ and $w\in V$.
Additionally, we have a degree constraint $d\geq 2$.
The objective is to find a tree $T$ in $G$ in which no vertex has a degree greater the degree constraint, i.e., $\forall v\in V: deg_T(v)\leq d$, and the weight of the longest edge is minimized.

## Modelling the DBST

How can we optimize the DBST with only a SAT-solver?
There are multiple challenges, we are going to address one after the other.

### Optimization vs. Decision Problem

While the DBST is an optimization problem, SAT is a pure decision problem.
A SAT-solver does not find the optimal solution but just returns any feasible assignment.
To still obtain an optimal solution with a SAT-solver (instead of just any feasible), we use it repeatedly instead of just once.
We transform the optimization problem into its corresponding decision problem.
Instead of asking the SAT-solver *"What is the spanning tree with maximum degree $d$ and shortest possible longest edge?"*,
we ask it (Q) *"Is there a spanning tree with maximum degree $d$, whose longest edge has a weight of at most $b$?"*.

A very useful observation is that the objective value (bottleneck) always equals the weight of a single edge, thus,
there are only $\mathcal{O}(n^2)$ different values to check.
Instead of randomly checking all, we first sort all these values and put them into a list on which we could apply a binary search.
This allows us to find the optimal solution by asking (i.e., running the SAT-solver) $\mathcal{O}(\log n)$ times the question (Q).


###  Selection of variables

We want a tree on a given set of vertices $V$.
Thus, we are looking for a subset of edges.
The set of all edges is given by $E  = \{vw \mid v,w \in V\}$.
Given a bound $b$ for question (Q) on the weight of the longest edge, only edges of $E(b) = \{vw \mid v,w \in V, d(v,w) \leq b\}$ are feasible.
To answer our question (Q) for specific $b$, we are looking for any subset $E'\subseteq E(b)$ that contains a tree with a maximum degree of at most $d$ that spans $V$.
Such a subset can be encoded by introducing a boolean variable for every $e\in E(b)$ that is $\texttt{true}$ if and only if $e$ is in $E'$.

If we are able to express, via clauses and cardinality constraints, that $E'$

1. has at most degree $b$, and
2. is a spanning tree on $V$

we can answer our question (Q) with a SAT-solver (and solve the optimization problem by repeated applications of it).

###  Degree constraint

The degree constraint is the easiest to enforce, so we take care of that one first.
For a vertex $v\in V$, let $\delta_b(v) = \{vw \mid w \in V, vw\in E(b)\}$ be the edges in $E(b)$ that are incident to $v$.
We have to express that at most $b$ of them are allowed to be used.
Using a cardinality constraint, this is straight-forward:

```math
\sum\limits_{e \in \delta_b(v)} x_e \leq d.
```

### Spanning tree

Finally,  we  have to enforce that the graph induced by $E'$ is a spanning tree on $V$.
Thus, we want to ensure that the graph is connected and free of cycles.

A fundamental observation is that every tree on $n$ vertices has exactly $n-1$ edges.
Thus, we can define the cardinality constraint
```math
\sum\limits_{e \in E(b)} x_e \leq n-1\text{ and } \sum\limits_{e \in E(b)}\bar{x}_e \leq |E(b)| - n + 1
```
to deal with that.

Additionally, it is well known that a graph with $n$ vertices and $n-1$ edges is free of cycles if and only if it is connected.
Instead of prohibiting cycles we can alternatively enforce the graph to be connected.
In general, there are multiple options to model connectivity.

The simplest method, we are going to use in this example, is as follows.
For every real and non-empty subset $S \subsetneq V$ of vertices, we introduce a clause that enforces to have at least on edge connecting $S$ with $V\setminus S$.
```math
 \forall \emptyset \subsetneq S \subsetneq V: \bigvee\limits_{v \in S, w \notin S} x_{vw}.
```

Unfortunately, there are exponentially many such subsets $S$ and it is no option to just add all of them directly to the SAT-formula.
However, only a small amount of these subsets will  actually be relevant and we can instead do  the following:
Start without these constraints and look onto the assignment returned by the SAT-solver.
If it is connected, we are fine.
If it is not connected, we can easily add the clause for any connected component $S \in \{V_1,\ldots,V_k\}$ in the solution and run the SAT-solver again.
We can repeat this until the returned solution is connected or the SAT-solver tells us that the formula has become infeasible.
This may sound inefficient but many SAT-solvers allow incremental formula building and will save the insights the gained on the previous formula.
No assignment that has already been discarded by the previous runs can become feasible ever again, making solving the slightly refined formula (often) very fast to solve.
