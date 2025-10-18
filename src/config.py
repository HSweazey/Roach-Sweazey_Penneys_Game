# define configuration constants for deck generation & database handling

# Card settings
CARDS_PER_COLOR = 26
DECK_LEN = 52
DEFAULT_COMPOSITION = {"R": CARDS_PER_COLOR, "B": CARDS_PER_COLOR}

# Generation settings
BATCH_SIZE = 10000

# File paths
DATA_UNSCORED_FOLDER = "./data/decks/unscored"
DATA_SCORED_FOLDER = "./data/decks/scored"
DB_PATH = "decks.db"
FIGURES_DIR = "./figures"
RESULTS_DIR = "./data/results/"
RESULTS_CSV = "./data/results/scoring_results.csv"

# Player pattern length 
PATTERN_LEN = 3  

# Test Pipeline
SCORE_FLAG = True

