"""
N-Queens: Backtracking vs Hill Climbing
Clean Interactive Dashboard with Dedicated Dynamic Queen Prototype.
"""

import time
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from backtracking import solve_backtracking
from hill_climbing import solve_hill_climbing, count_board_conflicts
from visualizer import plot_benchmark_charts
from benchmark import run_benchmark, DEFAULT_N_VALUES

# Page Config
st.set_page_config(
    page_title="N-Queens: Backtracking vs Hill Climbing",
    page_icon="♛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, Modern Minimalist CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 1.0rem;
        padding-bottom: 2rem;
    }
    .clean-header {
        background: #0F172A;
        padding: 1.2rem 1.6rem;
        border-radius: 10px;
        color: #F8FAFC;
        margin-bottom: 1.0rem;
        border: 1px solid #1E293B;
    }
    .clean-header h1 {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .metric-row {
        display: flex;
        gap: 0.7rem;
        margin-bottom: 0.8rem;
    }
    .mini-card {
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.55rem 0.75rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .mini-card-title {
        color: #64748B;
        font-size: 0.70rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .mini-card-val {
        color: #0F172A;
        font-size: 1.20rem;
        font-weight: 700;
        margin-top: 0.15rem;
    }
    .val-success {
        color: #16A34A !important;
    }
    .val-fail {
        color: #DC2626 !important;
    }
    .board-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0.5rem 0;
    }
    .board-grid {
        display: grid;
        border: 3px solid #0F172A;
        border-radius: 6px;
        background-color: #0F172A;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
        overflow: hidden;
    }
    .board-cell {
        display: flex;
        justify-content: center;
        align-items: center;
        user-select: none;
    }
    .tile-light {
        background-color: #F8FAFC;
    }
    .tile-dark {
        background-color: #94A3B8;
    }
    .queen-piece {
        color: #0F172A;
        filter: drop-shadow(0 2px 3px rgba(0,0,0,0.35));
    }
    .tile-active {
        background: radial-gradient(circle, rgba(234,179,8,0.45) 0%, rgba(202,138,4,0.2) 100%);
    }
    .tile-moved {
        background: radial-gradient(circle, rgba(239,68,68,0.55) 0%, rgba(220,38,38,0.25) 100%) !important;
        outline: 2px solid #DC2626;
    }
    .speedup-pill {
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    .hud-box {
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1.0rem;
    }
    .hud-metric {
        font-size: 1.15rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


def render_board(board: list, n: int, active_col: int = -1, title: str = ""):
    """Renders a responsive, interactive HTML chessboard with queen pieces and active highlights."""
    if not board:
        return

    cell_size = max(24, min(48, int(390 / n)))
    font_size = int(cell_size * 0.72)

    if title:
        st.markdown(f"<p style='text-align: center; font-weight: 700; margin-bottom: 0.3rem;'>{title}</p>", unsafe_allow_html=True)

    html = f"""
    <div class="board-wrapper">
        <div class="board-grid" style="
            grid-template-columns: repeat({n}, {cell_size}px);
            grid-template-rows: repeat({n}, {cell_size}px);
        ">
    """
    for r in range(n):
        for c in range(n):
            is_light = (r + c) % 2 == 0
            tile_cls = "tile-light" if is_light else "tile-dark"
            has_queen = (c < len(board) and board[c] == r)

            if has_queen:
                if c == active_col:
                    active_cls = " tile-moved"
                else:
                    active_cls = " tile-active"
            else:
                active_cls = ""

            queen_symbol = f"<span class='queen-piece' style='font-size: {font_size}px;'>♛</span>" if has_queen else ""
            html += f"<div class='board-cell {tile_cls}{active_cls}' style='width:{cell_size}px; height:{cell_size}px;'>{queen_symbol}</div>"

    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


# Clean Header
st.markdown("""
<div class="clean-header">
    <h1>♛ N-Queens: Backtracking vs Hill Climbing</h1>
</div>
""", unsafe_allow_html=True)

# Dedicated Navigation Tabs (Including dedicated Dynamic Prototype page)
tab_solver, tab_prototype, tab_benchmarks = st.tabs([
    "♛ Live Solver",
    "🎬 Dynamic Queen Prototype",
    "📊 Performance Benchmark"
])

# =============================================================================
# PAGE 1: LIVE SOLVER
# =============================================================================
with tab_solver:
    col_n, col_presets, col_btn = st.columns([1.5, 2.5, 1.2])

    with col_n:
        n_input = st.slider("Board Dimension (N):", min_value=4, max_value=20, value=8, step=1)

    with col_presets:
        st.write("")
        p1, p2, p3, p4 = st.columns(4)
        if p1.button("N = 4", key="p1_4", use_container_width=True):
            n_input = 4
        if p2.button("N = 8", key="p1_8", use_container_width=True):
            n_input = 8
        if p3.button("N = 12", key="p1_12", use_container_width=True):
            n_input = 12
        if p4.button("N = 16", key="p1_16", use_container_width=True):
            n_input = 16

    with col_btn:
        st.write("")
        run_solve = st.button("🚀 Solve Both", type="primary", use_container_width=True)

    if run_solve or "cached_n" not in st.session_state or st.session_state.cached_n != n_input:
        st.session_state.cached_n = n_input
        with st.spinner("Solving..."):
            st.session_state.bt_res = solve_backtracking(n_input, timeout=4.0)
            st.session_state.hc_res = solve_hill_climbing(n_input, timeout=8.0)

    bt_data = st.session_state.get("bt_res")
    hc_data = st.session_state.get("hc_res")

    if bt_data and hc_data:
        if bt_data["success"] and hc_data["success"] and hc_data["runtime"] > 0:
            speedup = bt_data["runtime"] / hc_data["runtime"]
            if speedup >= 1.0:
                st.markdown(
                    f"<div class='speedup-pill'>⚡ Min-Conflicts was <strong>{speedup:.1f}x faster</strong> than Backtracking for N = {n_input}</div>",
                    unsafe_allow_html=True
                )

        col_bt, col_hc = st.columns(2)

        with col_bt:
            st.markdown("### 🌲 Backtracking")
            bt_status = "SOLVED" if bt_data["success"] else "TIMED OUT"
            bt_cls = "val-success" if bt_data["success"] else "val-fail"

            st.markdown(f"""
            <div class="metric-row">
                <div class="mini-card"><div class="mini-card-title">Status</div><div class="mini-card-val {bt_cls}">{bt_status}</div></div>
                <div class="mini-card"><div class="mini-card-title">Runtime</div><div class="mini-card-val">{bt_data['runtime']*1000.0:.2f} ms</div></div>
                <div class="mini-card"><div class="mini-card-title">Nodes Explored</div><div class="mini-card-val">{bt_data['nodes_explored']:,}</div></div>
            </div>
            """, unsafe_allow_html=True)

            if bt_data["board"]:
                render_board(bt_data["board"], n_input)

        with col_hc:
            st.markdown("### 🏔️ Hill Climbing (Min-Conflicts)")
            hc_status = "SOLVED" if hc_data["success"] else "FAILED"
            hc_cls = "val-success" if hc_data["success"] else "val-fail"

            st.markdown(f"""
            <div class="metric-row">
                <div class="mini-card"><div class="mini-card-title">Status</div><div class="mini-card-val {hc_cls}">{hc_status}</div></div>
                <div class="mini-card"><div class="mini-card-title">Runtime</div><div class="mini-card-val">{hc_data['runtime']*1000.0:.2f} ms</div></div>
                <div class="mini-card"><div class="mini-card-title">Restarts</div><div class="mini-card-val">{hc_data['restarts']}</div></div>
                <div class="mini-card"><div class="mini-card-title">Steps</div><div class="mini-card-val">{hc_data['total_steps']:,}</div></div>
            </div>
            """, unsafe_allow_html=True)

            if hc_data["board"]:
                render_board(hc_data["board"], n_input)

# =============================================================================
# PAGE 2: DYNAMIC QUEEN PROTOTYPE (INTERACTIVE SIMULATOR)
# =============================================================================
with tab_prototype:
    col_proto_cfg, col_proto_hud = st.columns([1.5, 2.5])

    with col_proto_cfg:
        proto_algo = st.selectbox(
            "Algorithm:",
            ["Hill Climbing (Min-Conflicts)", "Backtracking"]
        )
        proto_n = st.slider("Board Dimension (N):", min_value=4, max_value=16, value=8, step=1, key="proto_n")
        proto_speed = st.select_slider("Playback Speed:", options=["Slow", "Normal", "Fast"], value="Normal")
        delay = 0.25 if proto_speed == "Slow" else (0.08 if proto_speed == "Normal" else 0.02)

        btn_gen = st.button("🔄 Generate Simulation", type="primary", use_container_width=True)

    # Session cache for simulation data
    sim_key = f"sim_{proto_algo}_{proto_n}"
    if btn_gen or sim_key not in st.session_state:
        with st.spinner("Generating simulation sequence..."):
            if "Hill Climbing" in proto_algo:
                res = solve_hill_climbing(proto_n, record_history=True, max_history_frames=200)
            else:
                res = solve_backtracking(proto_n, record_history=True, max_history_frames=200)
            st.session_state[sim_key] = res.get("history", [])

    history = st.session_state.get(sim_key, [])
    total_frames = len(history)

    if total_frames > 0:
        with col_proto_hud:
            st.markdown("#### 🎮 Simulation Player Controls")
            c_play, c_step, c_reset = st.columns([1.2, 2.5, 1.0])
            with c_play:
                play_anim = st.button("▶ Play Animation", use_container_width=True)
            with c_step:
                curr_step = st.slider("Step Scrubber:", 0, total_frames - 1, total_frames - 1)
            with c_reset:
                if st.button("⏮ Reset", use_container_width=True):
                    curr_step = 0

        st.markdown("---")
        board_display_col, info_col = st.columns([2, 1.2])

        target_frame = history[curr_step]
        board_state = target_frame["board"] if isinstance(target_frame, dict) else target_frame
        moved_col = target_frame.get("moved_col", -1) if isinstance(target_frame, dict) else -1
        conf_count = target_frame.get("conflicts", count_board_conflicts(board_state)) if isinstance(target_frame, dict) else count_board_conflicts(board_state)
        action_desc = target_frame.get("desc", f"Step {curr_step + 1}") if isinstance(target_frame, dict) else f"Step {curr_step + 1}"

        with info_col:
            st.markdown("##### 📡 Live Telemetry")
            conf_color = "#16A34A" if conf_count == 0 else "#DC2626"
            status_label = "GOAL REACHED (0 Conflicts)" if conf_count == 0 else f"{conf_count} Conflicts Active"

            st.markdown(f"""
            <div class="hud-box">
                <div style="font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Step Progress</div>
                <div class="hud-metric">{curr_step + 1} / {total_frames}</div>
                <div style="margin-top: 0.8rem; font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Conflict State</div>
                <div class="hud-metric" style="color: {conf_color};">{status_label}</div>
                <div style="margin-top: 0.8rem; font-size: 0.8rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Action Performed</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #1E293B;">{action_desc}</div>
            </div>
            """, unsafe_allow_html=True)

        with board_display_col:
            board_holder = st.empty()

            if play_anim:
                for idx in range(total_frames):
                    f = history[idx]
                    b = f["board"] if isinstance(f, dict) else f
                    m_col = f.get("moved_col", -1) if isinstance(f, dict) else -1
                    c = f.get("conflicts", count_board_conflicts(b)) if isinstance(f, dict) else count_board_conflicts(b)
                    with board_holder:
                        render_board(b, proto_n, active_col=m_col, title=f"Step {idx + 1}/{total_frames} (Conflicts: {c})")
                    time.sleep(delay)
            else:
                with board_holder:
                    render_board(board_state, proto_n, active_col=moved_col, title=f"Step {curr_step + 1}/{total_frames}")

# =============================================================================
# PAGE 3: PERFORMANCE BENCHMARK
# =============================================================================
with tab_benchmarks:
    c_run, c_space = st.columns([1.5, 3.5])
    with c_run:
        run_bench_btn = st.button("🔄 Run Full Benchmark (N=4 to 100)", type="primary", use_container_width=True)

    csv_path = "output/benchmark_results.csv"
    if "bench_records" not in st.session_state:
        if os.path.exists(csv_path):
            st.session_state.bench_records = pd.read_csv(csv_path).to_dict("records")
        else:
            st.session_state.bench_records = None

    if run_bench_btn:
        with st.spinner("Running automated experiments..."):
            st.session_state.bench_records = run_benchmark(
                n_values=DEFAULT_N_VALUES,
                trials=3,
                bt_timeout=3.0,
                hc_timeout=10.0,
                output_dir="output"
            )
            plot_benchmark_charts(st.session_state.bench_records, output_dir="output")

    records = st.session_state.bench_records

    if records:
        df_bench = pd.DataFrame(records)

        st.markdown("#### 📋 Performance Table")
        display_df = pd.DataFrame({
            "Board N": df_bench["n"],
            "Backtracking Success (%)": df_bench["bt_success_rate"].map(lambda x: f"{x:.1f}%"),
            "Backtracking Runtime": df_bench.apply(
                lambda r: f"{r['bt_runtime_ms']:.2f} ms" if r["bt_success_rate"] > 0 else "> 3000 ms (T/O)", axis=1
            ),
            "Hill Climbing Success (%)": df_bench["hc_success_rate"].map(lambda x: f"{x:.1f}%"),
            "Hill Climbing Runtime": df_bench["hc_runtime_ms"].map(lambda x: f"{x:.2f} ms"),
            "Hill Climbing Avg Restarts": df_bench["hc_avg_restarts"].map(lambda x: f"{x:.2f}")
        })
        st.dataframe(display_df, use_container_width=True)

        st.markdown("#### 📈 Benchmark Visualizations")
        p_col1, p_col2 = st.columns(2)

        chart_combined = "output/comparison_plots.png"
        chart_rt = "output/runtime_vs_n.png"
        chart_sr = "output/success_and_restarts_vs_n.png"

        if os.path.exists(chart_rt) and os.path.exists(chart_sr):
            with p_col1:
                st.image(chart_rt, caption="Runtime Scaling (Log Scale)", use_container_width=True)
            with p_col2:
                st.image(chart_sr, caption="Success Rate & Restarts", use_container_width=True)
        elif os.path.exists(chart_combined):
            st.image(chart_combined, use_container_width=True)

        with open("output/benchmark_results.csv", "rb") as f:
            st.download_button(
                label="📥 Download Benchmark Results (CSV)",
                data=f.read(),
                file_name="benchmark_results.csv",
                mime="text/csv"
            )
