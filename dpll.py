#!/usr/bin/env python3

import sys
import numpy as np


def dpll(f):
    """
    f is the input formula, as a list of 3-tuples of ints.  Each int is a
    variable index, and is negative if the variable is negated.

    Output:
        If the formula is satisfiable, a list of variables, positive iff true.
        Variables will be listed only if their value matters; they'll be left
        out if they can be true or false.
        
        If the formula is not satisfiable, then None.
    """

    print(f"Beginning work on {f}...")

    # Empty problems have trivial solutions
    if len(f) == 0:
        print("Return [] on empty formula")
        return []

    # Do we already have an empty clause?
    if any([len(clause) == 0 for clause in f]):
        print("Return None on empty clause")
        return None

    # Almost empty problems have almost trivial solutions
    if len(f) == 1:
        print(f"Return {f[0]} on only one clause")
        return f[0]

    # Ok, if we've gotten here, we need to do some actual thinking.
    # For future use, let's make a copy of f, so we don't accidentally change
    # the original.
    f = f.copy()

    # Let's make a helper function which removes variables.
    def remove_variable(formula, var):
        """
        Sets 'var' to a value (True if it's positive, False if it's negative)
        Returns simplified version
        """

        print(f"Removing {var} from {formula}")

        new_formula = []
        for term in formula:
            if var in term:
                pass  # It's been satisfied!
            elif -var in term:
                t = term.copy()
                t.remove(-var)
                new_formula.append(t)
            else:
                new_formula.append(term)

        return new_formula

    # Are there any unit clauses?  If so, give those variables values
    unit_vars = []  # Holds any variables which are unit-clause-able
    for clause in f:
        if len(clause) == 1:
            print(f"Set {clause[0]} from unit clause")
            unit_vars.append(clause[0])

    # Also look for pure literals
    # (Use a Python dict for deduplication)
    vars_used = {}
    for clause in f:
        for var in clause:
            vars_used[var] = None

    pure_literals = []
    for var in vars_used:
        if -var not in vars_used:
            print(f"Set {var} as a pure literal")
            pure_literals.append(var)

    # Combine lists of variables we have to set into a dict, for deduplication
    vars_to_set = {var: None for var in unit_vars}
    for var in pure_literals:
        vars_to_set[var] = None

    for var in vars_to_set.keys():
        # Check if any unit vars are present positively and negatively.  Yes, it's
        # O(n^2), but it's probably faster than not doing it, and it's actually
        # mandatory in this implementation.
        if -var in vars_to_set:
            return None

        f = remove_variable(f, var)

    # Check again to see if we've hit something trivially true or false
    if len(f) == 0:
        return unit_vars

    if any([len(clause) == 0 for clause in f]):
        return None

    # Ok, we have to take a guess.  Try a value, recurse, then try the other.
    # It's important to choose a variable in a way that doesn't cause use to
    # accidentally redo work; we choose the smallest numerically.

    smallest_var = np.inf
    for clause in f:
        for var in clause:
            smallest_var = min(abs(var), smallest_var)

    print(f"Trying branch with {var}...")
    true_branch = dpll(remove_variable(f, var))
    if true_branch is not None:
        print(f"Took branch with {var}")
        return true_branch + list(vars_to_set) + [var]

    print(f"Trying branch with {-var}...")
    false_branch = dpll(remove_variable(f, -var))
    if false_branch is not None:
        print(f"Took branch with {-var}")
        return false_branch + list(vars_to_set) + [-var]

    return None


def parse_dimacs(lines):
    """
    Parse a DIMACS-formatted SAT problem
    
    Return it in a form that dpll() can ingest
    """

    num_vars = None
    num_clauses = None
    clauses = []

    for line in lines:
        words = line.split(" ")
        words = [word.replace("\r", "").replace("\n", "") for word in words]
        if (len(words) == 0) or words[0] == "c":
            pass
        elif words[0] == "p":
            assert words[1] == "cnf"
            num_vars = int(words[2])
            num_clauses = int(words[3])
        else:
            clause = [int(word) for word in words[:-1]]
            clauses.append(clause)
            assert words[-1] == "0"

    assert len(clauses) == num_clauses

    return clauses


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        clauses = parse_dimacs(f.readlines())

    print("Formula to solve:")
    print(clauses)

    res = dpll(clauses)

    print("")
    print(f"Result: {res}")

    """
    A few runs:
    (intermediate output omitted for legibility)

    input:
    p cnf 2 3
    1 -2 0
    1 2 0
    -1 -2 0

    output:
    [1, -2]

    input:
    p cnf 3 3
    1 2 3 0
    -1 -2 3 0
    -1 2 -3 0

    output:
    [1, -2, 3]

    input:
    p cnf 5 3
    1 -5 4 0
    -1 5 3 4 0
    -3 -4 0

    output:
    [1, -5, 3, -4]

    input:
    p cnf 5 7
    1 -5 4 0
    -1 5 3 4 0
    -3 -4 0
    1 -5 3 4 0
    3 -4 0
    -1 5 4 0
    -1 -5 0

    output:
    [-1, -4, -5]

    input:
    p cnf 5 8
    1 -5 4 0
    -1 5 3 4 0
    -3 -4 0
    1 -5 3 4 0
    3 -4 0
    -1 5 4 0
    -1 -5 0
    1 4 0

    output:
    None
    """
