import os
import random

def count_files(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

def balance_directories():
    # Define directories
    dirs = {
        'up': 'images/up',
        'down': 'images/down',
        'neutral': 'images/neutral'
    }
    
    # Count files in each directory
    counts = {dir_name: count_files(path) for dir_name, path in dirs.items()}
    print("Initial counts:", counts)
    
    # Find minimum count
    min_count = min(counts.values())
    print(f"Target count per directory: {min_count}")
    
    # Balance each directory
    for dir_name, path in dirs.items():
        if counts[dir_name] > min_count:
            files = os.listdir(path)
            num_to_remove = counts[dir_name] - min_count
            print(f"Removing {num_to_remove} files from {dir_name}")
            
            # Randomly select files to remove
            files_to_remove = random.sample(files, num_to_remove)
            
            # Remove selected files
            for file in files_to_remove:
                os.remove(os.path.join(path, file))
    
    # Verify final counts
    final_counts = {dir_name: count_files(path) for dir_name, path in dirs.items()}
    print("Final counts:", final_counts)

if __name__ == "__main__":
    balance_directories()
