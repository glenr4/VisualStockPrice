import tkinter as tk
from tkinter import filedialog

def browse_file(initialdir="/"):
    """Opens a file dialog for the user to select a file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        initialdir=initialdir,  
        title="Select a File",
        filetypes=(("all files", "*.*"), ("Text files", "*.txt"))  # Optional: Filter file types
    )

    if file_path:
        print("Selected file:", file_path)
    else:
        print("No file selected.")

    return file_path
