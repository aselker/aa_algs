#!/usr/bin/env python3

import numpy as np


def dpll(f):
    """
    f is the input formula, as a list of 3-tuples of ints.  Each int is a
    variable index, and is negative if the variable is negated.

    Output is a list of vars, positive iff true, if the formula is satisfiable,
    or None if it isn't.
	"""

    # Empty problems have trivial solutions
    if len(f) == 0:
        return []

    # Do we already have an empty clause?
    if any([len(clause) == 0 for clause in f]):
        return None

    # Almost empty problems have almost trivial solutions
    if len(f) == 1:
        return {abs(var): (True if 0 < var else False) for var in f[0]}

    # Ok, if we've gotten here, we need to do some actual thinking.
    # For future use, let's make a copy of f, so we don't accidentally change
    # the original.
    f = copy(f)

    # Let's make a helper function which removes variables.
    def remove_variable(formula, var):
        """
		Sets 'var' to a value (True if it's positive, False if it's negative)
		Returns simplified version
		"""
        new_formula = []
        for term in formula:
            if var in term:
                pass  # It's been satisfied!
            elif -var in term:
                t = copy(term)
                t.remove(-var)
                new_formula.append(t)
            else:
                new_formula.append(term)

        return new_formula

    # Are there any unit clauses?  If so, give those variables values

    unit_vars = []  # Holds any variables which are unit-clause-able
    for clause in f:
        if len(clause) == 1:
            unit_vars.append(clause[0])

    for var in unit_vars:
        # Check if any unit vars are present positively and negatively.  Yes, it's
        # O(n^2), but it's probably faster than not doing it, and it's actually
        # mandatory in this implementation.
        if -var in unit_vars:
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

    true_branch = dpll(remove_variable(f, var))
    if true_branch is not None:
        return true_branch + unit_vars + [var]

    false_branch = dpll(remove_variable(f, -var))
    if false_branch is not None:
        return false_branch + unit_vars + [var]

    return None


def parse_dimacs(lines):
    """
    Parse a DIMACS-formatted SAT problem
    
    Return it in a form that dpll() can ingest
    """

    for line in lines:
