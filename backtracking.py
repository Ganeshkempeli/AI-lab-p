"""
Backtracking Solver for N-Queens Puzzle.
Systematic Depth-First Search with constraint pruning and timeout.
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


def solve_backtracking(
    n: int,
    timeout: float = 5.0,
    record_history: bool = False,
    max_history_frames: int = 150
) -> Dict[str, Any]:
    """
    Solve N-Queens using Backtracking with a hard timeout and optional state history.
    """
    if n in (2, 3):
        return {
            "success": False,
            "board": None,
            "runtime": 0.0,
            "nodes_explored": 0,
            "timed_out": False,
            "history": []
        }

    board = [-1] * n
    cols_used = [False] * n
    diag1_used = [False] * (2 * n)
    diag2_used = [False] * (2 * n)

    nodes_explored = 0
    start_time = time.perf_counter()
    timed_out = False
    history = []

    def backtrack(col: int) -> bool:
        nonlocal nodes_explored, timed_out
        nodes_explored += 1

        if nodes_explored % 4000 == 0:
            if time.perf_counter() - start_time > timeout:
                timed_out = True
                return False

        if col == n:
            if record_history and len(history) < max_history_frames:
                history.append(list(board))
            return True

        for row in range(n):
            d1 = row - col + (n - 1)
            d2 = row + col

            if not cols_used[row] and not diag1_used[d1] and not diag2_used[d2]:
                board[col] = row
                cols_used[row] = True
                diag1_used[d1] = True
                diag2_used[d2] = True

                if record_history and len(history) < max_history_frames:
                    history.append(list(board))

                if backtrack(col + 1):
                    return True

                if timed_out:
                    return False

                board[col] = -1
                cols_used[row] = False
                diag1_used[d1] = False
                diag2_used[d2] = False

                if record_history and len(history) < max_history_frames:
                    history.append(list(board))

        return False

    success = backtrack(0)
    elapsed = time.perf_counter() - start_time

    return {
        "success": success and not timed_out,
        "board": list(board) if success else None,
        "runtime": elapsed,
        "nodes_explored": nodes_explored,
        "timed_out": timed_out,
        "history": history
    }
