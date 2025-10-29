from itertools import product
from typing import List

def all_patterns(length: int) -> List[str]:
    """Return list of all binary patterns as strings e.g. '000'."""
    return [''.join(bits) for bits in product('01', repeat=length)]

def str_to_bits(s: str) -> List[int]:
    """Convert a binary string to a list of integers."""
    return [1 if ch == '1' else 0 for ch in s]

def match_pattern(deck: List[int], pattern: List[int]) -> int:
    """Return the index of the first occurence of pattern in deck, or -1."""
    m, n = len(pattern), len(deck)
    for i in range(n - m + 1):
        if deck[i:i+m] == pattern:
            return i
    return -1

def play_through_deck(deck, p1_bits, p2_bits):
    """
    Simulates playing through a deck of cards for Penney's Game.
    The player whose pattern appears first wins that trick, 
    earning all cards between the previous match and their pattern (inclusive).
    Any leftover cards at the end of the deck are discarded.
    """
    deck_str = "".join(map(str, deck))
    p1_cards = p1_tricks = p1_cards_wins = p1_tricks_wins = 0
    p2_cards = p2_tricks = p2_cards_wins = p2_tricks_wins= 0
    draw_cards = draw_tricks = 0
    last_idx = 0 

    p1_bits = "".join(map(str, p1_bits))
    p2_bits = "".join(map(str, p2_bits))

    while True:
        p1_idx = deck_str.find(p1_bits, last_idx)
        p2_idx = deck_str.find(p2_bits, last_idx)
        if p1_idx == -1 and p2_idx == -1:
            break
        if p1_idx != -1 and (p2_idx == -1 or p1_idx < p2_idx):
            winner = "p1"
            idx = p1_idx
            pattern_len = len(p1_bits)
        elif p2_idx != -1 and (p1_idx == -1 or p2_idx < p1_idx):
            winner = "p2"
            idx = p2_idx
            pattern_len = len(p2_bits)
        else:
            # (rare) exact tie in start positions
            winner = None
        if winner:
            cards_won = (idx + pattern_len) - last_idx
            if winner == "p1":
                p1_cards += cards_won
                p1_tricks += 1
            else:
                p2_cards += cards_won
                p2_tricks += 1
            last_idx = idx + pattern_len

    if p1_cards > p2_cards:
        p1_cards_wins += 1
    elif p1_cards < p2_cards:
        p2_cards_wins += 1
    else:
        draw_cards += 1
    
    if p1_tricks > p2_tricks:
        p1_tricks_wins += 1
    elif p1_tricks < p2_tricks:
        p2_tricks_wins += 1
    else:
        draw_tricks += 1

    return p1_cards, p1_cards_wins, p1_tricks, p1_tricks_wins, \
        p2_cards, p2_cards_wins, p2_tricks, p2_tricks_wins, \
        draw_cards, draw_tricks