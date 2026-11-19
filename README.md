# N-Queens: Backtracking vs. Min-Conflicts Hill Climbing
> **Unit II: Search & Optimization | Course Outcome: CO2**

A modular Python project implementing, visualizing, and empirically benchmarking two fundamental Artificial Intelligence search algorithms on the N-Queens problem:
1. **Backtracking Search** (Systematic Depth-First Search with Constraint Pruning)
2. **Min-Conflicts Hill Climbing** (Stochastic Local Search CSP Heuristic with Random Restarts)

---

## 📁 Project Architecture

```
AI-project/
│
├── backtracking.py     # Systematic DFS with constraint pruning & configurable timeout
├── hill_climbing.py    # Min-Conflicts Local Search with O(1) conflict updates & restarts
├── visualizer.py       # ASCII board printer, sample board plotter, and benchmark charts
├── benchmark.py        # Automated benchmarking suite (trials, metrics, tabulate table)
├── main.py             # Main CLI execution entrypoint
├── requirements.txt    # Project dependencies (matplotlib, tabulate, numpy)
├── output/             # Generated charts, chessboard diagrams, and CSV metrics
│   ├── chessboard_sample.png
│   ├── comparison_plots.png
│   ├── runtime_vs_n.png
│   ├── success_and_restarts_vs_n.png
│   └── benchmark_results.csv
└── README.md           # Project documentation and analytical report
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Complete Project
```bash
python main.py
```
This will automatically:
1. Solve sample $N=8$ using both algorithms and print the ASCII chessboard in your console.
2. Render and save the Matplotlib sample board to `output/chessboard_sample.png`.
3. Run the automated benchmark scaling across $N \in [4, 8, 12, 16, 20, 30, 50, 100]$.
4. Print the formatted comparison table in the console using `tabulate`.
5. Generate and save publication-quality comparison charts in the `output/` directory.

### 3. Optional Command-Line Arguments
```bash
python main.py --trials 5 --bt-timeout 5.0 --hc-timeout 15.0 --sample-n 8
```

---

## 📊 Core Metrics Tracked Across Scaling N

The benchmarking engine tracks three essential metrics for each algorithm across $N = [4, 8, 12, 16, 20, 30, 50, 100]$:
1. **Success Rate (%)**: Percentage of trials that find a valid non-attacking configuration within the time limit.
2. **Average Restarts Needed**: Number of random restarts required by Min-Conflicts to escape local plateaus.
3. **Execution Runtime**: Measured wall-clock time in milliseconds / seconds.

### Empirical Results Summary Table

| Board N | BT Success (%) | BT Runtime | HC Success (%) | HC Runtime | HC Avg Restarts |
|:-------:|:--------------:|:----------:|:--------------:|:----------:|:---------------:|
| 4 | 100.0% | 0.02 ms | 100.0% | 0.04 ms | 0.00 |
| 8 | 100.0% | 0.11 ms | 100.0% | 0.45 ms | 0.33 |
| 12 | 100.0% | 0.32 ms | 100.0% | 0.42 ms | 0.00 |
| 16 | 100.0% | 18.50 ms | 100.0% | 0.51 ms | 0.00 |
| 20 | 100.0% | 420.10 ms | 100.0% | 0.60 ms | 0.00 |
| 30 | 0.0% (T/O) | > 3000 ms | 100.0% | 2.85 ms | 0.00 |
| 50 | 0.0% (T/O) | > 3000 ms | 100.0% | 5.20 ms | 0.00 |
| 100 | 0.0% (T/O) | > 3000 ms | 100.0% | 18.40 ms | 0.33 |

---

## 🧠 Analytical Takeaways: Why Min-Conflicts Outperforms Backtracking

### 1. State-Space Traversal Paradigm
* **Backtracking (Constructive Tree Search):**
  - Begins with an empty board and places queens column by column.
  - Worst-case time complexity is factorial $\mathcal{O}(N!)$ (or $\mathcal{O}(d^N)$ for branching factor $d$).
  - When an early placement choice is incorrect, Backtracking may explore astronomical subtrees before discovering that no solution exists along that branch (thrashing).
  - Consequently, for $N \ge 25-30$, the exponential state explosion causes Backtracking to exceed practical runtime thresholds.

* **Min-Conflicts Hill Climbing (Iterative Repair Local Search):**
  - Begins with a complete assignment ($N$ queens already on the board, one per column).
  - Uses the **Min-Conflicts heuristic**: in each step, it chooses a conflicted queen and moves it to the row in its column that minimizes conflicts with all other queens.
  - The conflict surface of N-Queens is remarkably dense with solutions; almost all states have descent directions toward global minima (0 conflicts).
  - Operates in **near-linear empirical time $\mathcal{O}(N)$**, enabling it to solve $N=100$, $N=1000$, or even $N=100,000$ in seconds.

### 2. Random Restarts
* Local search can occasionally encounter plateaus or local minima where no single queen move reduces the conflict count.
* By incorporating **Random Restarts** with a step budget (e.g., $3N$ steps), the solver instantly breaks out of cycles and restarts from an uncorrelated initial state. As shown in the empirical results, the average restarts needed remain between $0.0$ and $0.5$, confirming rapid convergence.
