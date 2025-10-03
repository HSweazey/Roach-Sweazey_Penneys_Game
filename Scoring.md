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

# Test Run Summary: 2025-10-03 15:00:59
## 📊 Performance Comparison
| approach   |   wall_time_seconds |   cpu_time_seconds |   peak_memory_mb |   num_decks_processed |
|:-----------|--------------------:|-------------------:|-----------------:|----------------------:|
| Approach 1 |            7.28613  |           7.27777  |        0.0651217 |                   200 |
| Approach 2 |            0.740335 |           0.738035 |        0.0201111 |                   200 |

## Scores: Approach 1 (pandas_in_memory)
| p1   | p2   |   p1_cards |   p1_tricks |   p2_cards |   p2_tricks |   draw_cards |   draw_tricks |   games_count |
|:-----|:-----|-----------:|------------:|-----------:|------------:|-------------:|--------------:|--------------:|
| BBB  | BBR  |      33310 |        4950 |      33362 |        5178 |            0 |             0 |          1400 |
| BBB  | BRB  |      26423 |        4120 |      40369 |        6295 |            0 |             0 |          1400 |
| BBB  | BRR  |      26126 |        4950 |      42391 |        7622 |            0 |             0 |          1400 |
| BBB  | RBB  |       3465 |        1155 |      63185 |        8972 |            0 |             0 |          1400 |
| BBB  | RBR  |      28099 |        4950 |      40130 |        7066 |            0 |             0 |          1400 |
| BBB  | RRB  |      16812 |        3627 |      51748 |        8911 |            0 |             0 |          1400 |
| BBB  | RRR  |      33397 |        4950 |      32466 |        4873 |            0 |             0 |          1400 |
| BBR  | BBB  |      33362 |        5178 |      33310 |        4950 |            0 |             0 |          1400 |
| BBR  | BRB  |      48419 |        7989 |      20036 |        4039 |            0 |             0 |          1400 |
| BBR  | BRR  |      49324 |        8991 |      19921 |        4428 |            0 |             0 |          1400 |
| BBR  | RBB  |      10487 |        2758 |      56809 |        8405 |            0 |             0 |          1400 |
| BBR  | RBR  |      47216 |        8991 |      22423 |        5317 |            0 |             0 |          1400 |
| BBR  | RRB  |      34872 |        7206 |      34770 |        7169 |            0 |             0 |          1400 |
| BBR  | RRR  |      52269 |        8991 |      16499 |        3649 |            0 |             0 |          1400 |
| BRB  | BBB  |      40369 |        6295 |      26423 |        4120 |            0 |             0 |          1400 |
| BRB  | BBR  |      20036 |        4039 |      48419 |        7989 |            0 |             0 |          1400 |
| BRB  | BRR  |      34667 |        7118 |      34808 |        7176 |            0 |             0 |          1400 |
| BRB  | RBB  |      31375 |        5891 |      36782 |        6125 |            0 |             0 |          1400 |
| BRB  | RBR  |      33399 |        5076 |      33019 |        4990 |            0 |             0 |          1400 |
| BRB  | RRB  |      22701 |        5413 |      46810 |        8911 |            0 |             0 |          1400 |
| BRB  | RRR  |      40460 |        7118 |      27777 |        4873 |            0 |             0 |          1400 |
| BRR  | BBB  |      42391 |        7622 |      26126 |        4950 |            0 |             0 |          1400 |
| BRR  | BBR  |      19921 |        4428 |      49324 |        8991 |            0 |             0 |          1400 |
| BRR  | BRB  |      34808 |        7176 |      34667 |        7118 |            0 |             0 |          1400 |
| BRR  | RBB  |      34773 |        7207 |      34685 |        7164 |            0 |             0 |          1400 |
| BRR  | RBR  |      36635 |        6089 |      31671 |        5849 |            0 |             0 |          1400 |
| BRR  | RRB  |      56614 |        8317 |      10780 |        2832 |            0 |             0 |          1400 |
| BRR  | RRR  |      63202 |        8915 |       3618 |        1206 |            0 |             0 |          1400 |
| RBB  | BBB  |      63185 |        8972 |       3465 |        1155 |            0 |             0 |          1400 |
| RBB  | BBR  |      56809 |        8405 |      10487 |        2758 |            0 |             0 |          1400 |
| RBB  | BRB  |      36782 |        6125 |      31375 |        5891 |            0 |             0 |          1400 |
| RBB  | BRR  |      34685 |        7164 |      34773 |        7207 |            0 |             0 |          1400 |
| RBB  | RBR  |      35022 |        7247 |      34384 |        7066 |            0 |             0 |          1400 |
| RBB  | RRB  |      20059 |        4446 |      49087 |        8911 |            0 |             0 |          1400 |
| RBB  | RRR  |      43054 |        7718 |      25570 |        4873 |            0 |             0 |          1400 |
| RBR  | BBB  |      40130 |        7066 |      28099 |        4950 |            0 |             0 |          1400 |
| RBR  | BBR  |      22423 |        5317 |      47216 |        8991 |            0 |             0 |          1400 |
| RBR  | BRB  |      33019 |        4990 |      33399 |        5076 |            0 |             0 |          1400 |
| RBR  | BRR  |      31671 |        5849 |      36635 |        6089 |            0 |             0 |          1400 |
| RBR  | RBB  |      34384 |        7066 |      35022 |        7247 |            0 |             0 |          1400 |
| RBR  | RRB  |      20634 |        4079 |      47716 |        7857 |            0 |             0 |          1400 |
| RBR  | RRR  |      40599 |        6312 |      26303 |        4086 |            0 |             0 |          1400 |
| RRB  | BBB  |      51748 |        8911 |      16812 |        3627 |            0 |             0 |          1400 |
| RRB  | BBR  |      34770 |        7169 |      34872 |        7206 |            0 |             0 |          1400 |
| RRB  | BRB  |      46810 |        8911 |      22701 |        5413 |            0 |             0 |          1400 |
| RRB  | BRR  |      10780 |        2832 |      56614 |        8317 |            0 |             0 |          1400 |
| RRB  | RBB  |      49087 |        8911 |      20059 |        4446 |            0 |             0 |          1400 |
| RRB  | RBR  |      47716 |        7857 |      20634 |        4079 |            0 |             0 |          1400 |
| RRB  | RRR  |      33378 |        5253 |      33443 |        4873 |            0 |             0 |          1400 |
| RRR  | BBB  |      32466 |        4873 |      33397 |        4950 |            0 |             0 |          1400 |
| RRR  | BBR  |      16499 |        3649 |      52269 |        8991 |            0 |             0 |          1400 |
| RRR  | BRB  |      27777 |        4873 |      40460 |        7118 |            0 |             0 |          1400 |
| RRR  | BRR  |       3618 |        1206 |      63202 |        8915 |            0 |             0 |          1400 |
| RRR  | RBB  |      25570 |        4873 |      43054 |        7718 |            0 |             0 |          1400 |
| RRR  | RBR  |      26303 |        4086 |      40599 |        6312 |            0 |             0 |          1400 |
| RRR  | RRB  |      33443 |        4873 |      33378 |        5253 |            0 |             0 |          1400 |

