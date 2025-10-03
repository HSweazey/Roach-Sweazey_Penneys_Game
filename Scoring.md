## Approach 1: Pandas in Memory 
In both of our scoring approaches, the core game mechanics are implemented in the shared game_logic module. This provides utilities for generating all possible binary patterns (all_patterns), converting single string representations to lists of integers, locating the first occurence of a pattern withing a deck (match_pattern), and simulating an entire play-through of Penney's Game Between two patterns. 

Our first scoring method maintains all scoring results in memory using a pandas dataframe instead of relying on an external persistence layer. At initialization, the dataframe is seeded with every possible ordered pair of binary patterns, each row pre-allocated with counters for cards, tricks, and games played. As decks are streamed from disk in batches of numpy arrays, each one is converted into a python list for simulation with the shared play_through_deck function. The results from each match are then applied directly to the in-memory dataframe using update_aggregate_df, which updates the cumulative counts by locating the appropriate row and incrementing its fields. This approach was focused more on simplicity than efficiency. All intermediate results are kept in RAM, updates happen in-place without queries. 


## Approach 2: Temporary Database
Our second scoring method similarly processes the decks stored in the generated .npy files and computes the outcomes for every possible combination of a 3-card-selection. This approach utilizes the sqlite UPDATE command for each individual game. First, it extracts a deck and converts it to a python list of integers (0 sand 1s). Then, using the standard play_through_deck function, it does basic pattern matching for each possible combination. Finally, it looks through the database, updating the correct row with the corresponding statistics from the game. Then, it exports that data to a .csv file and deletes the temporary database for file size purposes. We wanted to try using a database again since it showed some surprising performance statistics during the deck generation stage. We also wanted to see what the benefits were of avoiding holding the data in memory.


## Testing
To test our code, we used 10-200 randomly selected decks (currently set at 200) to play each possible iteration of Penny’s Game. Eventually, we will track what files and decks have been used so there is absolutely no repetition, but we simply wanted to make sure our pipeline was working. It uses both approaches on the same sample, run’s the computations as specified in the above sections, and updates each .csv. It also keeps track of similar statistics we used during the generation phase for the purpose of comparing the two approaches. Specifically we look at how many decks were processed, peak memory, wall time (total elapsed time), and CPU time (time when CPU is actively executing instructions in the program). The csvs for are located in the /data/comparisons/ folder.


## Selection and Reasoning 
In the end, it seemed once again the database-based method outperformed the other approach. As seen in the performance table, the database approach took significantly less time and memory (as we predicted since the dataframe approach is based in memory). With the time disparity using only 200 decks, we certainly must prioritize time as we will get up to 2 million (or maybe even 10 million) decks. Both approaches’ numeric content is the same, showing they both are accurate and are interchangeable in surface functionality.


---

# Test Run Summary: 2025-10-03 15:11:45
## 📊 Performance Comparison
| approach                      |   wall_time_seconds |   cpu_time_seconds |   peak_memory_mb |   num_decks_processed |
|:------------------------------|--------------------:|-------------------:|-----------------:|----------------------:|
| Approach 1 (pandas_in_memory) |            7.35776  |           7.35165  |        0.0651217 |                   200 |
| Approach 2 (sqlite_temp_db)   |            0.740876 |           0.739652 |        0.0201111 |                   200 |

