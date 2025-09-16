# sweazey_generation.py (Corrected)
import os
import collections
import random
import re
from typing import Dict, List, Optional

class Deck:
    """
    A class representing a deck of cards, refined for database interaction.
    """
    def __init__(self, composition: Optional[Dict[str, int]] = None, shuffle: bool = True):
        if composition is None:
            self._composition = {'R': 26, 'B': 26}
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

def get_next_seed(data_folder='./data/sweazey_decks/'):
    """
    Finds the latest file in a directory based on a specific naming
    convention, retrieves the last random seed, and returns the next
    sequential seed value.
    """
    filename_pattern = re.compile(r'^decks_\d+_seed(\d+)\.npy$')
    last_seed = 0

    if not os.path.isdir(data_folder):
        print(f"Warning: Directory '{data_folder}' not found. Defaulting to seed 1.")
        # Create the directory if it doesn't exist to prevent errors later
        os.makedirs(data_folder, exist_ok=True)
        return 1

    for filename in os.listdir(data_folder):
        match = filename_pattern.match(filename)
        if match:
            seed = int(match.group(1))
            if seed > last_seed:
                last_seed = seed
    return last_seed + 1