from itertools import product
from typing import List, Tuple

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


def play_through_deck(deck: List[int], p1_bits: List[int], p2_bits: List[int]) -> Tuple[int,int,int,int,int,int]:
    """
    Play through the entire deck until no pattern occurrences remain.
    Returns:
        (p1_cards, p1_tricks, p2_cards, p2_tricks, draw_cards, draw_tricks)
    
    Scoring:
    - Winner of each trick gets all cards since the last trick up to their matched pattern.
    - Draws are computed after the deck is fully scored:
        * draw_tricks = tricks tied
        * draw_cards = cards tied
    """
    p1_c = p1_t = p2_c = p2_t = 0
    last_idx = 0
    n = len(deck)
    L1, L2 = len(p1_bits), len(p2_bits)
    i = 0

    while i < n:
        # Find next occurrences relative to current index
        idx1_rel = match_pattern(deck[i:], p1_bits)
        idx2_rel = match_pattern(deck[i:], p2_bits)

        # If both patterns are gone, end
        if idx1_rel == -1 and idx2_rel == -1:
            break

        # Convert relative indices to absolute deck positions
        idx1 = i + idx1_rel if idx1_rel != -1 else float('inf')
        idx2 = i + idx2_rel if idx2_rel != -1 else float('inf')

        # Determine winner
        if idx1 < idx2:  # P1 wins
            cards_won = idx1 + L1 - last_idx
            p1_c += cards_won
            p1_t += 1
            last_idx = idx1 + L1
            i = last_idx
        elif idx2 < idx1:  # P2 wins
            cards_won = idx2 + L2 - last_idx
            p2_c += cards_won
            p2_t += 1
            last_idx = idx2 + L2
            i = last_idx
        else:  # One pattern missing
            # Winner by default if the other pattern doesn't exist
            if idx1 != float('inf'):
                cards_won = idx1 + L1 - last_idx
                p1_c += cards_won
                p1_t += 1
                last_idx = idx1 + L1
                i = last_idx
            elif idx2 != float('inf'):
                cards_won = idx2 + L2 - last_idx
                p2_c += cards_won
                p2_t += 1
                last_idx = idx2 + L2
                i = last_idx

    # --- Compute draws after deck is fully scored ---
    d_t = d_c = 0
    if p1_t == p2_t:
        d_t = p1_t  # tricks tied
    if p1_c == p2_c:
        d_c = p1_c  # cards tied

    return p1_c, p1_t, p2_c, p2_t, d_c, d_t


# original play through deck function that generated incorrect heatmaps: 

'''

def play_through_deck(deck: List[int], p1_bits: List[int], p2_bits: List[int]) -> Tuple[int, int, int, int, int, int]:
    """
    Play through the entire deck until no pattern occurences remain.
    Returns (p1_cards, p1_tricks, p2_cards, p2_tricks, draw_cards, draw_tricks).
    """
    p1_c = p1_t = p2_c = p2_t = d_c = d_t = 0
    i = 0
    n = len(deck)
    L1, L2 = len(p1_bits), len(p2_bits)

    while i < n:
        remaining = deck[i:]
        idx1 = match_pattern(remaining, p1_bits)
        idx2 = match_pattern(remaining, p2_bits)

        if idx1 == -1 and idx2 == -1: break
        if idx2 == -1: # P1 wins by default
            cards_won = min(idx1 + L1, len(remaining))
            p1_t += 1; p1_c += cards_won; i += cards_won
            continue
        if idx1 == -1: # P2 wins by default
            cards_won = min(idx2 + L2, len(remaining))
            p2_t += 1; p2_c += cards_won; i += cards_won
            continue
        
        # Both patterns exist, determine winner
        if idx1 < idx2:
            cards_won = min(idx1 + L1, len(remaining))
            p1_t += 1; p1_c += cards_won; i += cards_won
        elif idx2 < idx1:
            cards_won = min(idx2 + L2, len(remaining))
            p2_t += 1; p2_c += cards_won; i += cards_won
        else: # Draw
            cards_won = min(idx1 + max(L1, L2), len(remaining))
            d_t += 1; d_c += cards_won; i += cards_won
            
    return p1_c, p1_t, p2_c, p2_t, d_c, d_t

'''