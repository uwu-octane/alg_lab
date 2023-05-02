# Solving the Degree Constrained Bottleneck Spanning Tree Problem with CP-SAT

## Problem Definition

## Selection of Variables for the Model

The most trivial variable selection would be to choose a boolean variable for every edge, that represents if the edge is in the solution.
Unfortunately, with this representation it is difficult to efficiently contrain the edge set to be a tree.
Instead we will work on an [arborescence](https://en.wikipedia.org/wiki/Arborescence_(graph_theory)) (instead of an undirected tree) and keep track of how deep a vertex is in this arborescence.
You will often need to create auxiliary variables or constructs that allow you to enforce your constraints more efficiently.
After some time, you acquire a set of such techniques that allow you to model nearly anything without much thinking.
In the beginning, a lot may seem unelegant or random.

* Arc variables $x_{vw}\in \{0,1\}$ and $x_{wv}\in \{0,1\}$ for every edge $\{v, w\} \in E$ that represent with $x_{vw}=1$ if the arc is used for the arborescence.
    * An edge $\{v,w\}$ will be in the solution if either $x_{vw}=1$ or $x_{wv}=1$.
* Bottleneck variable $y\in \{0,1,\ldots,\max_{\{v,w\}in E}(d(v,w))\}$ that represent the weight of the most expensive used edge/arc.
* Depth variables $d_v \in \{0, 1, \ldots, |V|-1\}$ for every vertex $v\in V$ representing how deep the vertex is in the arborescence.

## Objective Function

The objective function is in this case trivial as we created the auxiliary variable $y$.
As long as we ensure that $y$ actually gets assigned the value of the most expensive selected edge, we just have to specify
$$\min y$
to obtain the feasible solution with the smallest possible $y$-value.

## Constraints

We have specified what a solution looks like and how to measure its quality.
Next, we have to make sure it actually obeys the rules as otherwise we just get the trivial zero solution that is of perfect zero-weight, but unfortunately not a feasible solution.

Let us start with some simple constraints that don't need much explanation:

* Only one direction of an edge can be chosen: $\forall \{v,w\}\in E: x_{vw}+x_{wv}\leq 1$
* We need to select $|V|-1$ edges for a tree: $\sum_{\{v,w\}\in E}x_{vw}+x_{wv} = |V|-1$
* 

### y-Variable represents most expensive selected edge.

An edge $\{v,w\}$ is selected if $x_{vw}=1$ or $x_{wv}=1$.
Thus, if $x_{vw}=1$, $y\geq d(v,w)$.
$$y \geq d(v,w) \quad \text{if }x_{vw}=1 \quad \forall vw \text{ with } \{v, w\}\in E$$
The objective will make sure that it is not larger than necessary, setting it equal to the most expensive selected edge.


### Tree constraint

A tree needs to have $|V|-1$ edges, so we enforce
$$ \sum_{\{v, w\}\in E} x_{vw}+x_{wv} = |V|-1$$

To make sure it does not have cycles, 

### Degree constraint


