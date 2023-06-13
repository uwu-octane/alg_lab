# alg_lab

python solver für NP hard Problem 

Infor von Projekt:

Optimization problems occur in many practical applications of computer science, such as planning routes or scheduling jobs.
Some of them, e.g. shortest paths, are easy to solve to optimality, at least with the proper theoretical background.
Many of them are not and can be proved to be NP-hard, i.e., there is probably no algorithm that can solve every instance of the problem efficiently to provable optimality.
The most common tactic for these cases is to just implement a heuristic, e.g., a genetic algorithm.
But is this really there really no hope for an optimal algorithm?
During this lab, we will investigate three techniques that can actually compute optimal solutions in reasonable time for instances of reasonable size for many problems.
These techniques are:


Constraint Programming with CP-SAT. A very generic technique that allows you to specify the constraints of the problem and it will try to solve it by a portfolio of techniques, especially the next mentioned two.

SAT Solver that can often solve very large logical formulas, and by a clever application can also be tricked into solving optimization problems.

Mixed Integer Programming that can be used to solve optimization problems expressible by integer and fractional variables and linear constraints.

A trained algorithm engineer or operations researcher is actually able to model most combinatorial optimization problems with one of these techniques, even if they contain complex constraints or objective functions.
At the end of the semester, you will be able to solve many problems with these tools, too.
Of course it is not just about how well a problem can be modelled but also, how effective the underlying engine can solve it; these are NP-hard problems after all.

Content
The lab consists of four sheets and a final project.

In the first sheet, you will set up the programming environment and take a peek into some actual code.
The second sheet will have you use CP-SAT, the most generic technique.
The third sheet makes you use a SAT-solver, which are more rudimentary but can actually deal with much more variables than CP-SAT.
The fourth sheet then makes you use a Mixed Integer Programming solver, which are especially powerful, e.g., for network problems.

In a final project, your team has to get creative and develop a solver for an NP-hard optimization problem of your choice.
We will help you select one.
