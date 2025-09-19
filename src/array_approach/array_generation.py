import os
import time
import psutil
import argparse
import numpy as np
import random
import csv
from src.array_approach.array_helpers import generate_deck

def set_random_seed(seed: int = None) -> None:
    '''
    Sets random seed for reproducibility
    '''

    random.seed(seed)
    np.random.seed(seed)


def generate_n_decks(n: int, seed: int = None) -> np.ndarray:
    '''
    Generates n decks of cards as a numpy array
    shape should be (n, 52)
    '''

    rng = np.random.default_rng(seed)
    decks = []
    for _ in range(n):
        np.random.seed(rng.integers(0, 2**32 - 1))
        decks.append(generate_deck())
    return np.array(decks)


def save_decks(batch: np.ndarray, seed: int, output_dir: str) -> np.ndarray:
    '''
    Saves decks (from generate n decks) to .npy file
    filename format: 10000_decks_seed00001.npy ...
    '''

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f'decks_{batch.shape[0]}_seed{seed}.npy')

    if os.path.exists(filename):
        print(f"[INFO] Loading existing decks from {filename}")
        return np.load(filename)

    np.save(filename, batch)
    # print(f'saved {batch.shape[0]} decks to {filename}')
    return batch



def log_run(logfile: str, n_files: int, n_decks: int, runtime: float, space_mb: float):
    '''
    Track deck generations and storage space in a csv.
    '''
    file_exists = os.path.isfile(logfile)

    with open(logfile, 'a', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['num_files', 'decks_per', 'time_s', 'space_mb'])
        writer.writerow([n_files, n_decks, f'{runtime:.4f}', f'{space_mb:.4f}'])



def main(total_decks: int, batch_size: int, output_dir: str, log_file: str = "generation_log.csv"):
    print(f"[START] Generating {total_decks} decks...")
    start_time = time.time()

    rng = np.random.default_rng()
    total_saved = 0
    memory_used = 0
    n_files = 0

    # Calculate number of full batches and the remainder
    num_full_batches = total_decks // batch_size
    remainder_decks = total_decks % batch_size

    # Process full batches
    for _ in range(num_full_batches):
        seed = int(rng.integers(0, 2**32 - 1))
        batch = generate_n_decks(batch_size, seed)
        saved = save_decks(batch, seed, output_dir)

        total_saved += saved.shape[0]
        memory_used += saved.nbytes
        n_files += 1
    
    # Process the remainder if it exists
    if remainder_decks > 0:
        seed = int(rng.integers(0, 2**32 - 1))
        batch = generate_n_decks(remainder_decks, seed)
        saved = save_decks(batch, seed, output_dir)

        total_saved += saved.shape[0]
        memory_used += saved.nbytes
        n_files += 1


    elapsed = time.time() - start_time
    process = psutil.Process(os.getpid())
    rss_mb = process.memory_info().rss / (1024 ** 2)

    size_mb = memory_used / (1024**2)

    print("\n[SUMMARY]")
    print(f" Total decks generated: {total_saved}")
    print(f" Number of files: {n_files}")
    print(f" Runtime: {elapsed:.2f} seconds")
    print(f" Peak memory usage: {rss_mb:.2f} MB")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random decks.")
    parser.add_argument("--total_decks", type=int, default=2000000,
                        help="Total number of decks to generate")
    parser.add_argument("--batch_size", type=int, default=10000,
                        help="Number of decks per batch")
    parser.add_argument("--output_dir", type=str, default="./data/decks",
                        help="Directory to save generated decks")

    args = parser.parse_args()
    main(args.total_decks, args.batch_size, args.output_dir, args.log_file)