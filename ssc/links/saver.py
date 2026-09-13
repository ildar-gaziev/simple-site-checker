import csv
import sys

def save_to_csv(results, filename):
    """
    Saves the list of results (link, code) to a CSV file.
    
    Args:
        results (list): A list of tuples containing (link, code).
        filename (str): The destination file path.
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['link', 'code'])
            writer.writerows(results)
    except OSError as e:
        print(f"Error saving results to '{filename}': {e}", file=sys.stderr)
