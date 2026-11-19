"""
Backtracking Solver for N-Queens Puzzle.
Unit II: Search & Optimization (CO2).

Implements systematic Depth-First Search with constraint pruning
and a configurable timeout to prevent hanging on large N.
"""

import time
from typing import List, Optional, Dict, Any


def is_safe(board: List[int], row: int, col: int) -> bool:
    """Check if placing a queen at (row, col) conflicts with previous columns."""
    for prev_col in range(col):
        prev_row = board[prev_col]
        if prev_row == row or abs(prev_row - row) == abs(prev_col - col):
            return False
    return True


def solve_backtracking(n: int, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Solve N-Queens using Backtracking with a hard timeout.

    Parameters:
        n (int): Board dimension (N x N) and queen count.
        timeout (float): Max runtime in seconds before aborting.

    Returns:
        dict: {
            "success": bool,
            "board": Optional[List[int]],
            "runtime": float (seconds),
            "nodes_explored": int,
            "timed_out": bool
        }
    """
    if n in (2, 3):
        return {
            "success": False,
            "board": None,
            "runtime": 0.0,
            "nodes_explored": 0,
            "timed_out": False
        }

    board = [-1] * n
    cols_used = [False] * n
    diag1_used = [False] * (2 * n)  # row - col + (n - 1)
    diag2_used = [False] * (2 * n)  # row + col

    nodes_explored = 0
    start_time = time.perf_counter()
    timed_out = False

    def backtrack(col: int) -> bool:
        nonlocal nodes_explored, timed_out
        nodes_explored += 1

        # Periodic timeout check
        if nodes_explored % 4000 == 0:
            if time.perf_counter() - start_time > timeout:
                timed_out = True
                return False

        if col == n:
            return True

        for row in range(n):
            d1 = row - col + (n - 1)
            d2 = row + col

            if not cols_used[row] and not diag1_used[d1] and not diag2_used[d2]:
                board[col] = row
                cols_used[row] = True
                diag1_used[d1] = True
                diag2_used[d2] = True

                if backtrack(col + 1):
                    return True

                if timed_out:
                    return False

                board[col] = -1
                cols_used[row] = False
                diag1_used[d1] = False
                diag2_used[d2] = False

        return False

    success = backtrack(0)
    elapsed = time.perf_counter() - start_time

    return {
        "success": success and not timed_out,
        "board": list(board) if success else None,
        "runtime": elapsed,
        "nodes_explored": nodes_explored,
        "timed_out": timed_out
    }
