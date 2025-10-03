import os
import numpy as np
import pandas as pd
from src.test_helpers import run_and_profile, update_markdown_summary

# ==============================================================================
# --- CONFIGURATION ---
# ==============================================================================
NUM_DECKS_TO_TEST = 200
PATTERN_LEN = 3
INPUT_DECK_FOLDER = 'data/decks/'
OUTPUT_DIR = 'data/comparisons/'
MD_SUMMARY_FILE = 'Scoring.md'
# ==============================================================================

def main():
    """Main function to orchestrate the test runs and output generation."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.isdir(INPUT_DECK_FOLDER):
        print(f"❌ ERROR: Input folder not found at '{INPUT_DECK_FOLDER}'")
        # Fallback to create dummy data for a first run
        os.makedirs(INPUT_DECK_FOLDER, exist_ok=True)
        dummy_file = os.path.join(INPUT_DECK_FOLDER, 'dummy_decks_01.npy')
        np.save(dummy_file, np.random.randint(0, 2, size=(NUM_DECKS_TO_TEST, 52)))
        print(f"Dummy file '{dummy_file}' created for demonstration.")

    print(f"Searching for .npy files in '{INPUT_DECK_FOLDER}'...")
    npy_files = sorted([os.path.join(INPUT_DECK_FOLDER, f) for f in os.listdir(INPUT_DECK_FOLDER) if f.endswith('.npy')])
    if not npy_files:
        print(f"❌ ERROR: No .npy files found."); return

    loaded_decks = [np.load(f) for f in npy_files]
    all_loaded_decks = np.concatenate(loaded_decks, axis=0)
    total_decks_available = len(all_loaded_decks)
    print(f"\nFound a total of {total_decks_available} decks.")

    if total_decks_available < NUM_DECKS_TO_TEST:
        print(f"[WARN] Only {total_decks_available} decks available. Using all of them (shuffled).")
        np.random.shuffle(all_loaded_decks)
        decks_to_test = all_loaded_decks
    else:
        print(f"Randomly selecting {NUM_DECKS_TO_TEST} decks for the test run...")
        indices = np.random.choice(total_decks_available, size=NUM_DECKS_TO_TEST, replace=False)
        decks_to_test = all_loaded_decks[indices]
    
    print(f"\nSuccessfully prepared {len(decks_to_test)} decks for testing.")

    performance_results = [
        run_and_profile('Approach 1', decks_to_test, PATTERN_LEN, OUTPUT_DIR),
        run_and_profile('Approach 2', decks_to_test, PATTERN_LEN, OUTPUT_DIR)
    ]

    perf_df = pd.DataFrame(performance_results)
    perf_csv_path = os.path.join(OUTPUT_DIR, 'performance_stats.csv')
    perf_df.to_csv(perf_csv_path, index=False)
    
    print("\n==============================================")
    print("✅ Testing Complete!")
    print(f"Performance comparison saved to: {perf_csv_path}")
    print("==============================================")
    print(perf_df.round(4).to_string(index=False))

    dtype_spec = {'p1': str, 'p2': str}
    df1 = pd.read_csv(os.path.join(OUTPUT_DIR, 'approach1_scores.csv'), dtype=dtype_spec)
    df2 = pd.read_csv(os.path.join(OUTPUT_DIR, 'approach2_scores.csv'), dtype=dtype_spec)
    
    update_markdown_summary(MD_SUMMARY_FILE, perf_df, df1, df2)

if __name__ == '__main__':
    main()