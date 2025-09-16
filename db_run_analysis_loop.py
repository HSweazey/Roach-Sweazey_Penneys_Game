import time
import os
import tracemalloc
import psutil
import csv

# Get the current process to track its resource usage.
PROCESS = psutil.Process(os.getpid())

def main_program_logic(decks_to_generate: int):
    """
    This is an automated, non-interactive version of your main logic.
    It generates a specified number of decks and immediately exports them.
    """
    # Import necessary functions from your project files
    from db_approach.db_helpers import decks_loaded
    from db_approach.db_setup import setup_database, check_length, export_decks_and_clear_db, insert_decks

    # Setup the database if it doesn't exist
    setup_database()

    # --- Automated Main Logic ---
    # 1. Generate a fixed number of decks
    insert_decks(decks_to_generate)
    
    # 2. Export the newly created decks and clear/delete the database
    export_decks_and_clear_db()
    

if __name__ == "__main__":
    # --- Configuration ---
    TOTAL_ITERATIONS = 10
    DECKS_PER_ITERATION = 2000000  # Number of decks to generate in each loop
    CSV_FILENAME = 'sw_ON_r_performance_stats.csv'

    print(f"Starting performance test: {TOTAL_ITERATIONS} iterations of {DECKS_PER_ITERATION} decks each.")
    print(f"Results will be saved to '{CSV_FILENAME}'")

    # --- Setup CSV Logging ---
    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row
        header = [
            'Iteration', 
            'Execution Time (s)', 
            'CPU Usage (%)', 
            'Peak Memory (MB)', 
            'Total Decks Exported'
        ]
        csv_writer.writerow(header)

        # --- Main Loop for Performance Tracking ---
        for i in range(1, TOTAL_ITERATIONS + 1):
            print(f"\n--- Running Iteration {i}/{TOTAL_ITERATIONS} ---")

            # --- 1. Start Tracking ---
            tracemalloc.start()
            start_time = time.perf_counter()
            PROCESS.cpu_percent(interval=None) # Initialize CPU measurement

            # --- 2. Run the Main Program Logic ---
            main_program_logic(decks_to_generate=DECKS_PER_ITERATION)

            # --- 3. Stop Tracking and Collect Stats ---
            end_time = time.perf_counter()
            cpu_usage = PROCESS.cpu_percent(interval=None)
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # --- 4. Calculate and Format Results ---
            execution_time = end_time - start_time
            peak_mem_mb = peak_mem / 1024**2
            
            # Get the cumulative total of decks from the helper function
            from db_approach.db_helpers import decks_loaded
            total_decks = decks_loaded()

            # --- 5. Print to Console and Save to CSV ---
            print(f"Iteration {i} complete in {execution_time:.2f}s | Peak Memory: {peak_mem_mb:.2f} MB")
            
            # Write the results for the current iteration to the CSV file
            row = [i, f"{execution_time:.4f}", f"{cpu_usage:.2f}", f"{peak_mem_mb:.4f}", total_decks]
            csv_writer.writerow(row)
            
    print(f"\n✅ Performance test finished. All stats saved to '{CSV_FILENAME}'.")