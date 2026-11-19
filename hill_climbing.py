"""
Min-Conflicts Hill Climbing Solver for N-Queens.
Stochastic Local Search heuristic with Random Restarts.
"""

import random
import time
from typing import List, Optional, Dict, Any


def count_board_conflicts(board: List[int]) -> int:
    """Calculate the total conflicting pairs on the board."""
    if not board:
        return 0
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] != -1 and board[j] != -1:
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
    return conflicts


def solve_hill_climbing(
    n: int,
    max_restarts: int = 50,
    max_steps_per_restart: Optional[int] = None,
    timeout: float = 10.0,
    record_history: bool = False,
    max_history_frames: int = 200
) -> Dict[str, Any]:
    """
    Solve N-Queens using Min-Conflicts Hill Climbing with Random Restarts.
    """
    if n in (2, 3):
        return {
            "success": False,
            "board": None,
            "runtime": 0.0,
            "restarts": 0,
            "total_steps": 0,
            "conflicts": 1,
            "history": []
        }

    steps_limit = max_steps_per_restart if max_steps_per_restart is not None else max(200, 3 * n)
    start_time = time.perf_counter()
    total_steps = 0
    restarts = 0
    history = []

    while restarts <= max_restarts:
        if time.perf_counter() - start_time > timeout:
            break

        # Random complete initialization
        queens = [random.randint(0, n - 1) for _ in range(n)]
        init_conf = count_board_conflicts(queens)

        if record_history and len(history) < max_history_frames:
            history.append({
                "board": list(queens),
                "moved_col": -1,
                "from_row": -1,
                "to_row": -1,
                "conflicts": init_conf,
                "step": 0,
                "desc": "Initial Random Placement"
            })

        # Frequency tables for O(1) conflict updates
        row_count = [0] * n
        d1_count = [0] * (2 * n)  # row - col + (n - 1)
        d2_count = [0] * (2 * n)  # row + col

        for col in range(n):
            r = queens[col]
            row_count[r] += 1
            d1_count[r - col + (n - 1)] += 1
            d2_count[r + col] += 1

        def get_pos_conflicts(r: int, c: int) -> int:
            d1 = r - c + (n - 1)
            d2 = r + c
            return (row_count[r] - 1) + (d1_count[d1] - 1) + (d2_count[d2] - 1)

        def get_cand_conflicts(r: int, c: int, curr_r: int) -> int:
            d1 = r - c + (n - 1)
            d2 = r + c
            conf = row_count[r] + d1_count[d1] + d2_count[d2]
            if r == curr_r:
                conf -= 3
            return conf

        for _ in range(steps_limit):
            total_steps += 1

            if total_steps % 500 == 0 and (time.perf_counter() - start_time > timeout):
                elapsed = time.perf_counter() - start_time
                return {
                    "success": False,
                    "board": None,
                    "runtime": elapsed,
                    "restarts": restarts,
                    "total_steps": total_steps,
                    "conflicts": count_board_conflicts(queens),
                    "history": history
                }

            conflicted_cols = [c for c in range(n) if get_pos_conflicts(queens[c], c) > 0]

            if not conflicted_cols:
                elapsed = time.perf_counter() - start_time
                if record_history and (not history or history[-1]["board"] != queens):
                    history.append({
                        "board": list(queens),
                        "moved_col": -1,
                        "from_row": -1,
                        "to_row": -1,
                        "conflicts": 0,
                        "step": total_steps,
                        "desc": "Goal State Reached (0 Conflicts)"
                    })
                return {
                    "success": True,
                    "board": list(queens),
                    "runtime": elapsed,
                    "restarts": restarts,
                    "total_steps": total_steps,
                    "conflicts": 0,
                    "history": history
                }

            c = random.choice(conflicted_cols)
            curr_r = queens[c]

            min_c = float("inf")
            best_rows = []

            for r in range(n):
                conf = get_cand_conflicts(r, c, curr_r)
                if conf < min_c:
                    min_c = conf
                    best_rows = [r]
                elif conf == min_c:
                    best_rows.append(r)

            next_r = random.choice(best_rows)

            if next_r != curr_r:
                row_count[curr_r] -= 1
                d1_count[curr_r - c + (n - 1)] -= 1
                d2_count[curr_r + c] -= 1

                queens[c] = next_r
                row_count[next_r] += 1
                d1_count[next_r - c + (n - 1)] += 1
                d2_count[next_r + c] += 1

                if record_history and len(history) < max_history_frames:
                    history.append({
                        "board": list(queens),
                        "moved_col": c,
                        "from_row": curr_r,
                        "to_row": next_r,
                        "conflicts": count_board_conflicts(queens),
                        "step": total_steps,
                        "desc": f"Moved Col {c}: Row {curr_r} -> Row {next_r}"
                    })

        restarts += 1

    elapsed = time.perf_counter() - start_time
    return {
        "success": False,
        "board": None,
        "runtime": elapsed,
        "restarts": restarts,
        "total_steps": total_steps,
        "conflicts": -1,
        "history": history
    }
