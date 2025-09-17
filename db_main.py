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
        
        # Ask to export the newly created decks
        export_new_choice = input('Export newly added decks now? (Y/N) ')
        if export_new_choice.upper() == 'Y':
            export_decks_and_clear_db()
        
        print(f'\nProcess complete. There are now {decks_loaded()} total decks exported.')

    except ValueError:
        print("Invalid input. Please enter a number.")