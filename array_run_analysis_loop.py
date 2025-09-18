import csv
import os
import time
import tracemalloc
import psutil
from src.array_approach.array_generation import main as generate_main


PROCESS = psutil.Process(os.getpid())


def decks_exported(output_dir) -> int:
    """
    Helper to count .npy files.
    """
    if not os.path.exists(output_dir):
        return 0
    return len([f for f in os.listdir(output_dir) if f.endswith(".npy")])

def automated_main_logic(total_decks, batch_size, output_dir):
    """
    Non-interactive version of the main logic that
    only asks for number of decks generated
    """

    generate_main(total_decks, batch_size, output_dir)


if __name__ == "__main__":
    TOTAL_ITERATIONS = 10
    DECKS_PER_ITERATION = 1000000
    BATCH_SIZE = 10000
    OUTPUT_DIR = "./data/array_decks"
    CSV_FILENAME = './data/comparisons/array_performance_stats.csv'

    print(f"Starting performance test: {TOTAL_ITERATIONS} iterations, generating {DECKS_PER_ITERATION} decks each.")
    print(f"Results will be saved to '{CSV_FILENAME}'")


    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
    
        header = [
            'Iteration',
            'Execution Time (s)',
            'CPU Usage (%)',
            'Peak Memory (MB)',
            'Total Deck Files'
        ]
        csv_writer.writerow(header)

        # --- Loop ---
        for i in range(1, TOTAL_ITERATIONS + 1):
            print(f"\n--- Running Iteration {i}/{TOTAL_ITERATIONS} ---")

            tracemalloc.start()
            start_time = time.perf_counter()
            PROCESS.cpu_percent(interval=None)

            automated_main_logic(DECKS_PER_ITERATION, BATCH_SIZE, OUTPUT_DIR)

            end_time = time.perf_counter()
            cpu_usage = PROCESS.cpu_percent(interval=None)
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            execution_time = end_time - start_time
            peak_mem_mb = peak_mem / 1024**2
            total_files = decks_exported(OUTPUT_DIR)

            # --- Print and Save ---
            print(f"Iteration {i} complete in {execution_time:.2f}s | Peak Memory: {peak_mem_mb:.2f} MB")

            row = [i, f"{execution_time:.4f}", f"{cpu_usage:.2f}", f"{peak_mem_mb:.4f}", total_files]
            csv_writer.writerow(row)

    print(f"\n✅ Performance test finished. All stats saved to '{CSV_FILENAME}'.")