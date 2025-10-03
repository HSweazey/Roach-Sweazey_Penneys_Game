## Approach 1: Pandas in Memory 
In both of our scoring approaches, the core game mechanics are implemented in the shared game_logic module. This provides utilities for generating all possible binary patterns (all_patterns), converting single string representations to lists of integers, locating the first occurence of a pattern withing a deck (match_pattern), and simulating an entire play-through of Penney's Game Between two patterns. 

Our first scoring method maintains all scoring results in memory using a pandas dataframe instead of relying on an external persistence layer. At initialization, the dataframe is seeded with every possible ordered pair of binary patterns, each row pre-allocated with counters for cards, tricks, and games played. As decks are streamed from disk in batches of numpy arrays, each one is converted into a python list for simulation with the shared play_through_deck function. The results from each match are then applied directly to the in-memory dataframe using update_aggregate_df, which updates the cumulative counts by locating the appropriate row and incrementing its fields. This approach was focused more on simplicity than efficiency. All intermediate results are kept in RAM, updates happen in-place without queries. 


## Approach 2: Temporary Database
Our second scoring method similarly processes the decks stored in the generated .npy files and computes the outcomes for every possible combination of a 3-card-selection. This approach utilizes the sqlite UPDATE command for each individual game. First, it extracts a deck and converts it to a python list of integers (0 sand 1s). Then, using the standard play_through_deck function, it does basic pattern matching for each possible combination. Finally, it looks through the database, updating the correct row with the corresponding statistics from the game. Then, it exports that data to a .csv file and deletes the temporary database for file size purposes. We wanted to try using a database again since it showed some surprising performance statistics during the deck generation stage. We also wanted to see what the benefits were of avoiding holding the data in memory.


## Testing
To test our code, we used 10-200 randomly selected decks (currently set at 200) to play each possible iteration of Penny’s Game. Eventually, we will track what files and decks have been used so there is absolutely no repetition, but we simply wanted to make sure our pipeline was working. It uses both approaches on the same sample, run’s the computations as specified in the above sections, and updates each .csv. It also keeps track of similar statistics we used during the generation phase for the purpose of comparing the two approaches. Specifically we look at how many decks were processed, peak memory, wall time (total elapsed time), and CPU time (time when CPU is actively executing instructions in the program).


## Selection and Reasoning 
In the end, it seemed once again the database-based method outperformed the other approach. As seen in the performance table, the database approach took significantly less time and memory (as we predicted since the dataframe approach is based in memory). With the time disparity using only 200 decks, we certainly must prioritize time as we will get up to 2 million (or maybe even 10 million) decks. Both approaches’ numeric content is the same, showing they both are accurate and are interchangeable in surface functionality.


---

# Test Run Summary: 2025-10-03 15:06:43
## 📊 Performance Comparison
| approach                      |   wall_time_seconds |   cpu_time_seconds |   peak_memory_mb |   num_decks_processed |
|:------------------------------|--------------------:|-------------------:|-----------------:|----------------------:|
| Approach 1 (pandas_in_memory) |            7.36152  |           7.35654  |        0.0651217 |                   200 |
| Approach 2 (sqlite_temp_db)   |            0.736207 |           0.735207 |        0.0201111 |                   200 |

