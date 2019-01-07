#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 12:49:24 2019

@author: wilmer gonzalez
"""
import sqlalchemy as db

def getExplicitSolution(n):
    """Calculating single explicit solution for a given n using guarantees
    provided by:
        - Hoffman, E., Loessi, J., & Moore, R. (1969). 
          Constructions for the Solution of the m Queens Problem. 
          Mathematics Magazine, 42(2), 66-72. doi:10.2307/2689192
          
        - Bernhardsson, B. (1991). 
          Explicit solutions to the N-queens problem for all N. 
          SGAR.
        
    Keyword arguments:
    n -- Required matrix size (n*n)/ number of queens
    """
    queens = [(0,0)] * n
    mid_n = n//2
    if n % 6 != 2:
        for i in range(1,mid_n+1):
            queens[i-1] = (i,2*i)
            queens[i-1 + mid_n] = ( (mid_n) + i,2*i - 1 )
    else:
        for i in range(1,mid_n+1):
            queens[i-1] = (i, 1 + ((2*(i-1) + (mid_n) - 1) % n))
            queens[i-1 + mid_n] = (n + 1 - i,n - ((2*(i-1) + (mid_n) - 1) % n))
    return(queens)
    
def getFirstSolution(n):
    """Interface for calculating single solution
        
    Keyword arguments:
    n -- Required matrix size (n*n)/ number of queens
    """
    if n % 2 == 0: # Checking case for N to provide explicit solution
        solutions = getExplicitSolution(n)
    else:
        solutions = getExplicitSolution(n-1)
        solutions.append((n,n))
    return(solutions)

def getAllSolutions(n):
    """Interface for calculating every solution using python-constraint package
        
    Keyword arguments:
    n -- Required matrix size (n*n)/ number of queens
    """
    from constraint import Problem
    problem = Problem()
    cols = range(n)
    rows = range(n)
    problem.addVariables(cols, rows)
    for col1 in cols:
        for col2 in cols:
            if col1 < col2:
                problem.addConstraint(lambda row1, row2, col1=col1, col2=col2:
                                        abs(row1-row2) != abs(col1-col2)
                                        and row1 != row2, (col1, col2))
    solutions = problem.getSolutions()
    solutions_arr = []
    for s in solutions:
        solutions_arr.append([(i,j) for i,j in s.items()])
    return(solutions_arr)

def printSol(solution):
    """Interface for plotting resulting solution with stout"""
    print(solution)

def printSolution(solution):
    """Interface for plotting resulting solution with matplotlib
        
    Keyword arguments:
    solution -- placement of every queen on the board
    """
    from mlxtend.plotting import checkerboard_plot
    import matplotlib.pyplot as plt
    import numpy as np
    n = len(solution)
    board = np.array([' '] * (n*n))
    board = board.reshape(n,n)
    for qi,qj in solution:
        board[qi-1][qj-1] = 'Q'
    checkerboard_plot(board,
                      fmt="%s",
                      col_labels=["%d" % i for i in range(1,n+1)],
                      row_labels=["%d" % i for i in range(1,n+1)])
    plt.show()


def initDB(user='user',passwd='pass',db_name='nqueens'):
    """Postgres db initializer"""
    engine = db.create_engine('postgresql://'+user+':'+passwd+'@postgresql/'+db_name)
    connection = engine.connect()
    metadata = db.MetaData()
    sol_db = db.Table('sol_db', metadata,
                      db.Column('id',db.Integer()),
                      db.Column('N', db.Integer()),
                      db.Column('row', db.Integer()),
                      db.Column('column', db.Integer()))
    metadata.create_all(engine)
    return(connection,sol_db)
    
    
def saveSolution(solution,con,sol_db,ix):
    """Store solution to db
    
    Keyword arguments:
    solution -- placement of every queen on the board
    con -- DB connection
    sol_db -- Solutions DB
    ix -- Solution ID"""
    query = db.insert(sol_db)
    values = [{'N':len(solution),
               'id':ix,
               'row':qi,
               'column':qj} for qi,qj in solution]
    con.execute(query,values)
    
def getCachedSolution(N,con,sol_db):
    """Search cached solutions for given N
    
    Keyword arguments:
    N -- Required matrix size (n*n)/ number of queens
    con -- DB connection
    sol_db -- Solutions DB"""
    res = con.execute(db.select([sol_db]).where(sol_db.columns.N==N)).fetchall()
    solution = []
    if(len(res)>0):
        id_s = min([a for a,b,c,d in res])
        solution = [(qi,qj) for i,n,qi,qj in res if i==id_s]
    return(solution)
     

N_SOLUTIONS = [1,1,0,0,2,10,4,40,92,352,724,2680,14200,73712,
               365596,2279184,14772512,95815104,666090624,
               4968057848,39029188884,314666222712,2691008701644,
               24233937684440,227514171973736,2207893435808352,
               22317699616364044,234907967154122528]
# Number of solutions for n matrix size, discovered thanks to the OEIS 
# https://oeis.org/A002562/list


try:
    ix = 1
    while True:
        con,sol_db = initDB()
        print("N-Queens python solver! (Press Ctrl-C to exit)")
        print("Please introduce the dimensions of the board: ")
        n = int(input())
        print("Do you want to get on [F]irst solution or [A]ll solutions?")
        n_sol = input()
        if(n_sol=='F'):
            cachedSol = getCachedSolution(n,con,sol_db)
            if(len(cachedSol)==0):
                solution = getFirstSolution(n)
                printSol(solution)
                saveSolution(solution,con,sol_db,ix)
                print('Solution has been inserted on DB')
                ix += 1
            else:
                printSol(cachedSol)
                print('Solution has been loaded from DB')
        else:
            if(n_sol=='A'):
                cachedSol = getCachedSolution(n,con,sol_db)
                if(len(cachedSol)==0):
                    solution = getAllSolutions(n)
                    print('Showing only first solution')
                    printSol(solution[0])
                    for s in solution:
                        saveSolution(s,con,sol_db,ix)
                        ix += 1
                    print('All solutions has been inserted on DB')
                else:
                    printSol(cachedSol)
                    print('Solution has been loaded from DB')
except KeyboardInterrupt:
    print('Goodbye!')
