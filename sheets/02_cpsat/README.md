# Sheet 02: Constraint Programming with CP-SAT

You probably already know SQL as a way to declaratively work with data: Describe which data you want, and the database system will try to provide them as quickly as possible.
Now imagine the same for optimization problems: Describe the variables, an objective (a score for how good a solution is), and constraints that have to be satisfied, and the system tries to provide you with the best variable assignment (i.e., solution) satisfying all constraints.
Of course, this is a significantly harder task as the system may have to solve NP-hard problems.
Such a system also gets pretty close to generic artifical intelligence that can solve any problem you state.
While you cannot expect such a system to work for all problems you state, there actually exist some that are powerful enough for many real problems.
The general term for this is *Constraint Programming*, but things are not as much standardized as for databases and the implementations vary a lot.
Here, we will learn how to use [CP-SAT](https://developers.google.com/optimization/cp/cp_solver) of [Google's ortools-suite](https://developers.google.com/optimization) to solve combinatorial optimization problems.


## Installation

The installation of CP-SAT, which is part of the ortools package, is very easy and can
be done via pip.

```shell
pip install -U ortools
```

This command will also update an existing installation of ortools.
As this tool is in active development, it is recommendable to update it frequently.
We actually encountered wrong behavior, i.e., bugs, in earlier versions that then have
been fixed by updates (this was on some more advanced features, don't worry about
correctness with basic usage).

## Example

Before we dive into any complex problems, let us take a quick look on a simple application of CP-SAT.
This example is so simple that you could solve it by hand,
but know that CP-SAT would (probably) be fine with you adding a thousand (maybe even ten- or hundred-thousand) variables and constraints more.
However, it is not purely declarative, because it can still make a huge(!) difference how you model the problem and
getting that right takes some experience and understanding of the internals.
You can still get lucky for smaller problems (let us say few hundreds to thousands variables) and obtain optimal
solutions without having an idea of what is going on.
The solvers can handle more and more 'bad' problem models effectively with every year.

Our first problem has no deeper meaning, except of showing the basic workflow of creating the variables (x and y), adding the
constraint x+y<=30 on them, setting the objective function (maximize 30*x + 50*y), and obtaining a solution:

```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Variables
x = model.NewIntVar(0, 100, 'x')  # you always need to specify an upper bound.
y = model.NewIntVar(0, 100, 'y')
# there are also no continuous variables: You have to decide for a resolution and then work on integers.

# Constraints
model.Add(x + y <= 30)

# Objective
model.Maximize(30 * x + 50 * y)

# Solve
solver = cp_model.CpSolver()  # Contrary to Gurobi, model and solver are separated.
status = solver.Solve(model)
assert status == cp_model.OPTIMAL  # The status tells us if we were able to compute a solution.
print(f"x={solver.Value(x)},  y={solver.Value(y)}")
print("=====Stats:======")
print(solver.SolutionInfo())
print(solver.ResponseStats())
```

    x=0,  y=30
    =====Stats:======
    default_lp
    CpSolverResponse summary:
    status: OPTIMAL
    objective: 1500
    best_bound: 1500
    booleans: 1
    conflicts: 0
    branches: 1
    propagations: 0
    integer_propagations: 2
    restarts: 1
    lp_iterations: 0
    walltime: 0.00289923
    usertime: 0.00289951
    deterministic_time: 8e-08
    gap_integral: 5.11888e-07

Pretty easy, right? For solving a generic problem, not just one specific instance, you would of course create a
dictionary or list of variables and use something like `model.Add(sum(vars)<=n)`, because you don't want to create
the model by hand for larger instances.

> **Definition:** A *model* refers to a concrete problem and instance description within the framework, consisting of
> variables, constraints, and optionally an objective function. *Modelling* refers to transforming a problem (instance)
> into the corresponding framework. Be aware that the SAT-community uses the term *model* to refer to a (feasible) 
> variable assignment, i.e., solution of a SAT-formula.

Here are some further examples, if you are not yet satisfied:

* [N-queens](https://developers.google.com/optimization/cp/queens) (this one also gives you a quick introduction to
  constraint programming, but it may be misleading because CP-SAT is no classical FD-solver. This example probably has
  been modified from the previous generation, which is also explained at the end.)
* [Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling)
* [Job Shop Problem](https://developers.google.com/optimization/scheduling/job_shop)
* More examples can be found
  in [the official repository](https://github.com/google/or-tools/tree/stable/ortools/sat/samples) for multiple
  languages (yes, CP-SAT does support more than just Python). As the Python-examples are named in snake-case, they are
  at the end of the list.
