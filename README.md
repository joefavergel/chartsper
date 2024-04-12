<img heigth="8" src="https://i.imgur.com/DTmSLPg.png" alt="chartsper">

<h1 align="center">🎸 Chartsper 🎮</h1>

<p align="center">Supervised Fine-Tuning (SFT) for Guitar Note Recognition</p>

<p align="center">
  <a href="https://joefavergel.dev/">joefavergel.dev</a> 
  <br> <br>
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#contribute">Contribute</a>
  <br> <br>
  <a target="_blank">
    <img src="https://github.com/QData/TextAttack/workflows/Github%20PyTest/badge.svg" alt="Github Runner Covergae Status">
  </a>
  <a href="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000">
    <img src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" alt="Version" height="18">
  </a>
  <a  href="[https://twitter.com/joefavergel](https://twitter.com/joefavergel)"  target="_blank">
    <img  alt="Twitter: joefavergel"  src="https://img.shields.io/twitter/follow/joefavergel.svg?style=social"/>
  </a>
</p>


---

## About

`chartsper` is a Python library that documents the application of [Supervised Fine-Tuning (SFT)](https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)) to pre-trained deep learning models to recognize guitar note [charts](https://wiki.clonehero.net/books/general-info/page/dictionary#bkmrk-chart) for rhythm games as [Clone Hero](https://clonehero.net/).


---

## Features

`chartsper` is built on `Python 3.11` with [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/), [librosa](https://librosa.org/doc/latest/index.html), [transformers](https://huggingface.co/docs/transformers/index) among others, to preprocess the data, build the machine learning models, and visualize the results. 

For development, the library use:

- Formatting with [black](https://github.com/psf/black)
- Import sorting with [isort](https://github.com/timothycrosley/isort)
- Linting with [flake8](http://flake8.pycqa.org/en/latest/)
- Git hooks that run all the above with [pre-commit](https://pre-commit.com/)
- Testing with [pytest](https://docs.pytest.org/en/latest/)


---

## Contribute

First, make sure that before enabling pipenv, you must have `Python 3.9` installed. If it does not correspond to the version you have installed, you can create a conda environment with:

```sh
# Create and activate python 3.9 virutal environment
$ conda create -n py39 python=3.11
$ conda activate py311
```

Now, you can managament the project dependencies with `Pipenv`. To create de virtual environment and install all dependencies follow:

```sh
# Install pipx if pipenv and cookiecutter are not installed
$ python3 -m pip install pipx
$ python3 -m pipx ensurepath

# Install pipenv using pipx
$ pipx install poetry

# Create pipenv virtual environment
$ poetry shell

# Install dependencies
$ poetry install --dev
```

Once the dependencies are installed, we need to notify `Jupyter` of this new `Python` environment by creating a kernel:

```sh
$ ipython kernel install --user --name KERNEL_NAME
```

Finally, before making any changes to the library, be sure to review the [GitFlow](https://www.atlassian.com/es/git/tutorials/comparing-workflows/gitflow-workflow) guide and make any changes outside of the `master` branch.
