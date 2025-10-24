import os
import collections
import random
import re
from typing import Dict, List, Optional

from .config import DEFAULT_COMPOSITION, DATA_SCORED_FOLDER, DATA_UNSCORED_FOLDER

class Deck:
    """
    Class representing a deck of cards, refined for database interaction.
    """
    def __init__(self, composition: Optional[Dict[str, int]] = None, shuffle: bool = True):
        if composition is None:
            self._composition = DEFAULT_COMPOSITION.copy()
        else:
            self._composition = composition
        
        card_list: List[str] = []
        for card_type, count in self._composition.items():
            card_list.extend([card_type] * count)
        
        if shuffle:
            random.shuffle(card_list)
        
        self.cards = collections.deque(card_list)

    def get_sequence_string(self) -> str:
        return "".join(self.cards)

    @classmethod
    def from_sequence_string(cls, sequence: str) -> 'Deck':
        new_deck = cls(composition={}, shuffle=False)
        new_deck.cards = collections.deque(list(sequence))
        return new_deck

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f"Deck with {len(self)} cards. Top card: {self.cards[0] if self.cards else 'N/A'}"

def get_next_seed(data_unscored=DATA_UNSCORED_FOLDER, data_scored=DATA_SCORED_FOLDER) -> int:
    """
    Finds the last used seed by searching for the highest seed number
    in both the unscored and scored data folders.
    """
    filename_pattern = re.compile(r'^decks_\d+_seed(\d+)\.npy$')
    last_seed = 0
    folders_to_check = [data_unscored, data_scored]

    # Loop through each specified folder
    for folder in folders_to_check:
        if not os.path.isdir(folder):
            print(f"Warning: Directory '{folder}' not found. Skipping.")
            continue

        # Check every file in the current folder
        for filename in os.listdir(folder):
            match = filename_pattern.match(filename)
            if match:
                seed = int(match.group(1))
                # Update last_seed if the current file's seed is higher
                if seed > last_seed:
                    last_seed = seed
                    
    # If no files were found, last_seed remains 0, so this returns 1.
    return last_seed + 1