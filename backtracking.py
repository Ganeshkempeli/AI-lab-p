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
    max_history_frames: int = 200
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

    if record_history:
        history.append({
            "board": list(board),
            "moved_col": -1,
            "from_row": -1,
            "to_row": -1,
            "conflicts": 0,
            "step": 0,
            "desc": "Initial Empty Board"
        })

    def backtrack(col: int) -> bool:
        nonlocal nodes_explored, timed_out
        nodes_explored += 1

        if nodes_explored % 4000 == 0:
            if time.perf_counter() - start_time > timeout:
                timed_out = True
                return False

        if col == n:
            if record_history and len(history) < max_history_frames:
                history.append({
                    "board": list(board),
                    "moved_col": col - 1,
                    "from_row": -1,
                    "to_row": board[col - 1],
                    "conflicts": 0,
                    "step": nodes_explored,
                    "desc": "Goal State Reached (All Queens Placed)"
                })
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
                    history.append({
                        "board": list(board),
                        "moved_col": col,
                        "from_row": -1,
                        "to_row": row,
                        "conflicts": 0,
                        "step": nodes_explored,
                        "desc": f"Col {col}: Placed Queen at Row {row}"
                    })

                if backtrack(col + 1):
                    return True

                if timed_out:
                    return False

                board[col] = -1
                cols_used[row] = False
                diag1_used[d1] = False
                diag2_used[d2] = False

                if record_history and len(history) < max_history_frames:
                    history.append({
                        "board": list(board),
                        "moved_col": col,
                        "from_row": row,
                        "to_row": -1,
                        "conflicts": 0,
                        "step": nodes_explored,
                        "desc": f"Col {col}: Backtracked from Row {row}"
                    })

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
