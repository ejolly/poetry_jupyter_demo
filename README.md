# How to use Poetry + Jupyter together

## Overview

This is just a demo project to get acquainted with [poetry](https://python-poetry.org/docs/). Poetry is a useful tool for building, running, and testing python packages and code in an **isolated environment**, in a very simple and user-friendly way. It works a lot like other packaging and build tools like `npm` in Javascript. This repo demonstrates basic usage as well as how to make a **Jupyter Notebook** aware of a poetry environment for interactive work.

---

- [Overview](#overview)
- [Creating a new project and installing dependencies](#creating-a-new-project-and-installing-dependencies)
- [Running commands from within poetry's environment, e.g. tests](#running-commands-from-within-poetrys-environment-eg-tests)
- [Interacting with poetry's virtual env](#interacting-with-poetrys-virtual-env)
- [Auto-reflecting code changes in an interactive session (editable installs)](#auto-reflecting-code-changes-in-an-interactive-session-editable-installs)
  - [Editable install *within* poetry's environment (preferred):](#editable-install-within-poetrys-environment-preferred)
  - [Editable install *outside* poetry's environment:](#editable-install-outside-poetrys-environment)
  - [Usage](#usage)
- [Removing poetry's Python and environment from jupyter](#removing-poetrys-python-and-environment-from-jupyter)

## Creating a new project and installing dependencies

The following steps demonstrated how to get started with poetry and how this specific project was bootstrapped. In addition they demonstrate how to make a poetry project compatible with an existing jupyter notebook installation

1. Create a new project (and virtualenv)

    `poetry new demo_project`

2. Add some development dependencies for error checking, formatting, and to make poetry's virtual environment usable by jupyter/ipython

    `poetry add -D pytest pycodestyle flake8 black ipykernel`

3. Assuming you already have a working jupyter install, run the following to make poetry's python version and installed packages selectable as a jupyter notebook/lab kernel:

    `poetry run python -m ipykernel install --user --name=demo_project`

4. If you're using VSCode you can ensure it uses poetry's Python and packages for development. Open up VSCode from within the project root which should automatically create the following file, if not create it manually. 

    `.vscode/settings.json`

## Running commands from within poetry's environment, e.g. tests

`poetry run pytest`

## Interacting with poetry's virtual env

We can jump into an interactive python session *inside* poetry's virtual environment by doing the following:

```bash
poetry run shell
python
```

```python
from demo_project import hello_world
hello_world()
```

## Auto-reflecting code changes in an interactive session (editable installs)

An editable install (`pip install -e .`) allows us to immediately see changes reflected in our source code without having to restart a python or jupyter interactive session. However, because poetry uses a `pyproject.toml` and editable installs require a `setup.py`, we need to use poetry to build a source distribution of our package and then parse it to create a `setup.py`.

```bash
poetry build --format sdist
tar -xvf dist//*-`poetry version -s`.tar.gz -O '*/setup.py' > setup.py
```

Now we can perform an editable install of our package either/both inside or outside poetry's environment. It's much better to do this *within* poetry's environment to avoid screwing up any other virtual environments or conda installations you have.

### Editable install *within* poetry's environment (preferred):

`poetry run pip install -e .`

### Editable install *outside* poetry's environment:

In the example below, we perform this in a `conda` environment that already has `pip` and `ipython` installed.

**Warning:** this installs project dependencies in that environment which may cause conflicts!

```bash
# from within this project root, but in another shell that has pip, e.g. a conda env
pip install -e . 
```

### Usage

First launch ipython or jupyter notebook as you would normally do. If you performed an editable install [within poetry's environment](#editable-install-within-poetrys-environment) and made jupyter aware of the poetry environment (step 3 in [initial setup](#creating-a-new-project-and-installing-dependencies)), make sure to choose that kernel from the dropdown list in jupyter. If you instead performed an editable install [outside poetry's environment](#editable-install-outside-poetrys-environment), you should be able to choose the default kernel you use for jupyter notebooks. Then within that session/notebook do the following:

```python
# Use ipython's auto-reloading of packages
%load_ext autoreload
%autoreload 2

from demo_project import hello_world
hello_world() # works

# ... 
# perform some edits to the source code for hello_world

hello_world() # changes are reflected immediately!
```

## Removing poetry's Python and environment from jupyter

To make jupyter forget about your poetry environment just run:  

`jupyter kernelspec uninstall demo_project`

You can see a list of kernels that jupyter is aware of via:

`jupyter kernelspec list`

