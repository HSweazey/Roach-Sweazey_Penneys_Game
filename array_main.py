# roach_main.py
from roach_generation import main as generate_main
import os

# --- Helper ---
def decks_exported(output_dir="./data/decks"):
    """Count how many decks files exist in the export folder."""
    if not os.path.exists(output_dir):
        return 0
    return len([f for f in os.listdir(output_dir) if f.endswith(".npy")])

# --- Main Program Logic ---
print(f'There are currently {decks_exported()} exported deck file(s).')

gen_choice = input('Generate new decks? (Y/N) ')
if gen_choice.upper() == 'Y':
    try:
        total_str = input('How many total decks to generate? ')
        total = int(total_str)

        batch_str = input('Batch size (default 10000)? ')
        batch = int(batch_str) if batch_str.strip() else 10000

        output_dir = input('Output directory (default ./data/decks)? ')
        output_dir = output_dir.strip() or "./data/decks"

        # Run the generator
        generate_main(total, batch, output_dir)

        print(f'\nProcess complete. There are now {decks_exported(output_dir)} total deck file(s) exported.')

    except ValueError:
        print("Invalid input. Please enter numbers for total decks and batch size.")

# testing testing 