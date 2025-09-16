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