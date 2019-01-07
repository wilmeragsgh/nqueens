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

N_SOLUTIONS = [1,1,0,0,2,10,4,40,92,352,724,2680,14200,73712,
               365596,2279184,14772512,95815104,666090624,
               4968057848,39029188884,314666222712,2691008701644,
               24233937684440,227514171973736,2207893435808352,
               22317699616364044,234907967154122528]

def test_getAllSolutions():
    for k in range(6,12):
        assert len(getAllSolutions(k)) == N_SOLUTIONS[k]
