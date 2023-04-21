# Algorithms Lab - Summer 2023

Optimization problems occur in many practical applications of computer science, such as [planning routes](https://en.wikipedia.org/wiki/Travelling_salesman_problem) or [scheduling jobs](https://en.wikipedia.org/wiki/Job-shop_scheduling).
Some of them, e.g. [shortest paths](https://en.wikipedia.org/wiki/Shortest_path_problem), are easy to solve to optimality, at least with the proper theoretical background.
Many of them are not and can be proved to be [NP-hard](https://en.wikipedia.org/wiki/NP-hardness), i.e., there is probably no algorithm that can solve _every_ instance of the problem _efficiently_ to provable _optimality_.
The most common tactic for these cases is to just implement a heuristic, e.g., a [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm).
But is this really there really no hope for an optimal algorithm?
During this lab, we will investiage three techniques that can actually compute optimal solutions in reasonable time for instances of reasonable size for many problems.
These techniques are:
* [Constraint Programming](https://en.wikipedia.org/wiki/Constraint_programming) with [CP-SAT](https://developers.google.com/optimization/cp/cp_solver). A very generic technique that allows you to specify the constraints of the problem and it will try to solve it by a portfolio of techniques, especially the next mentioned two.
* [SAT Solver](https://en.wikipedia.org/wiki/SAT_solver) that can often solve very large logical formulas, and by a clever application can also be tricked into solving optimization problems.
* [Mixed Integer Programming](https://en.wikipedia.org/wiki/Integer_programming) that can be used to solve optimization problems expressable by integer and fractional variables and linear constraints.

A trained algorithm engineer or operations researcher is actually able to model most combinatorial optimization problems with one of these techniques, even if they contain complex constraints or objective functions.
At the end of the semester, you will be able to solve many problems with these tools, too.
Of course it is not just about how well a problem can be modelled but also, how effective the underlying engine can solve it; these are NP-hard problems after all.

## Content

The lab consists of four sheets and a final project.
* In the first sheet, you will set up the programming environment and take a peek into some actual code.
* The second sheet will have you use CP-SAT, the most generic technique.
* The third sheet makes you use a SAT-solver, which are more rudimentary but can actually deal with much more variables than CP-SAT.
* The fourth sheet then makes you use a Mixed Integer Programming solver, which are especially powerful, e.g., for network problems.

In a final project, your team has to get creative and develop a solver for an NP-hard optimization problem of your choice.
We will help you select one.

## Requirements

* Good programming skills in Python, as the whole course will be in Python and there won't be time for us to teach you Python.
* Basic knowledge on algorithms. _Algorithms and Datastructures 1_ is mandatory. _Algorithms and Datastructures 2_ and _Network Algorithms_ are recommendable. If you already attended _Algorithm Engineering (Keldenich/Krupke)_ you may be overqualifyed for the first part and can directly start with a project.
* A unix system (can be a virtual machine) and basic knowledge on how to use it. It is possible to run most things also on Windows, but we cannot provide support.
* Basic skills with Git. This is actually something you can quickly learn, but you have to do it on your own.

## Lectures to go next

This lab is just a quick peek into solving NP-hard problems in practice, there is more!

* _Algorithm Engineering (Master, infrequently)_ will teach you a superset of this lab, with more details.
* _Mathematische Methode der Algorithmik (Master)_ will teach you the theoretical background of Linear Programming and Mixed Integer Programming.
* _Approximation Algorithms (Master)_ will teach you theoretical aspects of how to approximate NP-hard problems with guarantees. While this takes a theoretical point of view, the theoretical understanding can improve your practical skills on understanding and solving such problems.
