import os
import numpy as np

# Import the core functions from your project's modules
from src.db_setup import setup_database, insert_decks, export_decks_and_clear_db
from src.db_processing import init_temp_db, process_single_batch_array_db, export_db_to_csv
from src.config import *
from src.heatmap import * # This imports generate_heatmaps

def augment_data(n:int):
    """Runs a simple test of the generation and scoring pipeline."""
    os.makedirs(DATA_UNSCORED_FOLDER, exist_ok=True)
    os.makedirs(DATA_SCORED_FOLDER, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    # <<< NEW >>> Also ensure FIGURES_DIR exists
    os.makedirs(FIGURES_DIR, exist_ok=True) 

    # --- STAGE 1: DECK GENERATION ---
    print("--- STAGE 1: Generating Decks ---")
    setup_database()
    insert_decks(n)
    export_decks_and_clear_db()
    print(f"✅ Generation complete. {n} decks saved to .npy files.")

    if SCORE_FLAG == True:
        # --- STAGE 2: SCORING ---
        print("\n--- STAGE 2: Scoring Decks ---")
        all_unscored_files = [os.path.join(DATA_UNSCORED_FOLDER, f) for f in os.listdir(DATA_UNSCORED_FOLDER) if f.endswith('.npy')]
        if not all_unscored_files:
            print("❌ ERROR: No deck files found to score."); return

        all_decks = np.concatenate([np.load(f) for f in all_unscored_files], axis=0)
        total_available = len(all_decks)
        
        indices = np.random.choice(total_available, size=total_available, replace=False)
        decks_to_score = all_decks[indices]
        print(f"Scoring {len(decks_to_score)} unscored decks.")

        scoring_db_path = os.path.join(RESULTS_DIR, 'temp_scoring.db')
        output_csv_path = os.path.join(RESULTS_DIR, 'scoring_results.csv')
        
        if os.path.exists(scoring_db_path):
            os.remove(scoring_db_path)

        db_conn = init_temp_db(scoring_db_path, PATTERN_LEN, seed_csv_path=output_csv_path)
        process_single_batch_array_db(decks_to_score, db_conn, PATTERN_LEN)
        db_conn.commit()
        export_db_to_csv(db_conn, output_csv_path)
        db_conn.close()
        os.remove(scoring_db_path)
        
        print(f"✅ Scoring complete. Results saved to {output_csv_path}")

        print("\n--- STAGE 3: Moving Scored Deck Files ---")
        for file_path in all_unscored_files:
            filename = os.path.basename(file_path)
            destination_path = os.path.join(DATA_SCORED_FOLDER, filename)
            print(f"  -> Moving {filename} to '{DATA_SCORED_FOLDER}'")
            os.rename(file_path, destination_path)
        print("✅ All scored decks moved.")

        # --- STAGE 4: UPDATING HEATMAPS ---
        print("\n--- STAGE 4: Generating Heatmaps ---")
        try:
            # Call the heatmap function, which will use the default RESULTS_CSV path
            generate_heatmaps()
        except FileNotFoundError as e:
            print(f"❌ ERROR: Could not generate heatmaps. {e}")
        except Exception as e:
            print(f"❌ ERROR: An unexpected error occurred during heatmap generation: {e}")
    
    print("\nPipeline test finished successfully! 🎉")
        

if __name__ == "__main__":
    n = int(input('How many decks would you like to generate? '))
    augment_data(n)