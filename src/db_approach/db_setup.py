import sqlite3
import numpy as np
import random
from typing import List
import os
from db_generation import Deck, get_next_seed
from db_helpers import debugger, string_to_binary
import time
import psutil
import sys

DB_PATH = "decks.db"

def setup_database():
    """Creates the database and the 'decks' table if they don't exist."""
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
    print("Database setup complete.")

def check_length():
    """Checks if there are unloaded decks still present"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        total_decks = cursor.execute("SELECT COUNT(*) FROM decks").fetchone()[0]
    return total_decks

def insert_decks(num_to_add: int):
    """
    Generates and inserts new decks into the database, incrementing the
    random seed for each batch of 10,000 decks.
    """
    print(f"[START] Generating {num_to_add} decks in {num_to_add // 10000} batches ...")
    start_seed = get_next_seed()
    current_seed = start_seed
    decks_generated = 0
    batch_size = 10000
    
    start_time = time.time()
    total_saved = 0
    memory_used = 0
    n_files = 0

    size_mb = memory_used / (1024**2)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        while decks_generated < num_to_add:
            num_this_batch = min(batch_size, num_to_add - decks_generated)
            if num_this_batch <= 0:
                break
            print(f"  -> Generating batch of {num_this_batch} decks with seed {current_seed}...")
            random.seed(current_seed)
            decks_to_insert = [(Deck().get_sequence_string(),) for _ in range(num_this_batch)]
            cursor.executemany("INSERT INTO decks (sequence) VALUES (?)", decks_to_insert)
            conn.commit()
            decks_generated += num_this_batch
            current_seed += 1

            total_saved += len(decks_to_insert)
            memory_used += sys.getsizeof(decks_to_insert)
            n_files += 1
    
    elapsed = time.time() - start_time
    process = psutil.Process(os.getpid())
    rss_mb = process.memory_info().rss / (1024 ** 2)
    size_mb = memory_used / (1024**2)

    print("\n[SUMMARY]")
    print(f" Total decks generated: {total_saved}")
    print(f" Number of files: {n_files}")
    print(f" Total storage size: {size_mb:.2f} MB")
    print(f" Runtime: {elapsed:.2f} seconds")
    print(f" Peak memory usage: {rss_mb:.2f} MB")
    print(f"Successfully generated {decks_generated} decks.\n")

def export_decks_and_clear_db(batch_size: int = 10000):
    """
    Exports decks from the database, clears the table, and then deletes the .db file
    to ensure the file size is reset.
    """
    print(f"Exporting decks to .npy files with a batch size of {batch_size}...")
    seed = get_next_seed()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        total_decks = check_length()
        if total_decks == 0:
            print("No decks in the database to export.")
            return
        offset = 0
        while offset < total_decks:
            query = "SELECT sequence FROM decks ORDER BY id LIMIT ? OFFSET ?"
            results = cursor.execute(query, (batch_size, offset)).fetchall()
            if not results:
                break
            decks_as_lists = [string_to_binary(row[0]) for row in results]
            numpy_array = np.array(decks_as_lists, dtype=np.int8)
            end_num = len(results)
            filename = f"./data/db_decks/decks_{end_num}_seed{seed}.npy"
            print(f"  -> Writing array with shape {numpy_array.shape} to '{filename}'...")
            np.save(filename, numpy_array)
            offset += batch_size
            seed += 1
        
        # The 'DELETE' command empties the table.
        print("\nExport successful. Clearing decks table...")
        cursor.execute("DELETE FROM decks")
        conn.commit()
        
    print("Workflow complete.")

    # --- NEW STEP: Delete the database file itself ---
    try:
        os.remove(DB_PATH)
        print(f"Database file '{DB_PATH}' successfully deleted to manage size.")
    except OSError as e:
        print(f"Error deleting file {DB_PATH}: {e}")