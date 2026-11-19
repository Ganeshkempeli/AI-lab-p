"""
Main Execution Script for N-Queens: Backtracking vs Hill Climbing.
Unit II: Search & Optimization (CO2).

Orchestrates sample solving, chessboard rendering, benchmark execution,
tabular reporting, and plot generation.
"""

import argparse
import os
import sys

from backtracking import solve_backtracking
from hill_climbing import solve_hill_climbing
from benchmark import run_benchmark, DEFAULT_N_VALUES
from visualizer import print_ascii_board, plot_chessboard, plot_benchmark_charts


def run_sample_solution(sample_n: int = 8, output_dir: str = "output"):
    """Solve sample N-Queens instance and render ASCII + Matplotlib chessboard."""
    print("=" * 80)
    print(f"  1. SAMPLE SOLUTION DEMONSTRATION (N = {sample_n})")
    print("=" * 80)

    # 1. Backtracking
    print(f"[*] Solving N={sample_n} using Backtracking...")
    bt_res = solve_backtracking(sample_n)
    print(f"    - Status:         {'SUCCESS' if bt_res['success'] else 'FAILED'}")
    print(f"    - Runtime:        {bt_res['runtime']*1000.0:.3f} ms")
    print(f"    - Nodes Explored: {bt_res['nodes_explored']:,}")

    # 2. Hill Climbing
    print(f"\n[*] Solving N={sample_n} using Min-Conflicts Hill Climbing...")
    hc_res = solve_hill_climbing(sample_n)
    print(f"    - Status:         {'SUCCESS' if hc_res['success'] else 'FAILED'}")
    print(f"    - Runtime:        {hc_res['runtime']*1000.0:.3f} ms")
    print(f"    - Restarts:       {hc_res['restarts']}")
    print(f"    - Steps:          {hc_res['total_steps']}")

    # Render board
    if hc_res["board"]:
        print_ascii_board(hc_res["board"], title=f"Sample Solution Board (Min-Conflicts, N={sample_n})")
        board_img = plot_chessboard(hc_res["board"], output_path=os.path.join(output_dir, "chessboard_sample.png"))
        print(f"[+] Saved Matplotlib sample chessboard image to: {board_img}")


def main():
    parser = argparse.ArgumentParser(description="N-Queens: Backtracking vs Hill Climbing")
    parser.add_argument("--trials", type=int, default=3, help="Number of benchmark trials per N")
    parser.add_argument("--sample-n", type=int, default=8, help="Sample N value for board visualization")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory for output plots & metrics")
    parser.add_argument("--bt-timeout", type=float, default=3.0, help="Timeout in seconds for Backtracking")
    parser.add_argument("--hc-timeout", type=float, default=10.0, help="Timeout in seconds for Hill Climbing")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Step 1: Sample Solution & Chessboard
    run_sample_solution(sample_n=args.sample_n, output_dir=args.output_dir)

    # Step 2: Automated Benchmark across scaling N
    print("\n" + "=" * 80)
    print("  2. SCALING BENCHMARK ACROSS N = [4, 8, 12, 16, 20, 30, 50, 100]")
    print("=" * 80)
    data = run_benchmark(
        n_values=DEFAULT_N_VALUES,
        trials=args.trials,
        bt_timeout=args.bt_timeout,
        hc_timeout=args.hc_timeout,
        output_dir=args.output_dir
    )

    # Step 3: Generate Matplotlib Benchmark Charts
    print("[*] Generating comparison plots...")
    paths = plot_benchmark_charts(data, output_dir=args.output_dir)
    print(f"[+] Combined comparison chart saved to:       {paths['combined']}")
    print(f"[+] Individual runtime scaling chart saved to:  {paths['runtime']}")
    print(f"[+] Success & restarts chart saved to:          {paths['success_and_restarts']}")
    print(f"[+] Metrics CSV saved to:                       {os.path.join(args.output_dir, 'benchmark_results.csv')}")

    print("\n[✔] N-Queens project execution completed successfully!")


if __name__ == "__main__":
    main()
