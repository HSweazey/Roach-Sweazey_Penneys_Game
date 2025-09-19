import os
from src.analysis.compare_performance import update_markdown_report
from src.analysis.db_run_analysis_loop import run_db_performance_test
from src.analysis.array_run_analysis_loop import run_array_performance_test
from src.analysis.compare_performance import generate_comparison_and_get_stats

# CONFIGURATION

TOTAL_ITERATIONS = 5
DECKS_PER_ITERATION = 2_000_000
ARRAY_BATCH_SIZE = 10_000

# --- Directory Paths ---
DATA_DIR = './data/comparisons'
FIGURES_DIR = './figures'
ARRAY_DECKS_DIR = './data/array_decks'
DB_DECKS_DIR = './data/db_decks'

# --- File Paths ---
DB_CSV_PATH = os.path.join(DATA_DIR, 'db_performance_stats.csv')
ARRAY_CSV_PATH = os.path.join(DATA_DIR, 'array_performance_stats.csv')
MARKDOWN_REPORT_PATH = './DataGeneration.md'

# --- Ensure Directories Exist ---
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(ARRAY_DECKS_DIR, exist_ok=True)
os.makedirs(DB_DECKS_DIR, exist_ok=True)


# MAIN EXECUTION

if __name__ == "__main__":
    print("🚀 Starting Full Performance Analysis and Reporting Workflow 🚀")
    
    print("\n" + "="*50)
    print("📋 Test Configuration:")
    print(f"  - Total Iterations:    {TOTAL_ITERATIONS}")
    print(f"  - Decks per Iteration: {DECKS_PER_ITERATION:,}")
    print(f"  - Array Batch Size:    {ARRAY_BATCH_SIZE:,}")
    print("="*50)
    
    run_db_performance_test(TOTAL_ITERATIONS, DECKS_PER_ITERATION, DB_CSV_PATH)
    run_array_performance_test(TOTAL_ITERATIONS, DECKS_PER_ITERATION, ARRAY_BATCH_SIZE, ARRAY_CSV_PATH, ARRAY_DECKS_DIR)
    
    db_average_stats, array_average_stats = generate_comparison_and_get_stats(DB_CSV_PATH, ARRAY_CSV_PATH, FIGURES_DIR)
    
    update_markdown_report(db_average_stats, array_average_stats, TOTAL_ITERATIONS, DECKS_PER_ITERATION, MARKDOWN_REPORT_PATH)
    
    print("\n🎉 Workflow Complete! 🎉")