import os
import numpy as np
import pandas as pd
from itertools import product
from .game_logic import all_patterns, str_to_bits, play_through_deck

def init_aggregate_df(pattern_len: int, out_path: str) -> pd.DataFrame:

    '''
    Initializes or loads the aggregate DataFrame that stores cumulative results 
    for all valid pattern pairs 

    If an existing csv is found at out_path, it is loaded and any missing pairs 
    are added. Otherwise a new dataframe is created 

    Args: 
        pattern_len (int): Length of the patterns being tested
        out_path (str): Path to the csv file for loading/saving aggregate results

    Returns: 
        pd.DataFrame: dataframe containing statistics for each pattern pair 


    '''

    cols = ['p1', 'p2', 
            'p1_cards', 'p1_tricks', 
            'p2_cards', 'p2_tricks', 
            'draw_cards', 'draw_tricks', 
            'games_count'
            ]
    # generate all valid pattern pairs 
    patterns = all_patterns(pattern_len)
    ordered_pairs = [(p1, p2) for p1 in patterns for p2 in patterns if p1 != p2]
    if os.path.exists(out_path):
        print(f"[INFO] Loading existing aggregate file: {out_path}")
        df = pd.read_csv(out_path, dtype={'p1': str, 'p2': str})
        existing_keys = set(zip(df['p1'].astype(str), df['p2'].astype(str)))

        # add any missing pairs (p1, p2) not yet in the dataframe
        rows_to_add = [{'p1': p1, 'p2': p2, 
                        'p1_cards': 0, 'p1_tricks': 0, 
                        'p2_cards': 0, 'p2_tricks': 0, 
                        'draw_cards': 0, 'draw_tricks': 0, 
                        'games_count': 0} 
                        for p1, p2 in ordered_pairs if (p1, p2) not in existing_keys
                        ]
        
        if rows_to_add:
            df = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)
        return df.sort_values(['p1', 'p2']).reset_index(drop=True)[cols]
    else:
        print(f"[INFO] Creating new aggregate DataFrame in memory.")
        rows = [{'p1': p1, 'p2': p2, 'p1_cards': 0, 'p1_tricks': 0, 'p2_cards': 0, 'p2_tricks': 0, 'draw_cards': 0, 'draw_tricks': 0, 'games_count': 0} for p1, p2 in ordered_pairs]
        return pd.DataFrame(rows, columns=cols)

def update_aggregate_df(df: pd.DataFrame, p1: str, p2: str, p1_c: int, p1_t: int, p2_c: int, p2_t: int, d_c: int, d_t: int):
    
    '''
    Update the in-memory DataFrame with results from one game

    Args: 
        df (pd.DataFrame): DataFrame to update
        p1 (str): pattern for player 1
        p2 (str): pattern for player 2
        p1_c (int): cards won by player 1
        p1_t (int): tricks won by player 1
        p2_c (int): cards won by player 2
        p2_t (int): tricks won by player 2
        d_c (int): cards resulting in a draw
        d_t (int): tricks resulting in a draw
    '''

    # locate the row corresponding to (p1, p2)
    mask = (df['p1'] == p1) & (df['p2'] == p2)
    i = df.index[mask][0]
    df.at[i, 'p1_cards'] += p1_c; df.at[i, 'p1_tricks'] += p1_t
    df.at[i, 'p2_cards'] += p2_c; df.at[i, 'p2_tricks'] += p2_t
    df.at[i, 'draw_cards'] += d_c; df.at[i, 'draw_tricks'] += d_t
    df.at[i, 'games_count'] += 1

def process_single_batch_array(batch_array: np.ndarray, agg_df: pd.DataFrame, pattern_len: int):
    
    '''
    Processes a numpy array of decks, updating the in-memory DataFrame
    For each deck, simulate every valid pattern pair and update the dataframe 

    Args: 
        batch_array (np.ndarray): array of decks where each row is one deck
        agg_df (pd.DataFrame): dataframe to update with results
        pattern_len (int): length of the patterns being tested
    '''

    # precompute representations for all patterns bitewise 
    patterns = all_patterns(pattern_len)
    pattern_bits = {p: str_to_bits(p) for p in patterns}
    for row in batch_array:
        deck_list = list(map(int, row)) # convert row to lists of ints
        
        # loop through all valid pattern pairs 
        for p1 in patterns:
            for p2 in patterns:
                if p1 == p2: continue
                p1_c, p1_t, p2_c, p2_t, d_c, d_t = play_through_deck(deck_list, pattern_bits[p1], pattern_bits[p2])
                update_aggregate_df(agg_df, p1, p2, p1_c, p1_t, p2_c, p2_t, d_c, d_t)