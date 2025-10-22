# Penney's Game

**Hannah Sweazey** and **Ella Roach** wrote this project for **DATA 440: Automations and Workflow** with the intention of developing our skill and efficiency as python programmers. 

## Highlights 
This project...
- Generates randomized decks of red and black cards to simulate repeated simlations of Penney's Game. 
- Scores gameplay outcomes for all pattern pairs of length 3 across all simulated decks. 
- Implements full game logic, tracking both tricks won and cards won for each player. 
- Generates and updates visual heatmaps summarizing strategy advantages based on scoring approach. 

## Overview 

### Penney's Game

Penney's Game is a classic probability paradox which involves two players who each choose a sequence (or "pattern") of coin flips. Each player's pattern is typically of length three, such as HHT or THT. A coin is then flipped repeatedly, and the first player whose pattern appears wins. 

This project applies the logic of Penney's Game using red (R) and black (B) cards in a shuffled deck instead of heads and tails such that each simulated deck of 52 cards is a string of binary outcomes (R = 1, B = 0). 

**For more information on Penney's Game:** [Penney's Game Wikipedia](https://en.wikipedia.org/wiki/Penney%27s_game)

### Humble-Nishiyama Game

The Humble-Nishiyama variant of Penney's Game changes how each round of the game is resolved. Instead of simply checking which pattern appears first, it divides the deck into a sequence of "**tricks**." Whenever either player's pattern appears, that player has won a trick and collects all the cards that were turned over between the previous trick and the trick won. This process is repeated until the entire deck is played through. 

### Tricks vs. Cards Scoring 

This simulated gameplay scores two distinct methods accross all pattern pairs:

1. **Tricks Scoring:** Each time a player's pattern appears before their opponent's, that player earns one trick. The final score reflects the total number of tricks won by each player. At the end of the deck, the player with the most tricks has won the game. 

2. **Cards Scoring:** This scoring variant tracks the number of cards captured in the tricks won by each player, while disregarding the actual number of tricks. The final score reflects the number of cards won by each player. At the end of the deck, the player with the most cards has won the game. 

### Summary

This project simulates millions of games to estimate win probabilites under both scoring systems. The results are visualized as heatmaps, where rows represent the opponent's choice and columns represent the player's response. Darker cells indicate higher win percentages, and the parenthesis show the rate of draws. For each row, the player's ideal choice given their opponent's choice is lableled with a black outline.  



# Quick Start Guide


## Installing UV

This project is managed using UV, the link to which you can find [here](https://docs.astral.sh/uv/guides/install-python/).

Once you've properly installed UV, download the project and set it to your machine's directory. Then, run these commands to download dependencies and start the program.

```bash
uv sync
uv run main.py
```

If you need any troubleshooting assitance, refer to [UV's documentation](https://docs.astral.sh/uv/guides/install-python/).

## Content

*Below is a list of the folders you will find in this repository and a breif description of their contents and general functionality.*

`main.py`: the script you will call to run the program, automatically handles deck generation, scoring, and visualizations

`src/`: folder containing all files necessary for the program to run, has individual files for database creation, deck generation, scoring, and visualizations

`data/`: folder containing all data associated with the program including:

- a `decks/`folder that stores scored and unscored decks separately
- a `results/` folder that stores the overall scores .csv

`figures/`: folder that contains both heatmaps for each scoring method (cards vs tricks)