## Scores: Approach 1 (pandas_in_memory)
| p1   | p2   |   p1_cards |   p1_tricks |   p2_cards |   p2_tricks |   draw_cards |   draw_tricks |   games_count |
|:-----|:-----|-----------:|------------:|-----------:|------------:|-------------:|--------------:|--------------:|
| BBB  | BBR  |      43156 |        6394 |      42701 |        6636 |            0 |             0 |          1800 |
| BBB  | BRB  |      34123 |        5303 |      51725 |        8069 |            0 |             0 |          1800 |
| BBB  | BRR  |      33777 |        6394 |      54401 |        9812 |            0 |             0 |          1800 |
| BBB  | RBB  |       4479 |        1493 |      81315 |       11532 |            0 |             0 |          1800 |
| BBB  | RBR  |      36184 |        6394 |      51536 |        9078 |            0 |             0 |          1800 |
| BBB  | RRB  |      21613 |        4668 |      66576 |       11476 |            0 |             0 |          1800 |
| BBB  | RRR  |      42973 |        6394 |      41867 |        6299 |            0 |             0 |          1800 |
| BBR  | BBB  |      42701 |        6636 |      43156 |        6394 |            0 |             0 |          1800 |
| BBR  | BRB  |      62210 |       10291 |      25783 |        5182 |            0 |             0 |          1800 |
| BBR  | BRR  |      63354 |       11551 |      25658 |        5708 |            0 |             0 |          1800 |
| BBR  | RBB  |      13419 |        3526 |      73157 |       10805 |            0 |             0 |          1800 |
| BBR  | RBR  |      60717 |       11551 |      28819 |        6840 |            0 |             0 |          1800 |
| BBR  | RRB  |      44726 |        9268 |      44759 |        9222 |            0 |             0 |          1800 |
| BBR  | RRR  |      66952 |       11551 |      21400 |        4692 |            0 |             0 |          1800 |
| BRB  | BBB  |      51725 |        8069 |      34123 |        5303 |            0 |             0 |          1800 |
| BRB  | BBR  |      25783 |        5182 |      62210 |       10291 |            0 |             0 |          1800 |
| BRB  | BRR  |      44507 |        9131 |      44884 |        9238 |            0 |             0 |          1800 |
| BRB  | RBB  |      40317 |        7584 |      47328 |        7882 |            0 |             0 |          1800 |
| BRB  | RBR  |      42889 |        6508 |      42455 |        6433 |            0 |             0 |          1800 |
| BRB  | RRB  |      29091 |        6933 |      60243 |       11476 |            0 |             0 |          1800 |
| BRB  | RRR  |      51875 |        9131 |      35785 |        6299 |            0 |             0 |          1800 |
| BRR  | BBB  |      54401 |        9812 |      33777 |        6394 |            0 |             0 |          1800 |
| BRR  | BBR  |      25658 |        5708 |      63354 |       11551 |            0 |             0 |          1800 |
| BRR  | BRB  |      44884 |        9238 |      44507 |        9131 |            0 |             0 |          1800 |
| BRR  | RBB  |      44761 |        9280 |      44570 |        9203 |            0 |             0 |          1800 |
| BRR  | RBR  |      47074 |        7855 |      40733 |        7542 |            0 |             0 |          1800 |
| BRR  | RRB  |      72976 |       10745 |      13692 |        3608 |            0 |             0 |          1800 |
| BRR  | RRR  |      81335 |       11486 |       4587 |        1529 |            0 |             0 |          1800 |
| RBB  | BBB  |      81315 |       11532 |       4479 |        1493 |            0 |             0 |          1800 |
| RBB  | BBR  |      73157 |       10805 |      13419 |        3526 |            0 |             0 |          1800 |
| RBB  | BRB  |      47328 |        7882 |      40317 |        7584 |            0 |             0 |          1800 |
| RBB  | BRR  |      44570 |        9203 |      44761 |        9280 |            0 |             0 |          1800 |
| RBB  | RBR  |      45078 |        9315 |      44150 |        9078 |            0 |             0 |          1800 |
| RBB  | RRB  |      25698 |        5690 |      63201 |       11476 |            0 |             0 |          1800 |
| RBB  | RRR  |      54990 |        9907 |      33237 |        6299 |            0 |             0 |          1800 |
| RBR  | BBB  |      51536 |        9078 |      36184 |        6394 |            0 |             0 |          1800 |
| RBR  | BBR  |      28819 |        6840 |      60717 |       11551 |            0 |             0 |          1800 |
| RBR  | BRB  |      42455 |        6433 |      42889 |        6508 |            0 |             0 |          1800 |
| RBR  | BRR  |      40733 |        7542 |      47074 |        7855 |            0 |             0 |          1800 |
| RBR  | RBB  |      44150 |        9078 |      45078 |        9315 |            0 |             0 |          1800 |
| RBR  | RRB  |      26520 |        5224 |      61294 |       10167 |            0 |             0 |          1800 |
| RBR  | RRR  |      52167 |        8076 |      33769 |        5274 |            0 |             0 |          1800 |
| RRB  | BBB  |      66576 |       11476 |      21613 |        4668 |            0 |             0 |          1800 |
| RRB  | BBR  |      44759 |        9222 |      44726 |        9268 |            0 |             0 |          1800 |
| RRB  | BRB  |      60243 |       11476 |      29091 |        6933 |            0 |             0 |          1800 |
| RRB  | BRR  |      13692 |        3608 |      72976 |       10745 |            0 |             0 |          1800 |
| RRB  | RBB  |      63201 |       11476 |      25698 |        5690 |            0 |             0 |          1800 |
| RRB  | RBR  |      61294 |       10167 |      26520 |        5224 |            0 |             0 |          1800 |
| RRB  | RRR  |      42716 |        6704 |      43123 |        6299 |            0 |             0 |          1800 |
| RRR  | BBB  |      41867 |        6299 |      42973 |        6394 |            0 |             0 |          1800 |
| RRR  | BBR  |      21400 |        4692 |      66952 |       11551 |            0 |             0 |          1800 |
| RRR  | BRB  |      35785 |        6299 |      51875 |        9131 |            0 |             0 |          1800 |
| RRR  | BRR  |       4587 |        1529 |      81335 |       11486 |            0 |             0 |          1800 |
| RRR  | RBB  |      33237 |        6299 |      54990 |        9907 |            0 |             0 |          1800 |
| RRR  | RBR  |      33769 |        5274 |      52167 |        8076 |            0 |             0 |          1800 |
| RRR  | RRB  |      43123 |        6299 |      42716 |        6704 |            0 |             0 |          1800 |

