"""
Word Frequency Counter using Multiprocessing

This script counts word frequencies in a text file using multiple processes for parallel processing.
It splits the input text into segments, processes each segment in parallel, and combines the results.
The final word frequencies are sorted by count (descending) and then alphabetically.
"""

from multiprocessing import Process, Manager
from collections import Counter
from tqdm import tqdm
import sys
import time

def read_file(file_path):
    """
    Read and return the contents of a file.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: Contents of the file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_text(text, num_segments):
    """
    Split the input text into roughly equal segments for parallel processing.
    
    Args:
        text (str): Input text to split
        num_segments (int): Number of segments to create
        
    Returns:
        list: List of word lists, each representing a segment
    """
    words = text.split()
    segment_size = len(words) // num_segments
    segments = []

    for i in range(num_segments):
        start = i * segment_size
        # For the last segment, include all remaining words
        end = None if i == num_segments - 1 else (i + 1) * segment_size
        segments.append(words[start:end])

    return segments

def count_words(segment, index, result_dict, progress_list):
    """
    Count word frequencies in a text segment and store results.
    
    Args:
        segment (list): List of words to count
        index (int): Index of the segment
        result_dict (dict): Shared dictionary to store results
        progress_list (list): Shared list to track progress
    """
    counter = Counter(segment)
    result_dict[index] = counter
    progress_list[index] = 1  # Mark this process as done
    print(f"Process-{index + 1} intermediate count:\n{dict(counter)}\n")

def show_progress(progress_list):
    """
    Display a progress bar showing the completion status of all segments.
    
    Args:
        progress_list (list): Shared list tracking progress of each segment
    """
    with tqdm(total=len(progress_list), desc="Processing segments") as pbar:
        previous_done = 0
        while True:
            done_now = sum(progress_list)
            # Exit when all segments are processed
            if done_now == len(progress_list):
                pbar.update(len(progress_list) - previous_done)
                break
            # Update progress bar when new segments complete
            if done_now > previous_done:
                pbar.update(done_now - previous_done)
                previous_done = done_now
            time.sleep(0.1)

def main(file_path, num_segments):
    """
    Main function to orchestrate the word frequency counting process.
    
    Args:
        file_path (str): Path to the input text file
        num_segments (int): Number of segments to split the text into
    """
    # Read and split the input text
    text = read_file(file_path)
    segments = split_text(text, num_segments)

    with Manager() as manager:
        # Create shared data structures for inter-process communication
        result_dict = manager.dict()  # Store word counts from each process
        progress_list = manager.list([0] * num_segments)  # Track progress
        processes = []

        # Create and start processes for each segment
        for i, segment in enumerate(segments):
            p = Process(target=count_words, args=(segment, i, result_dict, progress_list))
            processes.append(p)
            p.start()

        # Show progress while processes are running
        show_progress(progress_list)

        # Wait for all processes to complete
        for p in processes:
            p.join()

        # Combine results from all processes
        final_count = Counter()
        for counter in result_dict.values():
            final_count.update(counter)

        # Write results to output file, sorted by frequency (descending) and then alphabetically
        with open("output.txt", "w", encoding='utf-8') as f:
            f.write("Final consolidated word frequency:\n")
            for word, freq in sorted(final_count.items(), key=lambda x: (-x[1], x[0])):
                f.write(f"{word}: {freq}\n")

        print("\n✅ Final result saved to output.txt")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python word_freq_multiprocessing.py <file_path> <num_segments>")
    else:
        main(sys.argv[1], int(sys.argv[2]))
