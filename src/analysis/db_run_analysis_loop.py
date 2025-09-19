import os
import csv
import time
import tracemalloc
import psutil
from src.db_approach.db_setup import setup_database, insert_decks, export_decks_and_clear_db

PROCESS = psutil.Process(os.getpid())

def run_db_performance_test(total_iterations, decks_per_iteration, db_csv_path):
    """
    Runs a performance analysis loop for the database method and saves results to a CSV file.
    """
    print(f"\n--- Starting Performance Test: Database Method ---")
    
    with open(db_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ['Iteration', 'Execution Time (s)', 'CPU Usage (%)', 'Peak Memory (MB)']
        csv_writer.writerow(header)

        for i in range(1, total_iterations + 1):
            print(f"  Running Iteration {i}/{total_iterations}...")
            
            setup_database() 
            
            tracemalloc.start()
            start_time = time.perf_counter()
            PROCESS.cpu_percent(interval=None)

            insert_decks(decks_per_iteration)
            export_decks_and_clear_db()

            end_time = time.perf_counter()
            cpu_usage = PROCESS.cpu_percent(interval=None)
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            execution_time = end_time - start_time
            peak_mem_mb = peak_mem / 1024**2
            
            row = [i, f"{execution_time:.4f}", f"{cpu_usage:.2f}", f"{peak_mem_mb:.4f}"]
            csv_writer.writerow(row)
            
    print("✅ Database method performance test finished.")