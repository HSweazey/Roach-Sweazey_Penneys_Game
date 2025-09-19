import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# This function remains the same
def generate_comparison_and_get_stats(db_csv_path, array_csv_path, figures_dir):
    """
    Reads CSVs, generates a 3-panel comparison graph, and returns summary stats.
    """
    print("\n--- Generating Comparison Report ---")
    try:
        db_df = pd.read_csv(db_csv_path)
        array_df = pd.read_csv(array_csv_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. Could not find performance CSV files.")
        return None, None

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 7))
    fig.suptitle('Performance Comparison: Database vs. Array Method', fontsize=16)

    # Plot 1: Execution Time
    ax1.plot(db_df['Iteration'], db_df['Execution Time (s)'], marker='o', linestyle='-', label='Database Method')
    ax1.plot(array_df['Iteration'], array_df['Execution Time (s)'], marker='x', linestyle='--', label='Array Method')
    ax1.set_title('Execution Time per Iteration')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Time (seconds)')
    ax1.legend()
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Plot 2: Memory Usage
    memory_data = [db_df['Peak Memory (MB)'], array_df['Peak Memory (MB)']]
    labels = ['Database Method', 'Array Method']
    bplot = ax2.boxplot(memory_data, patch_artist=True, labels=labels)
    ax2.set_title('Distribution of Peak Memory Usage')
    ax2.set_ylabel('Peak Memory (MB)')
    ax2.yaxis.grid(True, linestyle='--', linewidth=0.5)
    colors = ['lightblue', 'lightgreen']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    # Plot 3: CPU Usage
    ax3.plot(db_df['Iteration'], db_df['CPU Usage (%)'], marker='s', linestyle='-', color='purple', label='Database Method')
    ax3.plot(array_df['Iteration'], array_df['CPU Usage (%)'], marker='^', linestyle='--', color='orange', label='Array Method')
    ax3.set_title('CPU Usage per Iteration')
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('CPU Usage (%)')
    ax3.legend()
    ax3.grid(True, which='both', linestyle='--', linewidth=0.5)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    figure_filename = f"performance_comparison_{timestamp}.png"
    figure_output_path = os.path.join(figures_dir, figure_filename)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(figure_output_path)
    print(f"✅ Comparison graph saved to '{figure_output_path}'")

    return db_df.mean(), array_df.mean()


def update_markdown_report(db_stats, array_stats, total_iterations, decks_per_iteration, markdown_report_path):
    """
    Finds a marker in the markdown file and replaces the content after it with the new report.
    """
    if db_stats is None or array_stats is None:
        print("Skipping markdown update due to missing stats.")
        return

    summary_df = pd.DataFrame({
        'Metric': ['Execution Time (s)', 'Peak Memory (MB)', 'CPU Usage (%)'],
        'Database Method': [
            f"{db_stats['Execution Time (s)']:.2f}",
            f"{db_stats['Peak Memory (MB)']:.2f}",
            f"{db_stats['CPU Usage (%)']:.2f}"
        ],
        'Array Method': [
            f"{array_stats['Execution Time (s)']:.2f}",
            f"{array_stats['Peak Memory (MB)']:.2f}",
            f"{array_stats['CPU Usage (%)']:.2f}"
        ]
    }).set_index('Metric')

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Use a unique, non-empty marker
    report_marker = "Summary Table:"

    # Define the new report content, including the marker itself for future runs
    new_report_section = f"""{report_marker}
## Results from Most Recent Run ({timestamp})

The table below shows the **average results** from the most recent test. The test was conducted over **{total_iterations} iterations**, with **{decks_per_iteration:,} decks** generated per iteration. There are more detailed graphs in the figures folder.

{summary_df.to_markdown()}
"""
    
    try:
        # Read the original markdown file
        with open(markdown_report_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the position of our marker
        marker_position = content.find(report_marker)

        if marker_position != -1:
            # If marker exists, keep all content before it
            content_before_marker = content[:marker_position]
        else:
            # If no marker, keep the whole file and add a newline
            # The new section will be appended for the first time
            content_before_marker = content.strip() + "\n\n"

        # Combine the original content with the new, updated report
        final_content = content_before_marker + new_report_section

        # Write the new content back, overwriting the old file
        with open(markdown_report_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✅ Successfully updated report in '{markdown_report_path}'")
    except IOError as e:
        print(f"Error: Could not write to markdown file. {e}")