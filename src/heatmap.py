import os
from typing import List, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.game_logic import all_patterns
from src.db_generation import Deck, get_next_seed
from src.db_processing import init_temp_db, process_single_batch_array_db, export_db_to_csv
from src.config import *

os.makedirs(FIGURES_DIR, exist_ok = True)

def load_scores(csv_path: str = RESULTS_CSV) -> pd.DataFrame:
    '''
    Load precomputed scoring results CSV into pandas DataFrame.
    '''
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Results CSV not found at {csv_path}. Please run scoring first.")
    df = pd.read_csv(csv_path, dtype={'p1': str, 'p2': str})
    print(f"[load_scores] Loaded {len(df)} rows from {csv_path}")
    return df

def patterns_ordered(pattern_len: int = PATTERN_LEN) -> List[str]:
    '''
    Return ordered list of binary patterns as strings in binary counting order
    '''
    return all_patterns(pattern_len)

def make_matrix(df: pd.DataFrame, metric: str = 'tricks') -> Tuple[np.ndarray, np.ndarray]:
    '''
    Build two matrices (win_pct, draw_pct) with shape (n,n)...
    Returns matrices with integer percentages [0..100].
    '''
    patterns = patterns_ordered()
    n = len(patterns)
    idx = {pat: i for i, pat in enumerate(patterns)}
    
    win_matrix = np.zeros((n, n), dtype=int)
    draw_matrix = np.zeros((n, n), dtype=int)

    if metric == 'tricks':
        p1_col = 'p1_tricks_wins'
        p2_col = 'p2_tricks_wins'
        draw_col = 'draw_tricks'
    elif metric == 'cards':
        p1_col = 'p1_cards_wins'
        p2_col = 'p2_cards_wins'
        draw_col = 'draw_cards'
    else:
        raise ValueError('metric must be either "tricks" or "cards"')

    for _, row in df.iterrows():
        p1 = row['p1']
        p2 = row['p2']
        if p1 not in idx or p2 not in idx:
            continue
        i = idx[p2]  # vertical axis = opponent choice
        j = idx[p1]  # horizontal axis = my choice

        a = float(row.get(p1_col, 0))
        b = float(row.get(p2_col, 0))
        d = float(row.get(draw_col, 0))
        total = a + b + d

        win_matrix[i, j] = int(round(100 * (a / total))) if total > 0 else 0
        draw_matrix[i, j] = int(round(100 * (d / total))) if total > 0 else 0

    return win_matrix, draw_matrix

def plot_heatmap(win_matrix: np.ndarray, draw_matrix: np.ndarray, patterns: List[str],
                 title: str, out_path: str):
    '''
    Plot a heatmap with annotations "win(draw)" in integer percents.
    '''
    n = len(patterns)
    fig, ax = plt.subplots(figsize=(max(6, n), max(6, n)))
    im = ax.imshow(win_matrix, origin='upper', vmin=0, vmax=100, cmap='Blues')

    ax.set_xticks(range(n))
    ax.set_xticklabels(patterns, rotation=45, ha='right')
    ax.set_yticks(range(n))
    ax.set_yticklabels(patterns)
    ax.set_xlabel('My Choice')
    ax.set_ylabel('Opponent Choice')
    ax.set_title(title)

    for i in range(n):
        for j in range(n):
            txt = f"{int(win_matrix[i,j])}({int(draw_matrix[i,j])})"
            color = 'black' if win_matrix[i,j] < 50 else 'white'
            ax.text(j, i, txt, ha='center', va='center', color=color, fontsize=8)

    # black rectangle around best cell in each row
    for i in range(n):
        j_best = int(np.argmax(win_matrix[i, :]))
        rect = patches.Rectangle((j_best - 0.5, i - 0.5), 1, 1, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Win Probability (%)')

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close(fig)

def generate_heatmaps(csv_path: str = RESULTS_CSV, out_dir: str = FIGURES_DIR):
    '''
    Generate both tricks and cards heatmaps from CSV scores.
    Returns paths to saved images.
    '''
    df = load_scores(csv_path)
    patterns_binary = patterns_ordered()
    patterns_rb = [p.replace('0', 'B').replace('1', 'R') for p in patterns_binary]
    sample_size = int(df['games_count'].max()) if 'games_count' in df.columns else 0

    win_tricks, draw_tricks = make_matrix(df, metric='tricks')
    win_cards, draw_cards = make_matrix(df, metric='cards')
    tricks_title = f"Win% (Draw%) by Tricks - Sample Size {sample_size}"
    cards_title = f"Win% (Draw%) by Cards - Sample Size {sample_size}"
    tricks_path = os.path.join(out_dir, f"heatmap_tricks.png")
    cards_path = os.path.join(out_dir, f"heatmap_cards.png")

    plot_heatmap(win_tricks, draw_tricks, patterns_rb, tricks_title, tricks_path)
    plot_heatmap(win_cards, draw_cards, patterns_rb, cards_title, cards_path)

    print(f"[generate_heatmaps] Saved heatmaps:\n - {tricks_path}\n - {cards_path}")
    return tricks_path, cards_path

def heatmap_augment_data(n: int):
    '''
    create n new decks 
    automatically update all scores and figures 
    '''
    seed = get_next_seed()
    np.random.seed(seed)
    decks = np.zeros((n, DECK_LEN), dtype = int)

    for i in range(n):
        deck = Deck()
        decks[i] = [1 if c == 'R' else 0 for c in deck.cards]

    batch_path = os.path.join(DATA_SCORED_FOLDER, f'decks_{n}_seed{seed}.npy')
    np.save(batch_path, decks)

    conn = init_temp_db(DB_PATH, pattern_len = PATTERN_LEN, seed_csv_path = RESULTS_CSV)
    process_single_batch_array_db(decks, conn, pattern_len = PATTERN_LEN)
    export_db_to_csv(conn, RESULTS_CSV)
    conn.close()
    generate_heatmaps(RESULTS_CSV)