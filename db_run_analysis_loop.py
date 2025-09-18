import csv
import os
import time
import tracemalloc
import psutil
from src.db_approach.db_helpers import decks_loaded
from src.db_approach.db_setup import (export_decks_and_clear_db, insert_decks,
                                      setup_database)

PROCESS = psutil.Process(os.getpid())

def main_program_logic(decks_to_generate: int):
    """
    This is an automated, non-interactive version of your main logic.
    It generates 10,000 decks and immediately exports them (for testing purposes)
    """

    setup_database()
    insert_decks(decks_to_generate)
    export_decks_and_clear_db()


if __name__ == "__main__":
    TOTAL_ITERATIONS = 10
    DECKS_PER_ITERATION = 1000000
    CSV_FILENAME = './data/comparisons/db_performance_stats.csv'

    print(f"Starting performance test: {TOTAL_ITERATIONS} iterations of {DECKS_PER_ITERATION} decks each.")
    print(f"Results will be saved to '{CSV_FILENAME}'")

    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        header = [
            'Iteration',
            'Execution Time (s)',
            'CPU Usage (%)',
            'Peak Memory (MB)',
            'Total Decks Exported'
        ]
        csv_writer.writerow(header)

        # --- Loop ---
        for i in range(1, TOTAL_ITERATIONS + 1):
            print(f"\n--- Running Iteration {i}/{TOTAL_ITERATIONS} ---")

            tracemalloc.start()
            start_time = time.perf_counter()
            PROCESS.cpu_percent(interval=None)

            main_program_logic(decks_to_generate=DECKS_PER_ITERATION)

            end_time = time.perf_counter()
            cpu_usage = PROCESS.cpu_percent(interval=None)
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            execution_time = end_time - start_time
            peak_mem_mb = peak_mem / 1024**2
            total_decks = decks_loaded()

            # --- Print and Save ---
            print(f"Iteration {i} complete in {execution_time:.2f}s | Peak Memory: {peak_mem_mb:.2f} MB")

            row = [i, f"{execution_time:.4f}", f"{cpu_usage:.2f}", f"{peak_mem_mb:.4f}", total_decks]
            csv_writer.writerow(row)

    print(f"\n✅ Performance test finished. All stats saved to '{CSV_FILENAME}'.")