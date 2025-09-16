import time
import os
import tracemalloc
import psutil

# Get the current process to track its resource usage.
# This should be done once at the beginning.
PROCESS = psutil.Process(os.getpid())

def main_program_logic():
    """
    ==================================================================
    PASTE THE ENTIRE LOGIC FROM YOUR `main.py` SCRIPT HERE.
    This function will be timed and profiled.
    ==================================================================
    """
    # Example placeholder for your code:
    from db_approach.db_helpers import decks_loaded
    from db_approach.db_setup import setup_database, check_length, export_decks_and_clear_db, insert_decks

    # Setup the database if it doesn't exist
    setup_database()

    # --- Main Program Logic ---
    print(f'There are currently {decks_loaded()} deck(s) exported.')
    print(f'There are currently {check_length()} deck(s) in the database waiting to be exported.')

    if check_length() > 0:
        load_choice = input('Export remaining decks from the database? (Y/N) ')
        if load_choice.upper() == 'Y':
            export_decks_and_clear_db()
            print(f'\nExport complete. There are now {decks_loaded()} total decks exported.')

    gen_choice = input('Generate new decks? (Y/N) ')
    if gen_choice.upper() == 'Y':
        try:
            num_decks_str = input('How many decks to add? ')
            num_decks = int(num_decks_str)
            insert_decks(num_decks)
            
            export_new_choice = input('Export newly added decks now? (Y/N) ')
            if export_new_choice.upper() == 'Y':
                export_decks_and_clear_db()
            
            print(f'\nProcess complete. There are now {decks_loaded()} total decks exported.')

        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print("\n--- Main program has finished. ---")


if __name__ == "__main__":
    # --- 1. Start Tracking ---
    tracemalloc.start()  # Start tracking memory allocations
    start_time = time.perf_counter()  # Get a high-precision start time
    
    # Initialize CPU usage calculation
    PROCESS.cpu_percent(interval=None)

    # --- 2. Run the Main Program ---
    main_program_logic()

    # --- 3. Stop Tracking and Collect Stats ---
    end_time = time.perf_counter() # Get the end time
    cpu_usage = PROCESS.cpu_percent(interval=None) # Get CPU % used by this process
    current_mem, peak_mem = tracemalloc.get_traced_memory() # Get memory usage
    tracemalloc.stop() # Stop tracking memory

    # --- 4. Calculate and Display Results ---
    execution_time = end_time - start_time
    
    print("\n" + "="*40)
    print("      PERFORMANCE & EFFICIENCY STATS")
    print("="*40)
    print(f"Total Execution Time: {execution_time:.4f} seconds")
    print(f"Average CPU Usage:    {cpu_usage:.2f}%")
    print(f"Peak Memory Usage:      {peak_mem / 1024**2:.4f} MB")
    print(f"Current Memory Usage:   {current_mem / 1024**2:.4f} MB")
    print("="*40)

    # --- 5. Interpretation and Strategy ---
    print("\nInterpretation:")
    print("- Execution Time: Measures the overall speed of the program.")
    print("- CPU Usage: Indicates how much processing power was required.")
    print("- Peak Memory Usage: The most critical memory stat. It shows the maximum RAM")
    print("  your program needed at any single point. This is key for determining")
    print("  if the program can run on systems with limited memory.")