## Scores: Approach 2 (sqlite_temp_db)
*Note: The numerical results here should be identical to Approach 1.*
| p1   | p2   |   p1_cards |   p1_tricks |   p2_cards |   p2_tricks |   draw_cards |   draw_tricks |   games_count |
|:-----|:-----|-----------:|------------:|-----------:|------------:|-------------:|--------------:|--------------:|
| BBB  | BBR  |      33310 |        4950 |      33362 |        5178 |            0 |             0 |          1400 |
| BBB  | BRB  |      26423 |        4120 |      40369 |        6295 |            0 |             0 |          1400 |
| BBB  | BRR  |      26126 |        4950 |      42391 |        7622 |            0 |             0 |          1400 |
| BBB  | RBB  |       3465 |        1155 |      63185 |        8972 |            0 |             0 |          1400 |
| BBB  | RBR  |      28099 |        4950 |      40130 |        7066 |            0 |             0 |          1400 |
| BBB  | RRB  |      16812 |        3627 |      51748 |        8911 |            0 |             0 |          1400 |
| BBB  | RRR  |      33397 |        4950 |      32466 |        4873 |            0 |             0 |          1400 |
| BBR  | BBB  |      33362 |        5178 |      33310 |        4950 |            0 |             0 |          1400 |
| BBR  | BRB  |      48419 |        7989 |      20036 |        4039 |            0 |             0 |          1400 |
| BBR  | BRR  |      49324 |        8991 |      19921 |        4428 |            0 |             0 |          1400 |
| BBR  | RBB  |      10487 |        2758 |      56809 |        8405 |            0 |             0 |          1400 |
| BBR  | RBR  |      47216 |        8991 |      22423 |        5317 |            0 |             0 |          1400 |
| BBR  | RRB  |      34872 |        7206 |      34770 |        7169 |            0 |             0 |          1400 |
| BBR  | RRR  |      52269 |        8991 |      16499 |        3649 |            0 |             0 |          1400 |
| BRB  | BBB  |      40369 |        6295 |      26423 |        4120 |            0 |             0 |          1400 |
| BRB  | BBR  |      20036 |        4039 |      48419 |        7989 |            0 |             0 |          1400 |
| BRB  | BRR  |      34667 |        7118 |      34808 |        7176 |            0 |             0 |          1400 |
| BRB  | RBB  |      31375 |        5891 |      36782 |        6125 |            0 |             0 |          1400 |
| BRB  | RBR  |      33399 |        5076 |      33019 |        4990 |            0 |             0 |          1400 |
| BRB  | RRB  |      22701 |        5413 |      46810 |        8911 |            0 |             0 |          1400 |
| BRB  | RRR  |      40460 |        7118 |      27777 |        4873 |            0 |             0 |          1400 |
| BRR  | BBB  |      42391 |        7622 |      26126 |        4950 |            0 |             0 |          1400 |
| BRR  | BBR  |      19921 |        4428 |      49324 |        8991 |            0 |             0 |          1400 |
| BRR  | BRB  |      34808 |        7176 |      34667 |        7118 |            0 |             0 |          1400 |
| BRR  | RBB  |      34773 |        7207 |      34685 |        7164 |            0 |             0 |          1400 |
| BRR  | RBR  |      36635 |        6089 |      31671 |        5849 |            0 |             0 |          1400 |
| BRR  | RRB  |      56614 |        8317 |      10780 |        2832 |            0 |             0 |          1400 |
| BRR  | RRR  |      63202 |        8915 |       3618 |        1206 |            0 |             0 |          1400 |
| RBB  | BBB  |      63185 |        8972 |       3465 |        1155 |            0 |             0 |          1400 |
| RBB  | BBR  |      56809 |        8405 |      10487 |        2758 |            0 |             0 |          1400 |
| RBB  | BRB  |      36782 |        6125 |      31375 |        5891 |            0 |             0 |          1400 |
| RBB  | BRR  |      34685 |        7164 |      34773 |        7207 |            0 |             0 |          1400 |
| RBB  | RBR  |      35022 |        7247 |      34384 |        7066 |            0 |             0 |          1400 |
| RBB  | RRB  |      20059 |        4446 |      49087 |        8911 |            0 |             0 |          1400 |
| RBB  | RRR  |      43054 |        7718 |      25570 |        4873 |            0 |             0 |          1400 |
| RBR  | BBB  |      40130 |        7066 |      28099 |        4950 |            0 |             0 |          1400 |
| RBR  | BBR  |      22423 |        5317 |      47216 |        8991 |            0 |             0 |          1400 |
| RBR  | BRB  |      33019 |        4990 |      33399 |        5076 |            0 |             0 |          1400 |
| RBR  | BRR  |      31671 |        5849 |      36635 |        6089 |            0 |             0 |          1400 |
| RBR  | RBB  |      34384 |        7066 |      35022 |        7247 |            0 |             0 |          1400 |
| RBR  | RRB  |      20634 |        4079 |      47716 |        7857 |            0 |             0 |          1400 |
| RBR  | RRR  |      40599 |        6312 |      26303 |        4086 |            0 |             0 |          1400 |
| RRB  | BBB  |      51748 |        8911 |      16812 |        3627 |            0 |             0 |          1400 |
| RRB  | BBR  |      34770 |        7169 |      34872 |        7206 |            0 |             0 |          1400 |
| RRB  | BRB  |      46810 |        8911 |      22701 |        5413 |            0 |             0 |          1400 |
| RRB  | BRR  |      10780 |        2832 |      56614 |        8317 |            0 |             0 |          1400 |
| RRB  | RBB  |      49087 |        8911 |      20059 |        4446 |            0 |             0 |          1400 |
| RRB  | RBR  |      47716 |        7857 |      20634 |        4079 |            0 |             0 |          1400 |
| RRB  | RRR  |      33378 |        5253 |      33443 |        4873 |            0 |             0 |          1400 |
| RRR  | BBB  |      32466 |        4873 |      33397 |        4950 |            0 |             0 |          1400 |
| RRR  | BBR  |      16499 |        3649 |      52269 |        8991 |            0 |             0 |          1400 |
| RRR  | BRB  |      27777 |        4873 |      40460 |        7118 |            0 |             0 |          1400 |
| RRR  | BRR  |       3618 |        1206 |      63202 |        8915 |            0 |             0 |          1400 |
| RRR  | RBB  |      25570 |        4873 |      43054 |        7718 |            0 |             0 |          1400 |
| RRR  | RBR  |      26303 |        4086 |      40599 |        6312 |            0 |             0 |          1400 |
| RRR  | RRB  |      33443 |        4873 |      33378 |        5253 |            0 |             0 |          1400 |
