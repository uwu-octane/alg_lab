# First Sheet: Setup and a first look into examples

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

