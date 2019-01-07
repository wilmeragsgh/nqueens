# N-Queens dockerized solution

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/wilmeragsgh/nqueens_dockerized/blob/master/LICENSE)
[![Travis](https://travis-ci.org/wilmeragsgh/nqueens_dockerized.svg?branch=master)](https://travis-ci.org/wilmeragsgh/nqueens_dockerized)

Dockerized solution for N-Queens problems using Explicit theorical solutions and CSP approach

This repository contains a dockerized solution for N-queens as a generalization of the [Eight queens problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle), using Explicit solutions(doesn't require combinatorial computation or search for the first solution) as referred by [Hoffman, E., Loessi, J., & Moore, R. (1969). Constructions for the Solution of the m Queens Problem. Mathematics Magazine, 42(2), 66-72. doi:10.2307/2689192](https://www.jstor.org/stable/2689192) and getting all solutions by using [python-constraint](https://labix.org/python-constraint) 

## Features

This implementation provides:

* A explicit approach for getting a single solution for given N without having to search or perform combinatorial computation
* Constrained satisfaction approach for getting all solutions for a given N if asked
* Cache for previously asked solutions (stored on DB)


## Getting started

```shell
$ git clone https://github.com/wilmeragsgh/nqueens_dockerized.git
$ cd nqueens_dockerized
$ docker-compose up --build -d & # To put it on the background while using it
$ docker exec -it app bash
```

## Example
Current version designed for  N >= 3 to use explicit solutions

```shell
$ python setup.py
$ N-Queens python solver! (Press Ctrl-C to exit)
$ Please introduce the dimensions of the board: 
4   
$ Do you want to get on [F]irst solution or [A]ll solutions?
F
$ [(1, 2), (2, 4), (3, 1), (4, 3)]
$ Solution has been inserted on DB
```

Then, next time same N will be loaded from DB

```shell
$ N-Queens python solver! (Press Ctrl-C to exit)
$ Please introduce the dimensions of the board: 
4   
$ Do you want to get on [F]irst solution or [A]ll solutions?
F
$ [(1, 2), (2, 4), (3, 1), (4, 3)]
$ Solution has been loaded from DB
```


## Testing
Current test include check the number of solution provided for a given N in [6,12] (for demostrative purposes)

```shell
$ pytest
```


## Further work
Further work may include finishing up matplot output on the docker side, given that is already included on setup.py

![matplot demo](https://raw.githubusercontent.com/wilmeragsgh/nqueens_dockerized/master/images/matplot_output_demo.png)


## License

N-queens is released under the [Apache License 2.0](LICENSE).
