import random
import numpy as np
from datetime import datetime as dt
from typing import List, Callable

# debugger from class 

SHOW_ARGS = True  

def debugger(fun: Callable) -> Callable:
    def _wrapper(*args, **kwargs):
        print(f'{fun.__name__} called')
        if SHOW_ARGS:
            print(f'args: {args}')
            print(f'kwargs: {kwargs}')

        t0 = dt.now()
        # always write this line like this 

        results = fun(*args, **kwargs)
        print(f'ran for {dt.now()-t0} sec(s)')

        # do not modify the return signature 
        return results
    return _wrapper


# conversions 

def string_to_binary(seq: str) -> List[int]:
    '''
    convert a string like 'RRR' to binary [1, 1, 1]
    '''
    return [1 if ch == 'R' else 0 for ch in seq.upper()]

def binary_to_string(seq: List[int]) -> str:
    '''
    convert binary like [1, 0, 1] to string 'RBR'
    '''
    return ''.join('R' if bit == 1 else 'B' for bit in seq)


# simulate a deck of cards 

def generate_deck() -> List[int]: 
    '''
    generate 52 card deck as binary 
    half deck = 26, red = [1], black = [0]
    '''
    deck = ([1] * 26) + ([0] * 26)
    random.shuffle(deck)
    return deck 

def draw_cards(deck: List[int], n: int) -> List[int]:
    '''
    draw n cards from deck
    '''
    return deck[:n]


# play the game 

def match_pattern(deck: List[int], pattern: List[int]) -> int:
    '''
    return index of first time pattern is found in deck
    if pattern is not found in deck, return -1
    '''
    m, n = len(pattern), len(deck)
    for i in range(n - m + 1):
        if deck[i:i+m] == pattern:
            return i
        
    # if pattern not found 
    return -1

def play_game(deck: List[int], p1: List[int], p2: List[int]) -> int:
    '''
    simulate single round (trick) of penney's game 
    return 1 if p1 wins, 2 if p2 wins, 0 if draw 
    '''

    idx1 = match_pattern(deck, p1)
    idx2 = match_pattern(deck, p2)

    if idx1 == -1 and idx2 == -1: # neither pattern found, draw
        return 0 
    
    if idx1 == -1 and idx2 != -1: # only pattern 2 found, player 2 wins
        return 2
    
    if idx1 != -1 and idx2 == -1: # only pattern 1 found, player 1 wins
        return 1
    
    if idx1 < idx2: # pattern 1 appears first, player 1 wins 
        return 1 
    
    elif idx2 < idx1: # pattern 2 appears first, player 2 wins
        return 2

    else: 
        return 0 # draw (not technically possible if following rules)
    