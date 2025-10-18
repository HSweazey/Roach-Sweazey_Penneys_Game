import os
import random
import sqlite3
import sys
import time
from typing import List
import numpy as np
import psutil

# --- My Imports ---
from src.db_generation import Deck, get_next_seed
from src.db_helpers import debugger, string_to_binary
from src.config import DB_PATH, BATCH_SIZE, DATA_UNSCORED_FOLDER


def setup_database() -> None:
    """
    Creates the database and the 'decks' table if they don't exist.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY,
                sequence TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    #print("Database setup complete.")

def check_length() -> int:
    """
    Returns number of decks in db
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        total_decks = cursor.execute("SELECT COUNT(*) FROM decks").fetchone()[0]
    return total_decks

def insert_decks(num_to_add: int) -> None:
    """
    Generates and inserts new decks, incrementing
    random seed for each batch of 10,000 decks.
    """
    print(f"[START] Generating {num_to_add} decks in {num_to_add // BATCH_SIZE} batches ...")
    start_seed = get_next_seed()
    current_seed = start_seed
    decks_generated = 0
    
    start_time = time.time()
    total_saved = 0
    n_files = 0

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        while decks_generated < num_to_add:
            num_this_batch = min(BATCH_SIZE, num_to_add - decks_generated)
            if num_this_batch <= 0:
                break
            #print(f"  -> Generating batch of {num_this_batch} decks with seed {current_seed}...")
            
            random.seed(current_seed)
            decks_to_insert = [(Deck().get_sequence_string(),) for _ in range(num_this_batch)]
            cursor.executemany("INSERT INTO decks (sequence) VALUES (?)", decks_to_insert)
            conn.commit()

            decks_generated += num_this_batch
            current_seed += 1

            total_saved += len(decks_to_insert)
            n_files += 1
    
    elapsed = time.time() - start_time
    process = psutil.Process(os.getpid())
    rss_mb = process.memory_info().rss / (1024 ** 2)

    print("\n[SUMMARY]")
    print(f" Total decks generated: {total_saved}")
    print(f" Number of files: {n_files}")
    print(f" Runtime: {elapsed:.2f} seconds")
    print(f" Peak memory usage (RSS): {rss_mb:.2f} MB")
    print(f"Successfully generated {decks_generated} decks.\n")

def export_decks_and_clear_db(batch_size: int = BATCH_SIZE) -> None:
    """
    Exports decks from the database, clears the table, and then deletes the .db file
    to ensure the file size is reset.
    """
    #print(f"Exporting decks to .npy files with a batch size of {batch_size}...")
    
    seed = get_next_seed()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        total_decks = check_length()
        if total_decks == 0:
            print("No decks in the database to export.")
            return
        
        offset = 0
        cumulative_count = 0

        while offset < total_decks:
            query = "SELECT sequence FROM decks ORDER BY id LIMIT ? OFFSET ?"
            results = cursor.execute(query, (batch_size, offset)).fetchall()
            if not results:
                break

            # extract decks and seed values 
            decks_as_lists = [string_to_binary(row[0]) for row in results]
            numpy_array = np.array(decks_as_lists, dtype=np.int8)

            cumulative_count += len(results)
            filename = os.path.join(DATA_UNSCORED_FOLDER, f"decks_{batch_size}_seed{seed}.npy")
            np.save(filename, numpy_array)
 
            offset += batch_size
            seed += 1
        
        # empties table
        #print("\nExport successful. Clearing decks table...")
        cursor.execute("DELETE FROM decks")
        conn.commit()
        
    #print("Workflow complete.")

    # delete db to preserve size
    try:
        os.remove(DB_PATH)
        #print(f"Database file '{DB_PATH}' successfully deleted to manage size.\n")
    except OSError as e:
        print(f"Error deleting file {DB_PATH}: {e}")