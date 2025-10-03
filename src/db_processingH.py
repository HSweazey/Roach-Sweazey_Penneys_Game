import os
import numpy as np
import pandas as pd
import sqlite3
# Import shared logic from the new file
from .game_logic import all_patterns, str_to_bits, play_through_deck

def init_temp_db(db_path: str, pattern_len: int, seed_csv_path: str) -> sqlite3.Connection:
    """
    Initializes the temporary database.
    """

    conn = sqlite3.connect(db_path)
    if os.path.exists(seed_csv_path):
        pd.read_csv(seed_csv_path, dtype={'p1': str, 'p2': str}).to_sql('scores', conn, if_exists='replace', index=False)
    else:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE scores (p1 TEXT, p2 TEXT, p1_cards INTEGER, p1_tricks INTEGER, p2_cards INTEGER, p2_tricks INTEGER, draw_cards INTEGER, draw_tricks INTEGER, games_count INTEGER, PRIMARY KEY (p1, p2))")
        patterns = all_patterns(pattern_len)
        rows = [(p1, p2, 0, 0, 0, 0, 0, 0, 0) for p1 in patterns for p2 in patterns if p1 != p2]
        cursor.executemany("INSERT INTO scores VALUES (?,?,?,?,?,?,?,?,?)", rows)
        conn.commit()
    return conn

def update_aggregate_db(db_conn, p1: str, p2: str, p1_c: int, p1_t: int, p2_c: int, p2_t: int, d_c: int, d_t: int):
    """
    Updates the database.
    """

    query = "UPDATE scores SET p1_cards=p1_cards+?, p1_tricks=p1_tricks+?, p2_cards=p2_cards+?, p2_tricks=p2_tricks+?, draw_cards=draw_cards+?, draw_tricks=draw_tricks+?, games_count=games_count+1 WHERE p1=? AND p2=?"
    db_conn.cursor().execute(query, (p1_c, p1_t, p2_c, p2_t, d_c, d_t, p1, p2))

def export_db_to_csv(db_conn, out_csv_path: str):
    """
    Exports to CSV file.
    """

    pd.read_sql_query("SELECT * FROM scores ORDER BY p1, p2", db_conn).to_csv(out_csv_path, index=False)

def process_single_batch_array_db(batch_array: np.ndarray, db_conn: sqlite3.Connection, pattern_len: int):
    """
    Processes a numpy array of decks, updating database.
    """
    
    patterns = all_patterns(pattern_len)
    pattern_bits = {p: str_to_bits(p) for p in patterns}
    for row in batch_array:
        deck_list = list(map(int, row))
        for p1 in patterns:
            for p2 in patterns:
                if p1 == p2: continue
                p1_c, p1_t, p2_c, p2_t, d_c, d_t = play_through_deck(deck_list, pattern_bits[p1], pattern_bits[p2])
                update_aggregate_db(db_conn, p1, p2, p1_c, p1_t, p2_c, p2_t, d_c, d_t)