## Scores: Approach 2 (sqlite_temp_db)
*Note: The numerical results here should be identical to Approach 1.*
| p1   | p2   |   p1_cards |   p1_tricks |   p2_cards |   p2_tricks |   draw_cards |   draw_tricks |   games_count |
|:-----|:-----|-----------:|------------:|-----------:|------------:|-------------:|--------------:|--------------:|
| BBB  | BBR  |      43156 |        6394 |      42701 |        6636 |            0 |             0 |          1800 |
| BBB  | BRB  |      34123 |        5303 |      51725 |        8069 |            0 |             0 |          1800 |
| BBB  | BRR  |      33777 |        6394 |      54401 |        9812 |            0 |             0 |          1800 |
| BBB  | RBB  |       4479 |        1493 |      81315 |       11532 |            0 |             0 |          1800 |
| BBB  | RBR  |      36184 |        6394 |      51536 |        9078 |            0 |             0 |          1800 |
| BBB  | RRB  |      21613 |        4668 |      66576 |       11476 |            0 |             0 |          1800 |
| BBB  | RRR  |      42973 |        6394 |      41867 |        6299 |            0 |             0 |          1800 |
| BBR  | BBB  |      42701 |        6636 |      43156 |        6394 |            0 |             0 |          1800 |
| BBR  | BRB  |      62210 |       10291 |      25783 |        5182 |            0 |             0 |          1800 |
| BBR  | BRR  |      63354 |       11551 |      25658 |        5708 |            0 |             0 |          1800 |
| BBR  | RBB  |      13419 |        3526 |      73157 |       10805 |            0 |             0 |          1800 |
| BBR  | RBR  |      60717 |       11551 |      28819 |        6840 |            0 |             0 |          1800 |
| BBR  | RRB  |      44726 |        9268 |      44759 |        9222 |            0 |             0 |          1800 |
| BBR  | RRR  |      66952 |       11551 |      21400 |        4692 |            0 |             0 |          1800 |
| BRB  | BBB  |      51725 |        8069 |      34123 |        5303 |            0 |             0 |          1800 |
| BRB  | BBR  |      25783 |        5182 |      62210 |       10291 |            0 |             0 |          1800 |
| BRB  | BRR  |      44507 |        9131 |      44884 |        9238 |            0 |             0 |          1800 |
| BRB  | RBB  |      40317 |        7584 |      47328 |        7882 |            0 |             0 |          1800 |
| BRB  | RBR  |      42889 |        6508 |      42455 |        6433 |            0 |             0 |          1800 |
| BRB  | RRB  |      29091 |        6933 |      60243 |       11476 |            0 |             0 |          1800 |
| BRB  | RRR  |      51875 |        9131 |      35785 |        6299 |            0 |             0 |          1800 |
| BRR  | BBB  |      54401 |        9812 |      33777 |        6394 |            0 |             0 |          1800 |
| BRR  | BBR  |      25658 |        5708 |      63354 |       11551 |            0 |             0 |          1800 |
| BRR  | BRB  |      44884 |        9238 |      44507 |        9131 |            0 |             0 |          1800 |
| BRR  | RBB  |      44761 |        9280 |      44570 |        9203 |            0 |             0 |          1800 |
| BRR  | RBR  |      47074 |        7855 |      40733 |        7542 |            0 |             0 |          1800 |
| BRR  | RRB  |      72976 |       10745 |      13692 |        3608 |            0 |             0 |          1800 |
| BRR  | RRR  |      81335 |       11486 |       4587 |        1529 |            0 |             0 |          1800 |
| RBB  | BBB  |      81315 |       11532 |       4479 |        1493 |            0 |             0 |          1800 |
| RBB  | BBR  |      73157 |       10805 |      13419 |        3526 |            0 |             0 |          1800 |
| RBB  | BRB  |      47328 |        7882 |      40317 |        7584 |            0 |             0 |          1800 |
| RBB  | BRR  |      44570 |        9203 |      44761 |        9280 |            0 |             0 |          1800 |
| RBB  | RBR  |      45078 |        9315 |      44150 |        9078 |            0 |             0 |          1800 |
| RBB  | RRB  |      25698 |        5690 |      63201 |       11476 |            0 |             0 |          1800 |
| RBB  | RRR  |      54990 |        9907 |      33237 |        6299 |            0 |             0 |          1800 |
| RBR  | BBB  |      51536 |        9078 |      36184 |        6394 |            0 |             0 |          1800 |
| RBR  | BBR  |      28819 |        6840 |      60717 |       11551 |            0 |             0 |          1800 |
| RBR  | BRB  |      42455 |        6433 |      42889 |        6508 |            0 |             0 |          1800 |
| RBR  | BRR  |      40733 |        7542 |      47074 |        7855 |            0 |             0 |          1800 |
| RBR  | RBB  |      44150 |        9078 |      45078 |        9315 |            0 |             0 |          1800 |
| RBR  | RRB  |      26520 |        5224 |      61294 |       10167 |            0 |             0 |          1800 |
| RBR  | RRR  |      52167 |        8076 |      33769 |        5274 |            0 |             0 |          1800 |
| RRB  | BBB  |      66576 |       11476 |      21613 |        4668 |            0 |             0 |          1800 |
| RRB  | BBR  |      44759 |        9222 |      44726 |        9268 |            0 |             0 |          1800 |
| RRB  | BRB  |      60243 |       11476 |      29091 |        6933 |            0 |             0 |          1800 |
| RRB  | BRR  |      13692 |        3608 |      72976 |       10745 |            0 |             0 |          1800 |
| RRB  | RBB  |      63201 |       11476 |      25698 |        5690 |            0 |             0 |          1800 |
| RRB  | RBR  |      61294 |       10167 |      26520 |        5224 |            0 |             0 |          1800 |
| RRB  | RRR  |      42716 |        6704 |      43123 |        6299 |            0 |             0 |          1800 |
| RRR  | BBB  |      41867 |        6299 |      42973 |        6394 |            0 |             0 |          1800 |
| RRR  | BBR  |      21400 |        4692 |      66952 |       11551 |            0 |             0 |          1800 |
| RRR  | BRB  |      35785 |        6299 |      51875 |        9131 |            0 |             0 |          1800 |
| RRR  | BRR  |       4587 |        1529 |      81335 |       11486 |            0 |             0 |          1800 |
| RRR  | RBB  |      33237 |        6299 |      54990 |        9907 |            0 |             0 |          1800 |
| RRR  | RBR  |      33769 |        5274 |      52167 |        8076 |            0 |             0 |          1800 |
| RRR  | RRB  |      43123 |        6299 |      42716 |        6704 |            0 |             0 |          1800 |
