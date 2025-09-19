import csv
import time
import tracemalloc
import psutil
import os
from src.array_approach.array_generation import main as array_generate_main

PROCESS = psutil.Process(os.getpid())

def run_array_performance_test(total_iterations, decks_per_iteration, array_batch_size, array_csv_path, array_decks_dir):
    """
    Runs a performance analysis loop for the array-based method and saves results to a CSV file.
    """
    print(f"\n--- Starting Performance Test: Array Method ---")
    
    with open(array_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ['Iteration', 'Execution Time (s)', 'CPU Usage (%)', 'Peak Memory (MB)']
        csv_writer.writerow(header)

        for i in range(1, total_iterations + 1):
            print(f"  Running Iteration {i}/{total_iterations}...")
            
            tracemalloc.start()
            start_time = time.perf_counter()
            PROCESS.cpu_percent(interval=None)

            array_generate_main(decks_per_iteration, array_batch_size, array_decks_dir)

            end_time = time.perf_counter()
            cpu_usage = PROCESS.cpu_percent(interval=None)
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            execution_time = end_time - start_time
            peak_mem_mb = peak_mem / 1024**2
            
            row = [i, f"{execution_time:.4f}", f"{cpu_usage:.2f}", f"{peak_mem_mb:.4f}"]
            csv_writer.writerow(row)
            
    print("✅ Array method performance test finished.")