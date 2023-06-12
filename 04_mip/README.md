# Sheet 04: (Mixed) Integer (Linear) Programming

The oldest and most common technique for solving NP-hard optimization problems in practice is [(Mixed) Integer (Linear) Programming](https://en.wikipedia.org/wiki/Integer_programming).
It allows modeling problems using linear constraints and objective functions on fractional and integral variables.
Most combinatorial problems are easily expressible by Mixed Integer Programming, and most practical optimization problems can be sufficiently approximated.
The probably most famous success story of this technique is its usage by the [TSP-solver Concorde](https://en.wikipedia.org/wiki/Concorde_TSP_Solver), which was able to solve a (non-trivial) instance with over 85000 vertices to optimality.
The solvers are usually based on [Branch&Bound](https://en.wikipedia.org/wiki/Branch_and_bound), [Linear Relaxation](https://en.wikipedia.org/wiki/Linear_programming_relaxation), and [Cutting Planes](https://en.wikipedia.org/wiki/Cutting-plane_method), of which especially the last two have a serious mathematical foundation.
Mixed Integer Programming is one of the prime examples for the importance of theoretical research for practical progress.
However, you don't have to worry about any mathematical details, as modern solvers will do most of the complicated stuff for you.
This [primer](https://www.gurobi.com/resources/mixed-integer-programming-mip-a-primer-on-the-basics/) gives you some further details on how it is working.
We will focus here on just modeling the problems and using such a solver as a black box.

## Modeling

Modern MIP-solvers like Gurobi have a very expressive API that allows a declarative usage, similar to CP-SAT that we used in a [previous sheet](../02_cpsat).
The main differences are that MIP-solvers are usually limited to linear expressions (everything non-linear is usually done by inefficient tricks) but can deal much better with fractional values.
An advanced concept are also lazy constraints, that allow to efficiently add further constraints via callbacks.
In the [previous sheet](../03_card_sat), we already used iterative model building to only add constraints if necessary, with MIP-solvers this is more interactive.
Linear expressions are algebraic formulas of the first degree, i.e., variables are not multiplied or divided by each other (or themselves).
As comparisons, only $\leq, =, \geq$ are allowed, but not true inequalities, making them essentially half-planes or spaces in a high-dimensional spaces (and the solution space linear).
An example for a linear constraint is $4\cdot x_1-3 \cdot x_2+0.5\cdot x_3 \geq 7.3$.

$x_1^2 \leq 3$ would *not* be linear as $x_1$ is multiplied by itself.
Advanced functions such as $\sin x$ are of course completely forbidden (though, there are tricks to approximate them).

In a Mixed Integer Program, we have

1. Variables, which can be fractional, boolean, or integral. Fractional and integral variables can additionaly have a lower and upper bound (as opposed to CP-SAT, where bounds were mandatory).
2. A linear objective function that is to be minimized or maximized.
3. A set of linear constraints on the variables that have to be satisfied by every solution.
4. Optionally, a lazy constraints-function that gets a solution and returns nothing if the solution is feasible or returns constraints that are violated and should be added to the set. This allows to have a theoretically huge number of constraints in the model, but not in the computer memory.

You can also check out these [video lectures](https://www.gurobi.com/resource/tutorial-mixed-integer-linear-programming/).

We again provide an [example for the Degree Constrained Bottleneck Spanning Tree](./dbst_mip).

## Installation

We will use [Gurobi](https://www.gurobi.com/). In case you haven't already installed it, you can do so using Anaconda

```bash
conda config --add channels http://conda.anaconda.org/gurobi
conda install gurobi
```

You can also install it via `pip` but this may not install the license tool `grbgetkey`,  which is required for activating a full academic license.
Without such a license, only very small models and only a subset of the API can be used.
For getting such an academic license, you have to [register](https://www.gurobi.com/academia/academic-program-and-licenses/).
In the past, this page has been buggy from time to time (e.g., it forgot your student status).

Once you got a license from the webpage, you can run
```bash
grbgetkey XXXXXXXX-YOUR-KEY-XXXXXXXXXX
```
to activate  it.
You may have to be within the university's network (or use VPN) for this.

## Basic Usage

```python
import gurobipy as gp  # API
from gurobipy import GRB  # Symbols (e.g. GRB.BINARY)

model = gp.Model("mip1")  # Create a model
model.Params.TimeLimit = 90  # 90s time limit

# Create variables x (bool), y (integer), z (fractional)
x = model.addVar(vtype=GRB.BINARY, name="x")
y = model.addVar(vtype=GRB.INTEGER, name="y", lb=-GRB.INFINITY)
z = model.addVar(vtype=GRB.CONTINUOUS, name="z")
# further options: 
# * lb: float <= Lower Bound: Default Zero!!!
# * ub: float <= Upper Bound
# * obj: float <= Coefficient for the objective function.

# Objective function (Maximization)
model.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

# Constraints
model.addConstr(x + 2 * y + 3 * z <= 4, name="Constraint1")
model.addConstr(x + y >= 1, name="Constraint2")

# AND GO!
model.optimize()
```

This will give us the following log.
```
 Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (mac64)
Thread count: 4 physical cores, 8 logical processors, using up to 8 threads
Optimize a model with 2 rows, 3 columns and 5 nonzeros
Model fingerprint: 0xd685009c
Model has 1 quadratic objective term
Variable types: 1 continuous, 2 integer (1 binary)
Coefficient statistics:
  Matrix range     [1e+00, 3e+00]
  Objective range  [1e+00, 2e+00]
  QObjective range [2e+00, 2e+00]
  Bounds range     [1e+00, 1e+00]
  RHS range        [1e+00, 4e+00]
Found heuristic solution: objective 1.0000000
Presolve removed 2 rows and 3 columns
Presolve time: 0.00s
Presolve: All rows and columns removed

Explored 0 nodes (0 simplex iterations) in 0.01 seconds
Thread count was 1 (of 8 available processors)

Solution count 2: 3 1 

Optimal solution found (tolerance 1.00e-04)
Best objective 3.000000000000e+00, best bound 3.000000000000e+00, gap 0.0000%
```

```python
if model.Status == GRB.OPTIMAL: # an optimal solution has been found
    print("=== Optimal Solution ===")
    print(f"x={x.X}")
    print(f"y={y.X}")
    print(f"z={z.X}")
elif model.SolCount > 0:  # there exists a feasible solution
    print("=== Suboptimal Solution ===")
    print(f"x={x.X}")
    print(f"y={y.X}")
    print(f"z={z.X}")
else:
    print(f"Bad solution (code {model.Status}).")
    print(
        "See status codes on https://www.gurobi.com/documentation/9.5/refman/optimization_status_codes.html#sec:StatusCodes"
    )
```

> Caveat: Due to the underlying technique, the resulting variables may not be rounded. A boolean variable could take the value 0.00001 instead of 0, so you have to round to check them.

## Tasks

* Model the BTSP as a Mixed Integer Program on paper. Use the [constraint technique](https://en.wikipedia.org/wiki/Travelling_salesman_problem#Dantzig%E2%80%93Fulkerson%E2%80%93Johnson_formulation) already used for SAT to enforce a single tour and do not use the [technique](https://en.wikipedia.org/wiki/Travelling_salesman_problem#Miller%E2%80%93Tucker%E2%80%93Zemlin_formulation[21]) used with CP-SAT (as it performs poorly with MIP-solvers).
* Implement the model with Gurobi. Add the subtour elimination constraints via callbacks.
* How does the solver performs compared to the CP-SAT-solver and the SAT-solver? What is the smallest instance you can no longer solve, and what is the largest instance you still can solve in 5 minutes.
* You can provide Gurobi with initial solutions (for example, your heuristically constructed bottleneck tour). How does this influence the performance? (Lead: ["MIP starts"](https://support.gurobi.com/hc/en-us/articles/360043834831-How-do-I-use-MIP-starts-))
* Extend the solver by implementing a second version to not just search for the minimal bottleneck, but return the shortest tour with this bottleneck. Also adapt your CP-SAT solver to do so and compare the performance of the two.
