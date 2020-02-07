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

    if all(bottom_row >= 0):
        return None

    # Select the pivot column (but not the last two!)
    col_i = np.argmin(bottom_row[:-2])

    # Divide the column (except the bottom row), returning +inf if by zero
    ratios = [
        last_column[i] / m[i, col_i] if m[i, col_i] else np.inf
        # np.abs(last_column[i] / m[i, col_i]) if m[i, col_i] else np.inf
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

    Runtime: TBD
    """
    m = np.copy(m)  # Make a copy of the matrix, because we'll modify it

    pivot_row = m[row_i]  # Copy a *reference*!  Changes propagate back

    assert pivot_row[col_i] != 0  # If the pivot element is 0, something is wrong

    pivot_row /= pivot_row[col_i]  # Set pivot element to 1

    # Adjust the rest of the rows
    for i, row in enumerate(m):
        if i == row_i:
            continue
        row -= pivot_row * row[col_i]

    return m


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
