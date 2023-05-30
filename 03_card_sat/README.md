# Sheet  03: (Cardinality) SAT

Constraint Programming allows us to declaratively describe our problem and let the computer handle it.
This time, we will do all the encoding and optimizing ourselves, and only use a simple [SAT-solver](https://en.wikipedia.org/wiki/SAT_solver).
You probably already know the [Cook-Levin Theorem](https://en.wikipedia.org/wiki/Cook%E2%80%93Levin_theorem) from Theoretical Computer Science that allows to encode any problem in NP as a SAT-formula, and consequently solve it with a SAT-solver.
SAT-solvers have become very powerful in the recent years and can often solve formulas with thousand or even millions of variables and clauses in reasonable time.
Of course, the encoding of Cook-Levin is too generic and inefficient, even for powerful modern SAT-solvers, but we can often encode problems much more efficiently.
On this sheet, we will look on how to encode the Bottleneck Degree Constrained Spanning Tree problem with (cardinality) SAT and then you will try to do the same again for the Bottleneck TSP.

## The Boolean Satisfiability Problem

The boolean satisfiability problem (Satisfiability, SAT) is the first proved NP-hard problem and one of the most famous and important.
In this problem, we are given propositional formula $\phi$ on a set of boolean variables $\{x_1, \ldots, x_n\}$ in [conjunctive normal form](https://en.wikipedia.org/wiki/Conjunctive_normal_form).
Such a formula has the following form:

```math
\phi = \underbrace{(\ell_{1,1} \vee \cdots \vee \ell_{1,k_1})}_{\text{Clause 1}} \wedge \cdots \wedge \underbrace{(\ell_{m,1} \vee \cdots \vee \ell_{m,k_m})}_{\text{Clause $m$}}.
```

The $\ell_{i,j}$ are so called *literals* and have either the  form $x_u$ or $\bar{x}_u := \neg x_u$,  i.e., they are either a variable or a negation of it.
The formula $\phi$, thus, is a conjunction (AND-connections) of clauses, which are disjunctions (OR-connections) of variables or negated variables. 
An example for such a formula would be
```math
\phi_1 = (x_1 \vee \bar{x}_2 \vee x_3) \wedge (x_2 \vee x_4).
```

The boolean satisfiability problem asks if a given formula $\phi$ is *satisfiable$.
A formula  is satisfiable if there is a *satifying assignment*,
i.e., a mapping $a: \{x_1,\ldots,x_n\} \to \{\texttt{true}, \texttt{false}\}$,
that assignes every variable a boolean value, such that the formula evaluates to true.
For a formula  $\phi$ is  conjunctive normal form, this implies that every  clause needs to be satisfied, i.e.,
at least on of its literals has been satisfied.
A literal $\bar{x}_u$ is satisfied if and only if  $a(x_u) = \texttt{false}$ is;
analogous, a literal $x_u$ is satisified if and  only if $a(x_u)  = \texttt{true}$ is.
Our example $\phi_1$ is satisfied by the  assignment $x_1 = x_2 = x_3 = \texttt{false}, x_4 = \texttt{true}$.

There is a large number of highly-optimized SAT-solvers available, i.e., programs that can solve instances of this problem relatively efficiently.
The Python-package *pysat* (*python-sat*), you already installed on the first sheet, gives you the ability to easily access a collection of such SAT-solves.
We will also use this package for our example.

The formula  $\phi_1$ can be solved with the solver *Gluecard4* as follows:

```python
from pysat.solvers import Solver, Gluecard4
with Gluecard4(with_proof=False) as gc4:
	gc4.add_clause([1, -2, 3])
	gc4.add_clause([2, 4])
	if gc4.solve():
		solution = gc4.get_model() # returns [-1, -2, -3, 4]
	else:
		print("No solution!")
```

As shown in the examples, literals are encoded by integers in the API.
E.g., $x_2$ is represented by $2$ and $\bar{x}_2$ as $-2$;  $0$ is not used as it cannot be distinguished from its negation.
A clause is encoded by a list of literals.
The assignment that is returned by pysat is also a list of literals, in which every variable appears exactly once.
Thus, for every variable $i$ we will either have $i$ in the returned list if the variable is assigned true, or $-i$ if it  is assigned false.

**Caveat: In the SAT-community the term _model_ is used to describe an assignment, while we use the term as in the OR-community to describe the problem encoding.**



### Cardinality Constraints

When modelling some problem with boolean formulas, a frequent challenge is to model some cardinality constraints, i.e., from a set $L$ of literals, only at most $k$ are allowed to be satisfied.
For example, a tree should have at most $n-1$ edges selected.
If we interpret $\texttt{false}=0$ and $\texttt{true}=1$ (as commonly done in most programming languages), we can write these constraints as
```math
\sum\limits_{\ell \in L} \ell \leq k
```
Such a constraint is called *cardinality constraint*.

As this is a very common constraint, some SAT-solvers (e.g., the  previously used *Gluecard4*) support them directly (on top of the classical conjunctive normal form).
There are also automatic encodings that can convert cardinality constraints, but this is usually less efficient than telling the solver directly about the cardinality constraint, allowing it to use specialized algorithms.



##  Example 

To illustrate this technique, without directly giving you the solution for the BTSP, we again look onto how to solve the [Degree-Constrained Bottleneck Spanning Tree (DBST)](./DBST).


## Tasks

1. Model (text) the Bottleneck TSP as a decision variant, i.e., *"Is there are Hamilton circle whose longest edge has a weight of at most b?"*. You can use cardinality constraints, similar to the DBST example.
2. Implement this using pysat.
3. Compare the following three strategies to find the optimal solution: Binary search on the edge weights (as for DBST),  linear search starting from the largest edge, and linear search starting from the smallest edge. Create an experiment to evaluate which approach performs best. What may be the reason for this?
4. Design and implement a heuristic for the Bottleneck TSP that allows you to limit the search of the previous task. How much difference does this make?
5. How is the performance compared to the CP-SAT implementation? What is the size of the smallest instance you cannot solve? What is  the size of the largest instance you can still solve?
