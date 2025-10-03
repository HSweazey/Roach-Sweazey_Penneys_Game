# test_utils.py
import os
import time
import psutil
import tracemalloc
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime

# Import from the approach files
from .db_processingR import init_aggregate_df as init_df_R, process_single_batch_array as process_R
from .db_processingH import init_temp_db, process_single_batch_array_db as process_H, export_db_to_csv

def update_markdown_summary(md_path: str, perf_df: pd.DataFrame, df_r: pd.DataFrame, df_h: pd.DataFrame):
    """Updates a Markdown file by replacing only the last test run summary."""
    print(f"Updating test summary in: {md_path}")
    df_r_md, df_h_md = df_r.copy(), df_h.copy()
    for col in ['p1', 'p2']:
        df_r_md[col] = df_r_md[col].str.replace('0', 'B').str.replace('1', 'R')
        df_h_md[col] = df_h_md[col].str.replace('0', 'B').str.replace('1', 'R')
    try:
        with open(md_path, 'r', encoding='utf-8') as f: existing_content = f.read()
    except FileNotFoundError: existing_content = ""
    marker = "\n\n---\n\n# Test Run Summary:"
    last_summary_pos = existing_content.rfind(marker)
    base_content = existing_content[:last_summary_pos] if last_summary_pos != -1 else existing_content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_summary_parts = [
        f"\n\n---\n\n# Test Run Summary: {timestamp}\n", "## 📊 Performance Comparison\n",
        perf_df.to_markdown(index=False), "\n\n## Scores: Approach 1 (pandas_in_memory)\n",
        df_r_md.to_markdown(index=False), "\n\n## Scores: Approach 2 (sqlite_temp_db)\n",
        "*Note: The numerical results here should be identical to Approach 1.*\n",
        df_h_md.to_markdown(index=False), "\n"
    ]
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(base_content + "".join(new_summary_parts))

def run_and_profile(approach_name: str, decks: np.ndarray, pattern_len: int, output_dir: str) -> dict:
    """Runs and profiles a given processing approach."""
    print(f"\n--- Running Test for: {approach_name} ---")
    if approach_name == 'Approach 1 (pandas_in_memory)':
        output_csv = os.path.join(output_dir, 'approach1_scores.csv')
        # <<< CHANGE >>> The line that deleted the old CSV has been removed.
        # if os.path.exists(output_csv): os.remove(output_csv)
        agg_df = init_df_R(pattern_len, output_csv)
    elif approach_name == 'Approach 2 (sqlite_temp_db)':
        output_csv = os.path.join(output_dir, 'approach2_scores.csv')
        temp_db_path = os.path.join(output_dir, 'temp_agg.db')
        if os.path.exists(temp_db_path): os.remove(temp_db_path)
        # <<< CHANGE >>> The line that deleted the old CSV has been removed.
        # if os.path.exists(output_csv): os.remove(output_csv)
        db_conn = init_temp_db(temp_db_path, pattern_len, seed_csv_path=output_csv)

    process = psutil.Process(os.getpid())
    tracemalloc.start()
    start_time = time.perf_counter()
    cpu_time_start = process.cpu_times()
    print("Processing decks...")
    if approach_name == 'Approach 1 (pandas_in_memory)': process_R(decks, agg_df, pattern_len)
    elif approach_name == 'Approach 2 (sqlite_temp_db)': process_H(decks, db_conn, pattern_len); db_conn.commit()
    cpu_time_end = process.cpu_times()
    end_time = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("Processing complete.")
    if approach_name == 'Approach 1 (pandas_in_memory)': agg_df.to_csv(output_csv, index=False)
    elif approach_name == 'Approach 2 (sqlite_temp_db)': export_db_to_csv(db_conn, output_csv); db_conn.close(); os.remove(temp_db_path)
    print(f"Results saved to {output_csv}")
    return {
        'approach': approach_name, 'wall_time_seconds': end_time - start_time,
        'cpu_time_seconds': (cpu_time_end.user + cpu_time_end.system) - (cpu_time_start.user + cpu_time_start.system),
        'peak_memory_mb': peak_mem / 1024 / 1024, 'num_decks_processed': len(decks)
    }