## Scores: Approach 1 (pandas_in_memory)
| p1   | p2   |   p1_cards |   p1_tricks |   p2_cards |   p2_tricks |   draw_cards |   draw_tricks |   games_count |
|:-----|:-----|-----------:|------------:|-----------:|------------:|-------------:|--------------:|--------------:|
| BBB  | BBR  |      50113 |        7434 |      50133 |        7790 |            0 |             0 |          2100 |
| BBB  | BRB  |      39495 |        6154 |      60737 |        9477 |            0 |             0 |          2100 |
| BBB  | BRR  |      39385 |        7434 |      63565 |       11451 |            0 |             0 |          2100 |
| BBB  | RBB  |       5220 |        1740 |      94793 |       13464 |            0 |             0 |          2100 |
| BBB  | RBR  |      42224 |        7434 |      60142 |       10587 |            0 |             0 |          2100 |
| BBB  | RRB  |      25257 |        5436 |      77647 |       13350 |            0 |             0 |          2100 |
| BBB  | RRR  |      50213 |        7434 |      49005 |        7377 |            0 |             0 |          2100 |
| BBR  | BBB  |      50133 |        7790 |      50113 |        7434 |            0 |             0 |          2100 |
| BBR  | BRB  |      72378 |       11996 |      30289 |        6093 |            0 |             0 |          2100 |
| BBR  | BRR  |      74038 |       13492 |      29782 |        6623 |            0 |             0 |          2100 |
| BBR  | RBB  |      15592 |        4093 |      85332 |       12624 |            0 |             0 |          2100 |
| BBR  | RBR  |      70828 |       13492 |      33621 |        7987 |            0 |             0 |          2100 |
| BBR  | RRB  |      52303 |       10823 |      52092 |       10723 |            0 |             0 |          2100 |
| BBR  | RRR  |      78044 |       13492 |      25074 |        5470 |            0 |             0 |          2100 |
| BRB  | BBB  |      60737 |        9477 |      39495 |        6154 |            0 |             0 |          2100 |
| BRB  | BBR  |      30289 |        6093 |      72378 |       11996 |            0 |             0 |          2100 |
| BRB  | BRR  |      52013 |       10696 |      52283 |       10757 |            0 |             0 |          2100 |
| BRB  | RBB  |      47293 |        8894 |      55031 |        9188 |            0 |             0 |          2100 |
| BRB  | RBR  |      50008 |        7604 |      49448 |        7503 |            0 |             0 |          2100 |
| BRB  | RRB  |      33980 |        8107 |      70237 |       13350 |            0 |             0 |          2100 |
| BRB  | RRR  |      60584 |       10696 |      41801 |        7377 |            0 |             0 |          2100 |
| BRR  | BBB  |      63565 |       11451 |      39385 |        7434 |            0 |             0 |          2100 |
| BRR  | BBR  |      29782 |        6623 |      74038 |       13492 |            0 |             0 |          2100 |
| BRR  | BRB  |      52283 |       10757 |      52013 |       10696 |            0 |             0 |          2100 |
| BRR  | RBB  |      51908 |       10751 |      52273 |       10792 |            0 |             0 |          2100 |
| BRR  | RBR  |      54914 |        9161 |      47576 |        8815 |            0 |             0 |          2100 |
| BRR  | RRB  |      85303 |       12537 |      15818 |        4161 |            0 |             0 |          2100 |
| BRR  | RRR  |      94931 |       13379 |       5319 |        1773 |            0 |             0 |          2100 |
| RBB  | BBB  |      94793 |       13464 |       5220 |        1740 |            0 |             0 |          2100 |
| RBB  | BBR  |      85332 |       12624 |      15592 |        4093 |            0 |             0 |          2100 |
| RBB  | BRB  |      55031 |        9188 |      47293 |        8894 |            0 |             0 |          2100 |
| RBB  | BRR  |      52273 |       10792 |      51908 |       10751 |            0 |             0 |          2100 |
| RBB  | RBR  |      52656 |       10868 |      51467 |       10587 |            0 |             0 |          2100 |
| RBB  | RRB  |      30104 |        6671 |      73572 |       13350 |            0 |             0 |          2100 |
| RBB  | RRR  |      63958 |       11548 |      38963 |        7377 |            0 |             0 |          2100 |
| RBR  | BBB  |      60142 |       10587 |      42224 |        7434 |            0 |             0 |          2100 |
| RBR  | BBR  |      33621 |        7987 |      70828 |       13492 |            0 |             0 |          2100 |
| RBR  | BRB  |      49448 |        7503 |      50008 |        7604 |            0 |             0 |          2100 |
| RBR  | BRR  |      47576 |        8815 |      54914 |        9161 |            0 |             0 |          2100 |
| RBR  | RBB  |      51467 |       10587 |      52656 |       10868 |            0 |             0 |          2100 |
| RBR  | RRB  |      30991 |        6107 |      71485 |       11834 |            0 |             0 |          2100 |
| RBR  | RRR  |      60877 |        9413 |      39486 |        6169 |            0 |             0 |          2100 |
| RRB  | BBB  |      77647 |       13350 |      25257 |        5436 |            0 |             0 |          2100 |
| RRB  | BBR  |      52092 |       10723 |      52303 |       10823 |            0 |             0 |          2100 |
| RRB  | BRB  |      70237 |       13350 |      33980 |        8107 |            0 |             0 |          2100 |
| RRB  | BRR  |      15818 |        4161 |      85303 |       12537 |            0 |             0 |          2100 |
| RRB  | RBB  |      73572 |       13350 |      30104 |        6671 |            0 |             0 |          2100 |
| RRB  | RBR  |      71485 |       11834 |      30991 |        6107 |            0 |             0 |          2100 |
| RRB  | RRR  |      49658 |        7754 |      50518 |        7377 |            0 |             0 |          2100 |
| RRR  | BBB  |      49005 |        7377 |      50213 |        7434 |            0 |             0 |          2100 |
| RRR  | BBR  |      25074 |        5470 |      78044 |       13492 |            0 |             0 |          2100 |
| RRR  | BRB  |      41801 |        7377 |      60584 |       10696 |            0 |             0 |          2100 |
| RRR  | BRR  |       5319 |        1773 |      94931 |       13379 |            0 |             0 |          2100 |
| RRR  | RBB  |      38963 |        7377 |      63958 |       11548 |            0 |             0 |          2100 |
| RRR  | RBR  |      39486 |        6169 |      60877 |        9413 |            0 |             0 |          2100 |
| RRR  | RRB  |      50518 |        7377 |      49658 |        7754 |            0 |             0 |          2100 |

