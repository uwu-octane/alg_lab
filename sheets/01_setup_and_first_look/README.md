# First Sheet: Setup and a first look into examples

This first sheet will only let you set up a working development environment and take a first look into some examples.
You won't have to code anything on your own, yet, just getting ready.

## Task 1: Set up your environment

In order to properly participate in this lab, you need to have a working development environment.
We recommand to use a Linux or Mac system and can only provide support for those.
If you are using Windows, you can simply install a virtual machine with, e.g., Ubuntu.

Follow the following steps:

### Install Anaconda

[Anaconda](https://www.anaconda.com/) is a plattform for developing and deploying Python projects.
Most importantly, it comes with a powerful package manager named [conda](https://docs.conda.io/en/latest/).
It can not only install binary package but even a complete Python distribution.
One of the tools we are using can only be fully installed in Conda but not using [pip](https://pypi.org/project/pip/).
We also need specific Python versions and as every system ships its own, it is easier to use Anaconda.

Download the matching installer [here](https://www.anaconda.com/download#downloads) and run in.
You can find a more detailed guide for Linux [here](https://docs.anaconda.com/free/anaconda/install/linux/) or just execute the following steps.
```sh
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
chmod +X Anaconda3-2023.03-Linux-x86_64.sh
./Anaconda3-2023.03-Linux-x86_64.sh
```

You need to let the installer modify your shell configuration (`.bashrc`, `.zshrc`, etc.) such that it can load automatically.
If you don't want the conda environment to automatically load, run
```sh
conda config --set auto_activate_base false
```

### Create Conda Environment

We need Python 3.10, as some pacakges are not yet ready for later versions (this is due to high-perfomant but less compatible native bindings).
To create a matching environment, run
```sh
conda create -n alglab python=3.10
```
Finally, run
```sh
conda activate alglab
```
to activate the environment.
In the end, you can leave it again with `conda deactivate`.

### Install packages

Run in the `alglab` environment the following commands.
```sh
# Basics
conda install ipython numpy scipy networkx jupyterlab
# Gurobi
conda install -c gurobi gurobi
# Pip only packages
pip install -U ortools python-sat
```

### Get a Gurobi license

We are going to use the commercial Mixed Integer Programming solver [Gurobi](https://www.gurobi.com/).
While we prefer open source tools, Gurobi is in our experience simply far ahead of the open source competition and we want to use the easiest and most powerful tools in this lab.
You need to get a [free academic license](https://www.gurobi.com/academia/academic-program-and-licenses/) by creating an account and then using `grbgetkey` which has already been installed in the previous step.

### Get a proper IDE

Coding in Python gets much easier if you are using a good IDE.
We recommand PyCharm or Visual Studio Code (with corresponding plugins).

### Check you environment

Check you environment by running the [jupyter](https://jupyter.org/) notebooks of all three examples.
Just download the folder with all three examples and run `jupyterlab .` in it (everything of course in the conda environment `alglab`).
Then a brower tab will open and you can navigate to the corresponding file and select `run all`.
You will see the cells refresh, hopefully without any errors.
If you are confused, there are lots of tutorials on Jupyter out there.
If you have errors, try to encode them and check if you did anything wrong during the installation (after this fails, ask your teammates, and if even they cannot help you, ask us).

With PyCharm and Visual Studio Code, there are integrated plugins and you won't need to run `jupyterlab` or use your browser.

| Every participant has to show individually that he/she has a working environment, as this is of fundamental importance. We will do this remotely via screen sharing, such that you can also use your desktop computer.

## Task 2: Take a look into the code of the examples

We implemented three examples, one for every technique, for you.
These are first meant to check that your environment is actually working, and second, to take a peek into one uses these.
Every technique is used for a different, but relatively easy to describe, optimization problem.

* [Solving N-Partition with CP-SAT](./examples/constraint_programming/n_partition). Here we are using the most generic solver to solve the [problem](https://en.wikipedia.org/wiki/Multiway_number_partitioning) that is easiest to model mathematically.
* [Solving Feedback Vertex Cover with a SAT-solver](./examples/cardinality_sat/feedback_vertex_cover). Here we use a simple SAT-solver to optimize the graph problem [Feedback Vertex Set](https://en.wikipedia.org/wiki/Feedback_vertex_set).
* [Solving the Steiner Tree Problem with a Mixed Integer Programming solver](./examples/mixed_integer_programming/steiner_tree). Here we use Mixed Integer Programming to compute a minimal [Steiner Tree in Graphs](https://en.wikipedia.org/wiki/Feedback_vertex_set).

This task may look like much but actually we just want you to spent a few hours looking onto the examples and how one can communicate a problem to these tools.
It is not about being able to do it yourself, just about having a rough idea of what may be going on.
You will pass this task if you can convince us that you tried to answer the following questions (and dicussed it in the group).

### 1. Try to give a mathematical definition of the three problems.

This is not about modelling these problems yourself, but just about knowing what a precise problem definition is and to know what problem you are dealing with.
In order to use any of the techniques, we first have to be able to actually describe the problem to a computer.
Thus, feel free to search online for a definition and copy it.
You can also extract it from the code.
The definition for these problems should be just some _variables_, a few rules, or as we call them, _constraints_, and an _objective function_.

As an example, let us take a look on the Minimum Spanning Tree problem.
We are given a graph `G=(V,E)` with edge weight `w: E-> float`.
Let us use the boolean variables `x[e] for all e in E` with `x[e]==1` if e is in the MST, and `x[e]==0` otherwise.
As we are using the Minimum Spanning Tree, the objective is `SUM[e in E] w(e)*x[e]`.
The constraints are `SUM[e in E] x[e] == |V|-1` to enforce exactly `|V|-1` edges, and for every real and not-empty subset V' of V, `SUM[uv with u in V' and w not in V'] x[uv] >= 1` to make sure that every component is connected to the remaining graph.
We could actually skip the first constraint, as the objective will make sure we will not use more edges than necessary.

We will ask you to give us a quick informal defintion of the problems (which can be an example) and the show us the mathematical definition (with a rough idea what it states).

### 2. Get a grasp on how the examples use the corresponding solver.

Look into the code of the examples.
They are reasonably short and extensively documented.
How is the problem communicated to the individual solvers (CP-SAT, SAT, MIP)?
Can you identify the constraints?
What are the commonalities, what are the differences of their usage?

You do not have to look into CP-SAT, SAT, or MIP but can treat them as a black box.
Taking a look into their documentation, however, may be useful.

