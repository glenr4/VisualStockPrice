import os
import shutil
import random

def split_images(source_dir, target_dir, train_ratio=0.8):
    """
    Splits image data into training and testing sets with up, down, and neutral subfolders.

    Args:
        source_dir: The directory containing the original up, down, and neutral folders.
        target_dir: The directory where the train and test folders will be created.
        train_ratio: The proportion of data to use for training (default: 80%).
    """

    for category in ["up", "down", "neutral"]:
        source_category_dir = os.path.join(source_dir, category)
        if not os.path.exists(source_category_dir):
            print(f"Warning: Category '{category}' not found in source directory.")
            continue  # Skip to the next category if it's missing

        files = [f for f in os.listdir(source_category_dir) if os.path.isfile(os.path.join(source_category_dir, f))]
        random.shuffle(files)  # Shuffle files randomly

        num_train = int(len(files) * train_ratio)
        train_files = files[:num_train]
        test_files = files[num_train:]

        for split_name, split_files in [("train", train_files), ("test", test_files)]:
            target_split_dir = os.path.join(target_dir, split_name, category)
            os.makedirs(target_split_dir, exist_ok=True)  # Create directories if they don't exist

            for file_name in split_files:
                source_file_path = os.path.join(source_category_dir, file_name)
                target_file_path = os.path.join(target_split_dir, file_name)
                shutil.copy2(source_file_path, target_file_path) # Copy metadata as well

            print(f"Copied {len(split_files)} files to {target_split_dir}")


# Example usage:
source_directory = "images"  # Replace with the actual path to your data
target_directory = "images"  # Replace with where you want the split data

split_images(source_directory, target_directory)

print("Data splitting complete.")