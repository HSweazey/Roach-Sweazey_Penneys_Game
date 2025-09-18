import argparse
import os
from src.array_approach.array_generation import main as array_generate_main
from src.db_approach.db_helpers import decks_loaded as db_decks_exported
from src.db_approach.db_setup import (check_length, export_decks_and_clear_db,
                                      insert_decks, setup_database)
from src.array_approach.array_helpers import array_decks_loaded


# --- Helper Functions ---

def run_array_generation(num_to_generate) -> bool:
    """
    Handles the execution for the array approach.
    """
    try:
        batch = 10000
        output_dir_array = "./data/array_decks"

        print("\n>>> Running Array Generation...")
        array_generate_main(num_to_generate, batch, output_dir_array)
        print(">>> Array generation complete.")
        return True
    except ValueError:
        print("\nAn unexpected error occurred during array generation.")
        return False

def run_db_generation(num_to_generate) -> bool:
    """
    Handles the execution for the database approach.
    """
    print("\n>>> Running Database Generation...")
    insert_decks(num_to_generate)
    print(f">>> {num_to_generate} decks inserted into the database.")

    print(">>> Exporting newly added decks...")
    export_decks_and_clear_db()
    print(">>> Database export complete.")
    return True


# --- Main ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate decks using the database (default) or array strategy."
    )
    parser.add_argument(
        '--array',
        action='store_true',
        help='Use the array generation strategy instead of the default.'
    )
    args = parser.parse_args()

    # --- Setup/Status ---
    if args.array:
        print("--- Current Status (Array-Only Mode) ---")
        print(f'Array Approach: {array_decks_loaded()} deck(s) exported.')
        print("Database setup will be skipped.")
    else:
        print("Setting up database...")
        setup_database()
        print("-" * 30)

        print("--- Current Status ---")
        print(f'Array Approach: {array_decks_loaded()} deck(s) exported.')
        print(f'DB Approach:    {db_decks_exported()} deck(s) exported.')

        db_pending_count = check_length()
        if db_pending_count > 0:
            print(f'DB Approach:    {db_pending_count} deck(s) in the database pending export. Exporting now...')
            export_decks_and_clear_db()
            print(f'Export complete. There are now {db_decks_exported()} total DB decks exported.')
    print("-" * 30)

    # --- Get User Input for Deck Count ---
    num_to_generate = 0
    try:
        num_to_generate_str = input('How many decks to generate? ')
        num_to_generate = int(num_to_generate_str)
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
        exit()

    # --- Execute Strategy Based on Command-Line Flag ---
    if args.array:
        run_array_generation(num_to_generate)
    else:
        run_db_generation(num_to_generate)

    # --- Final Status Report ---
    print("\n" + "-" * 30)
    print("--- Final Status ---")
    print(f'There are now {array_decks_loaded()} total array deck(s) exported.')
    # Only report on the DB status if that strategy was used
    if not args.array:
        print(f'There are now {db_decks_exported()} total DB deck(s) exported.')
    print("Process complete.")