## Scores: Approach 2 (sqlite_temp_db)
*Note: The numerical results here should be identical to Approach 1.*
| p1   | p2   |   p1_cards |   p1_tricks |   p2_cards |   p2_tricks |   draw_cards |   draw_tricks |   games_count |
|:-----|:-----|-----------:|------------:|-----------:|------------:|-------------:|--------------:|--------------:|
| BBB  | BBR  |      50113 |        7434 |      50133 |        7790 |            0 |             0 |          2100 |
| BBB  | BRB  |      39495 |        6154 |      60737 |        9477 |            0 |             0 |          2100 |
| BBB  | BRR  |      39385 |        7434 |      63565 |       11451 |            0 |             0 |          2100 |
| BBB  | RBB  |       5220 |        1740 |      94793 |       13464 |            0 |             0 |          2100 |
| BBB  | RBR  |      42224 |        7434 |      60142 |       10587 |            0 |             0 |          2100 |
| BBB  | RRB  |      25257 |        5436 |      77647 |       13350 |            0 |             0 |          2100 |
| BBB  | RRR  |      50213 |        7434 |      49005 |        7377 |            0 |             0 |          2100 |
| BBR  | BBB  |      50133 |        7790 |      50113 |        7434 |            0 |             0 |          2100 |
| BBR  | BRB  |      72378 |       11996 |      30289 |        6093 |            0 |             0 |          2100 |
| BBR  | BRR  |      74038 |       13492 |      29782 |        6623 |            0 |             0 |          2100 |
| BBR  | RBB  |      15592 |        4093 |      85332 |       12624 |            0 |             0 |          2100 |
| BBR  | RBR  |      70828 |       13492 |      33621 |        7987 |            0 |             0 |          2100 |
| BBR  | RRB  |      52303 |       10823 |      52092 |       10723 |            0 |             0 |          2100 |
| BBR  | RRR  |      78044 |       13492 |      25074 |        5470 |            0 |             0 |          2100 |
| BRB  | BBB  |      60737 |        9477 |      39495 |        6154 |            0 |             0 |          2100 |
| BRB  | BBR  |      30289 |        6093 |      72378 |       11996 |            0 |             0 |          2100 |
| BRB  | BRR  |      52013 |       10696 |      52283 |       10757 |            0 |             0 |          2100 |
| BRB  | RBB  |      47293 |        8894 |      55031 |        9188 |            0 |             0 |          2100 |
| BRB  | RBR  |      50008 |        7604 |      49448 |        7503 |            0 |             0 |          2100 |
| BRB  | RRB  |      33980 |        8107 |      70237 |       13350 |            0 |             0 |          2100 |
| BRB  | RRR  |      60584 |       10696 |      41801 |        7377 |            0 |             0 |          2100 |
| BRR  | BBB  |      63565 |       11451 |      39385 |        7434 |            0 |             0 |          2100 |
| BRR  | BBR  |      29782 |        6623 |      74038 |       13492 |            0 |             0 |          2100 |
| BRR  | BRB  |      52283 |       10757 |      52013 |       10696 |            0 |             0 |          2100 |
| BRR  | RBB  |      51908 |       10751 |      52273 |       10792 |            0 |             0 |          2100 |
| BRR  | RBR  |      54914 |        9161 |      47576 |        8815 |            0 |             0 |          2100 |
| BRR  | RRB  |      85303 |       12537 |      15818 |        4161 |            0 |             0 |          2100 |
| BRR  | RRR  |      94931 |       13379 |       5319 |        1773 |            0 |             0 |          2100 |
| RBB  | BBB  |      94793 |       13464 |       5220 |        1740 |            0 |             0 |          2100 |
| RBB  | BBR  |      85332 |       12624 |      15592 |        4093 |            0 |             0 |          2100 |
| RBB  | BRB  |      55031 |        9188 |      47293 |        8894 |            0 |             0 |          2100 |
| RBB  | BRR  |      52273 |       10792 |      51908 |       10751 |            0 |             0 |          2100 |
| RBB  | RBR  |      52656 |       10868 |      51467 |       10587 |            0 |             0 |          2100 |
| RBB  | RRB  |      30104 |        6671 |      73572 |       13350 |            0 |             0 |          2100 |
| RBB  | RRR  |      63958 |       11548 |      38963 |        7377 |            0 |             0 |          2100 |
| RBR  | BBB  |      60142 |       10587 |      42224 |        7434 |            0 |             0 |          2100 |
| RBR  | BBR  |      33621 |        7987 |      70828 |       13492 |            0 |             0 |          2100 |
| RBR  | BRB  |      49448 |        7503 |      50008 |        7604 |            0 |             0 |          2100 |
| RBR  | BRR  |      47576 |        8815 |      54914 |        9161 |            0 |             0 |          2100 |
| RBR  | RBB  |      51467 |       10587 |      52656 |       10868 |            0 |             0 |          2100 |
| RBR  | RRB  |      30991 |        6107 |      71485 |       11834 |            0 |             0 |          2100 |
| RBR  | RRR  |      60877 |        9413 |      39486 |        6169 |            0 |             0 |          2100 |
| RRB  | BBB  |      77647 |       13350 |      25257 |        5436 |            0 |             0 |          2100 |
| RRB  | BBR  |      52092 |       10723 |      52303 |       10823 |            0 |             0 |          2100 |
| RRB  | BRB  |      70237 |       13350 |      33980 |        8107 |            0 |             0 |          2100 |
| RRB  | BRR  |      15818 |        4161 |      85303 |       12537 |            0 |             0 |          2100 |
| RRB  | RBB  |      73572 |       13350 |      30104 |        6671 |            0 |             0 |          2100 |
| RRB  | RBR  |      71485 |       11834 |      30991 |        6107 |            0 |             0 |          2100 |
| RRB  | RRR  |      49658 |        7754 |      50518 |        7377 |            0 |             0 |          2100 |
| RRR  | BBB  |      49005 |        7377 |      50213 |        7434 |            0 |             0 |          2100 |
| RRR  | BBR  |      25074 |        5470 |      78044 |       13492 |            0 |             0 |          2100 |
| RRR  | BRB  |      41801 |        7377 |      60584 |       10696 |            0 |             0 |          2100 |
| RRR  | BRR  |       5319 |        1773 |      94931 |       13379 |            0 |             0 |          2100 |
| RRR  | RBB  |      38963 |        7377 |      63958 |       11548 |            0 |             0 |          2100 |
| RRR  | RBR  |      39486 |        6169 |      60877 |        9413 |            0 |             0 |          2100 |
| RRR  | RRB  |      50518 |        7377 |      49658 |        7754 |            0 |             0 |          2100 |
