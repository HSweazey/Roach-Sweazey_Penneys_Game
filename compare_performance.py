# --- Third-Party Imports ---
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# (rest of the file is unchanged)

def generate_comparison_graph(db_csv, array_csv, output_image_file):
    """
    Reads performance data from two CSV files, prints summary statistics,
    and generates a side-by-side visual comparison.
    """
    try:
        # Load the data from the CSV files into pandas DataFrames
        db_df = pd.read_csv(db_csv)
        array_df = pd.read_csv(array_csv)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure both CSV files are in the same directory.")
        return

    # --- 1. Print Summary Statistics to the Console ---
    print("--- Performance Summary ---")
    # Add CPU Usage to the summary printout
    print("\nDatabase Method (Averages):")
    print(db_df[['Execution Time (s)', 'Peak Memory (MB)', 'CPU Usage (%)']].mean())
    print("\nArray Method (Averages):")
    print(array_df[['Execution Time (s)', 'Peak Memory (MB)', 'CPU Usage (%)']].mean())
    print("\n" + "="*30)

    # --- 2. Create the Comparison Plots ---
    # Change subplot layout to 1 row, 3 columns
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 7))
    fig.suptitle('Performance Comparison: Database Method vs. Array Method', fontsize=16)

    # Plot 1: Execution Time Comparison (Line Plot)
    ax1.plot(db_df['Iteration'], db_df['Execution Time (s)'], marker='o', linestyle='-', label='Database Method')
    ax1.plot(array_df['Iteration'], array_df['Execution Time (s)'], marker='x', linestyle='--', label='Array Method')
    ax1.set_title('Execution Time per Iteration')
    ax1.set_xlabel('Iteration Number')
    ax1.set_ylabel('Time (seconds)')
    ax1.legend()
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Plot 2: Peak Memory Usage Comparison (Box Plot)
    memory_data = [db_df['Peak Memory (MB)'], array_df['Peak Memory (MB)']]
    labels = ['Database Method', 'Array Method']
    bplot = ax2.boxplot(memory_data, patch_artist=True, labels=labels)
    ax2.set_title('Distribution of Peak Memory Usage')
    ax2.set_ylabel('Peak Memory (MB)')
    ax2.yaxis.grid(True, linestyle='--', linewidth=0.5)
    colors = ['lightblue', 'lightgreen']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        
    # --- NEW PLOT ---
    # Plot 3: CPU Usage Comparison (Line Plot)
    ax3.plot(db_df['Iteration'], db_df['CPU Usage (%)'], marker='o', linestyle='-', color='purple', label='Database Method')
    ax3.plot(array_df['Iteration'], array_df['CPU Usage (%)'], marker='x', linestyle='--', color='orange', label='Array Method')
    ax3.set_title('CPU Usage per Iteration')
    ax3.set_xlabel('Iteration Number')
    ax3.set_ylabel('CPU Usage (%)')
    ax3.legend()
    ax3.grid(True, which='both', linestyle='--', linewidth=0.5)
    # --- END NEW PLOT ---

    # --- 3. Save and Show the Figure ---
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_image_file)
    print(f"✅ Comparison graph saved to '{output_image_file}'")


if __name__ == "__main__":
    # Define the names of your two CSV files
    db_stats_file = './data/comparisons/db_performance_stats.csv'
    array_stats_file = './data/comparisons/array_performance_stats.csv'
    output_filename = './figures/performance_comparison.png'

    generate_comparison_graph(db_stats_file, array_stats_file, output_filename)