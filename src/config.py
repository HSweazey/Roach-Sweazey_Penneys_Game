# define configuration constants for deck generation & database handling

# Card settings
CARDS_PER_COLOR = 26
DEFAULT_COMPOSITION = {"R": CARDS_PER_COLOR, "B": CARDS_PER_COLOR}

# Generation settings
BATCH_SIZE = 10000

# File paths
DATA_FOLDER = "./data/db_decks/"
DB_PATH = "decks.db"
