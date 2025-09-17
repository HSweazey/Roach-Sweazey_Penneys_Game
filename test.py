import os

# --- Array approach imports ---
from src.array_approach.array_generation import main as array_generate_main

# --- Database approach imports ---
from src.db_approach.db_setup import setup_database, check_length, export_decks_and_clear_db, insert_decks
from src.db_approach.db_helpers import decks_loaded as db_decks_exported

# --- Helper Functions ---

def array_decks_exported(output_dir="./data/array_decks"):
    """Counts how many .npy deck files exist in the array export folder."""
    if not os.path.exists(output_dir):
        return 0
    return (10000*len([f for f in os.listdir(output_dir) if f.endswith(".npy")]))

def run_array_generation(num_to_generate):
    """Handles the user prompts and execution for the array generation strategy."""
    try:
        batch = 10000

        output_dir_array = "./data/array_decks"

        print("\n>>> Running Array Generation...")
        array_generate_main(num_to_generate, batch, output_dir_array)
        print(">>> Array generation complete.")
        return True
    except ValueError:
        print("\nInvalid input for batch size. Please enter a number.")
        return False

def run_db_generation(num_to_generate):
    """Handles the user prompts and execution for the database generation strategy."""
    print("\n>>> Running Database Generation...")
    insert_decks(num_to_generate)
    print(f">>> {num_to_generate} decks inserted into the database.")

    # Ask to export the newly created decks from the database
    export_new_choice = input('Export newly added decks from the database now? (Y/N) ')
    if export_new_choice.upper() == 'Y':
        export_decks_and_clear_db()
        print(">>> Database export complete.")
    return True

# --- Main Program Logic ---

if __name__ == "__main__":
    # Initial setup for the database
    print("Setting up database...")
    setup_database()
    print("-" * 30)

    # --- Initial Status Report ---
    print("--- Current Status ---")
    print(f'Array Approach: {array_decks_exported()} deck file(s) exported.')
    print(f'DB Approach:    {db_decks_exported()} deck file(s) exported.')
    
    db_pending_count = check_length()
    if db_pending_count > 0:
        print(f'DB Approach:    {db_pending_count} deck(s) in the database to be exported.')
        export_decks_and_clear_db()
        print(f'Export complete. There are now {db_decks_exported()} total DB decks exported.')
    print("-" * 30)

    # --- Strategy Selection ---
    print("Which deck generation strategy would you like to use?")
    print("  1: Array Strategy Only")
    print("  2: Database Strategy Only")
    print("  3: Both Strategies")
    
    choice = input("Enter your choice (1, 2, or 3): ")
    print("-" * 30)

    num_to_generate = 0
    should_run = False
    
    if choice in ['1', '2', '3']:
        try:
            num_to_generate_str = input('How many decks to generate? ')
            num_to_generate = int(num_to_generate_str)
            should_run = True
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

    if should_run:
        if choice == '1':
            # Run Array Strategy Only
            run_array_generation(num_to_generate)
        
        elif choice == '2':
            # Run Database Strategy Only
            run_db_generation(num_to_generate)

        elif choice == '3':
            # Run Both Strategies
            if run_array_generation(num_to_generate):
                run_db_generation(num_to_generate)

    elif choice:
        print("Invalid choice. Please run the script again and select 1, 2, or 3.")


    # --- Final Status Report ---
    print("\n" + "-" * 30)
    print("--- Final Status ---")
    print(f'There are now {array_decks_exported()} total array deck(s) exported.')
    print(f'There are now {db_decks_exported()} total DB deck(s) exported.')
    print("Process complete.")