#!/usr/bin/env python3
"""
Simplex method implementation using Numpy
Problem 6 on homework 1
"""

import numpy as np


def find_pivot(m):
    """
    Takes a matrix m, finds the pivot row and column
    Returns (row, column), or None if we're done

    Runtime: a+b where a, b are size of the matrix
    """
    bottom_row = m[-1]
    last_column = m[:, -1]

    # If the bottom row is all non-negative, we're done!
    if all(bottom_row >= 0):
        return None

    # Select the pivot column (but not the last two!)
    col_i = np.argmin(bottom_row[:-2])

    # To select the pivot element, we need the ratios of this column to
    # the last column.  If that would divide by zero, we don't want that
    # element; we represent this by using +inf.
    ratios = [
        last_column[i] / m[i, col_i] if m[i, col_i] else np.inf
        for i in range(len(last_column) - 1)
    ]

    # The smallest non-negative ratio is the pivot row
    row_i = np.argmin([(r if 0 <= r else np.inf) for r in ratios])
    return (row_i, col_i)


def pivot_column(m, row_i, col_i):
    """
    Takes a matrix m, a row and a column index
    Performs row operations until that columns is all 0's except for [row] which is 1
    Returns the modified matrix

    Runtime: a*b where a, b are the size of the matrix
    """
    m = np.copy(m)  # Make a copy of the matrix, because we'll modify it

    pivot_row = m[row_i]  # Copy a *reference*!  Changes propagate back

    assert pivot_row[col_i] != 0  # If the pivot element is 0, something is wrong

    pivot_row /= pivot_row[col_i]  # Set pivot element to 1

    # Adjust the rest of the rows
    for i, row in enumerate(m):
        if i == row_i:  # Don't reduce the pivot row!
            continue
        # Reduce this row until its element in the pivot column is 0.
        # We do this by subtracting n * the pivot row, where n is the
        # value of the element that needs to go to 0, because the pivot
        # row is guaranteed to have a 1 there.
        row -= pivot_row * row[col_i]

    # Return the modified matrix
    return m


def simplex_solve(c, p):
    """
    Solve a linear-programming problem using the Simplex method

    Args:
    c - the matrix of constraints
    p - the profit function, as coefficients

    Returns the maximum profit value.
    """

    constraints = np.array(c)[:, 0:-1]
    constraints = np.append(constraints, np.identity(len(c)), axis=1)

    last_column = np.array(c)[:, -1:]  # Excludes the bottom row
    print(last_column)

    bottom_row = np.array(p)
    bottom_row = np.append(bottom_row, 0)  # Add a 0 in the value column
    bottom_row = np.array([bottom_row])
    print(bottom_row)

    m = np.append(constraints, last_column, axis=1)
    m = np.append(m, bottom_row, axis=0)

    print("Starting m:\n", m)
    while True:
        pivot = find_pivot(m)

        if pivot is None:
            print("Done!")
            # print(m)
            break

        print("Pivot:", pivot)
        (row_i, col_i) = pivot
        m = pivot_column(m, row_i, col_i)
        print("New m:\n", m)

    print("Starting m:\n", m)
    while True:
        pivot = find_pivot(m)

        if pivot is None:
            print("Done!")
            # print(m)
            break

        print("Pivot:", pivot)
        (row_i, col_i) = pivot
        m = pivot_column(m, row_i, col_i)
        print("New m:\n", m)


if __name__ == "__main__":
    m = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0, 12],
            [5, 3, 0, 0, 1, 0, 0, 20],
            [0, 9, 2, 0, 0, 1, 0, 20],
            [-8, 6, -4, 0, 0, 0, 1, 0],
        ],
        dtype=np.float64,
    )

    c = [[1, 1, 1, 12], [5, 3, 0, 20], [0, 9, 2, 20]]
    p = [8, -6, 4]

    simplex_solve(c, p)
