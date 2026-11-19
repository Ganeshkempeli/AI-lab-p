"""
Automated Benchmarking Suite for N-Queens.
Unit II: Search & Optimization (CO2).

Benchmarks Backtracking vs Min-Conflicts Hill Climbing across scaling N,
computes empirical metrics (Success Rate, Restarts, Runtime),
and outputs a tabulate comparison table.
"""

import csv
import json
import os
from typing import List, Dict, Any
try:
    from tabulate import tabulate
except ImportError:
    def tabulate(rows, headers=None, tablefmt=None):
        """Zero-dependency fallback table formatter."""
        if not rows:
            return ""
        header_strs = [str(h) for h in headers] if headers else []
        row_strs = [[str(cell) for cell in r] for r in rows]
        all_lines = ([header_strs] if header_strs else []) + row_strs
        widths = [max(len(all_lines[r][c]) for r in range(len(all_lines))) for c in range(len(all_lines[0]))]

        output_lines = []
        if header_strs:
            h_line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(header_strs)) + " |"
            sep = "|-" + "-|-".join("-" * widths[i] for i in range(len(header_strs))) + "-|"
            output_lines.extend([h_line, sep])

        for r in row_strs:
            output_lines.append("| " + " | ".join(r[i].ljust(widths[i]) for i in range(len(r))) + " |")

        return "\n".join(output_lines)

from backtracking import solve_backtracking
from hill_climbing import solve_hill_climbing


DEFAULT_N_VALUES = [4, 8, 12, 16, 20, 30, 50, 100]


def run_benchmark(
    n_values: List[int] = DEFAULT_N_VALUES,
    trials: int = 5,
    bt_timeout: float = 3.0,
    hc_timeout: float = 10.0,
    output_dir: str = "output"
) -> List[Dict[str, Any]]:
    """
    Run empirical benchmarks for Backtracking and Hill Climbing across N values.

    Parameters:
        n_values (List[int]): Board dimensions to test.
        trials (int): Randomized runs per N value.
        bt_timeout (float): Max seconds before Backtracking aborts.
        hc_timeout (float): Max seconds before Hill Climbing aborts.
        output_dir (str): Directory where CSV and JSON results are stored.

    Returns:
        List[Dict[str, Any]]: Aggregated metric records for each N.
    """
    os.makedirs(output_dir, exist_ok=True)
    summary_data = []

    print(f"\n[*] Running Benchmark across N = {n_values} ({trials} trials per N)...")

    for n in n_values:
        # 1. Backtracking evaluation
        bt_successes = 0
        bt_times = []
        bt_nodes = []

        for _ in range(trials):
            res = solve_backtracking(n, timeout=bt_timeout)
            if res["success"]:
                bt_successes += 1
            bt_times.append(res["runtime"])
            bt_nodes.append(res["nodes_explored"])

            # If it timed out on trial 1, skip subsequent trials to save time
            if res["timed_out"]:
                for _ in range(trials - 1):
                    bt_times.append(res["runtime"])
                    bt_nodes.append(res["nodes_explored"])
                break

        bt_success_rate = (bt_successes / trials) * 100.0
        bt_avg_time = sum(bt_times) / len(bt_times)

        # 2. Hill Climbing evaluation
        hc_successes = 0
        hc_times = []
        hc_restarts = []
        hc_steps = []

        for _ in range(trials):
            res = solve_hill_climbing(n, timeout=hc_timeout)
            if res["success"]:
                hc_successes += 1
            hc_times.append(res["runtime"])
            hc_restarts.append(res["restarts"])
            hc_steps.append(res["total_steps"])

        hc_success_rate = (hc_successes / trials) * 100.0
        hc_avg_time = sum(hc_times) / len(hc_times)
        hc_avg_restarts = sum(hc_restarts) / len(hc_restarts)

        row = {
            "n": n,
            "bt_success_rate": bt_success_rate,
            "bt_runtime": bt_avg_time,
            "bt_runtime_ms": bt_avg_time * 1000.0,
            "hc_success_rate": hc_success_rate,
            "hc_runtime": hc_avg_time,
            "hc_runtime_ms": hc_avg_time * 1000.0,
            "hc_avg_restarts": hc_avg_restarts
        }
        summary_data.append(row)

    # Print Table using tabulate
    table_rows = []
    for r in summary_data:
        bt_time_disp = f"{r['bt_runtime_ms']:.2f} ms" if r['bt_success_rate'] > 0 else f"> {bt_timeout*1000:.0f} ms (T/O)"
        hc_time_disp = f"{r['hc_runtime_ms']:.2f} ms"
        table_rows.append([
            r["n"],
            f"{r['bt_success_rate']:.1f}%",
            bt_time_disp,
            f"{r['hc_success_rate']:.1f}%",
            hc_time_disp,
            f"{r['hc_avg_restarts']:.2f}"
        ])

    headers = [
        "Board N",
        "BT Success (%)",
        "BT Runtime",
        "HC Success (%)",
        "HC Runtime",
        "HC Avg Restarts"
    ]

    print("\n" + "=" * 80)
    print("           N-QUEENS BENCHMARK: BACKTRACKING vs HILL CLIMBING")
    print("=" * 80)
    print(tabulate(table_rows, headers=headers, tablefmt="github"))
    print("=" * 80 + "\n")

    # Save to CSV
    csv_path = os.path.join(output_dir, "benchmark_results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_data[0].keys()))
        writer.writeheader()
        writer.writerows(summary_data)

    # Save to JSON
    json_path = os.path.join(output_dir, "benchmark_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)

    return summary_data
