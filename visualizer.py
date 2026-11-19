"""
Visualizer Module for N-Queens.
Provides ASCII board printing, Matplotlib chessboard rendering,
and comparative benchmarking charts.
"""

import os
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np


def print_ascii_board(board: List[int], title: str = "Chessboard Solution") -> None:
    """Print a clean ASCII chessboard representation with [Q] and [.] symbols."""
    n = len(board)
    print("\n" + "=" * (4 * n + 6))
    print(f"  {title} (N = {n})")
    print("=" * (4 * n + 6))

    top_border = "    +" + "---+" * n
    print(top_border)
    for r in range(n):
        row_str = f"{r:2d}  |"
        for c in range(n):
            if board[c] == r:
                row_str += " Q |"
            else:
                row_str += " . |"
        print(row_str)
        print(top_border)

    col_str = "     " + " ".join(f"{c:2d} " for c in range(n))
    print(col_str)
    print("=" * (4 * n + 6) + "\n")


def plot_chessboard(board: List[int], output_path: str = "output/chessboard_sample.png") -> str:
    """Render and save a chessboard diagram using Matplotlib."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    n = len(board)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Alternating tile colors
    grid = np.zeros((n, n))
    for r in range(n):
        for c in range(n):
            grid[r, c] = (r + c) % 2

    ax.imshow(grid, cmap="Blues", origin="upper", alpha=0.3)

    # Place queen symbols
    for c in range(n):
        r = board[c]
        ax.text(c, r, "♛", fontsize=28, ha="center", va="center", color="#0F172A", weight="bold")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(range(n))
    ax.set_yticklabels(range(n))
    ax.set_title(f"Sample N-Queens Solution (N = {n})", fontsize=14, fontweight="bold", pad=12)
    ax.grid(color="#334155", linewidth=1.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def plot_benchmark_charts(benchmark_data: List[Dict[str, Any]], output_dir: str = "output") -> Dict[str, str]:
    """
    Generate and save publication-grade comparison charts:
      1. Runtime vs. N (Log Scale)
      2. Success Rate vs. N (%)
      3. Average Restarts vs. N (Hill Climbing)
      4. Combined 3-panel comparison figure
    """
    os.makedirs(output_dir, exist_ok=True)

    n_vals = [d["n"] for d in benchmark_data]
    bt_times = [d["bt_runtime"] for d in benchmark_data]
    hc_times = [d["hc_runtime"] for d in benchmark_data]
    bt_success = [d["bt_success_rate"] for d in benchmark_data]
    hc_success = [d["hc_success_rate"] for d in benchmark_data]
    hc_restarts = [d["hc_avg_restarts"] for d in benchmark_data]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Combined 3-Panel Plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("N-Queens: Backtracking vs Min-Conflicts Hill Climbing (Unit II - CO2)", fontsize=15, fontweight="bold")

    # Panel 1: Runtime vs N (Log Scale)
    ax1.plot(n_vals, bt_times, "o-", color="#DC2626", linewidth=2.2, label="Backtracking (DFS)")
    ax1.plot(n_vals, hc_times, "s-", color="#2563EB", linewidth=2.2, label="Min-Conflicts (Local Search)")
    ax1.set_yscale("log")
    ax1.set_xlabel("Board Size (N)", fontweight="bold")
    ax1.set_ylabel("Execution Runtime (Seconds, Log Scale)", fontweight="bold")
    ax1.set_title("Runtime Scaling as N Grows", fontweight="bold")
    ax1.legend()
    ax1.grid(True, which="both", linestyle="--", alpha=0.5)

    # Panel 2: Success Rate vs N
    ax2.plot(n_vals, bt_success, "o--", color="#DC2626", linewidth=2.0, label="Backtracking")
    ax2.plot(n_vals, hc_success, "s-", color="#16A34A", linewidth=2.0, label="Min-Conflicts")
    ax2.set_xlabel("Board Size (N)", fontweight="bold")
    ax2.set_ylabel("Success Rate (%)", fontweight="bold")
    ax2.set_ylim(-5, 105)
    ax2.set_title("Success Rate vs. N (Within Timeout)", fontweight="bold")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.5)

    # Panel 3: Restarts Needed vs N
    bars = ax3.bar([str(n) for n in n_vals], hc_restarts, color="#F59E0B", edgecolor="#D97706", width=0.6)
    ax3.set_xlabel("Board Size (N)", fontweight="bold")
    ax3.set_ylabel("Average Restarts", fontweight="bold")
    ax3.set_title("Average Restarts (Min-Conflicts)", fontweight="bold")
    ax3.grid(True, axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        h = bar.get_height()
        ax3.annotate(f"{h:.2f}",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    combined_path = os.path.join(output_dir, "comparison_plots.png")
    plt.savefig(combined_path, dpi=250)
    plt.close()

    # 2. Individual Runtime vs N Plot
    fig_rt, ax_rt = plt.subplots(figsize=(8, 5))
    ax_rt.plot(n_vals, bt_times, "o-", color="#DC2626", linewidth=2.2, label="Backtracking")
    ax_rt.plot(n_vals, hc_times, "s-", color="#2563EB", linewidth=2.2, label="Min-Conflicts")
    ax_rt.set_yscale("log")
    ax_rt.set_xlabel("Board Size (N)", fontweight="bold")
    ax_rt.set_ylabel("Runtime in Seconds (Log Scale)", fontweight="bold")
    ax_rt.set_title("Runtime Scaling Comparison (Logarithmic)", fontweight="bold")
    ax_rt.legend()
    ax_rt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    runtime_path = os.path.join(output_dir, "runtime_vs_n.png")
    plt.savefig(runtime_path, dpi=200)
    plt.close()

    # 3. Individual Success & Restarts Plot
    fig_sr, (ax_s, ax_r) = plt.subplots(1, 2, figsize=(14, 5))
    ax_s.plot(n_vals, bt_success, "o--", color="#DC2626", linewidth=2, label="Backtracking")
    ax_s.plot(n_vals, hc_success, "s-", color="#16A34A", linewidth=2, label="Min-Conflicts")
    ax_s.set_xlabel("Board Size (N)", fontweight="bold")
    ax_s.set_ylabel("Success Rate (%)", fontweight="bold")
    ax_s.set_ylim(-5, 105)
    ax_s.set_title("Success Rate Comparison", fontweight="bold")
    ax_s.legend()
    ax_s.grid(True, linestyle="--", alpha=0.5)

    ax_r.bar([str(n) for n in n_vals], hc_restarts, color="#F59E0B", edgecolor="#D97706", width=0.5)
    ax_r.set_xlabel("Board Size (N)", fontweight="bold")
    ax_r.set_ylabel("Average Restarts", fontweight="bold")
    ax_r.set_title("Hill Climbing Average Restarts", fontweight="bold")
    ax_r.grid(True, axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    sr_path = os.path.join(output_dir, "success_and_restarts_vs_n.png")
    plt.savefig(sr_path, dpi=200)
    plt.close()

    return {
        "combined": combined_path,
        "runtime": runtime_path,
        "success_and_restarts": sr_path
    }
