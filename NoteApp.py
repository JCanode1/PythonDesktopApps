import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style
from tools import add_note, load_notes, save_notes, delete_note

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Notes App")
    root.geometry("500x500")
    style = Style(theme='journal')
    style = ttk.Style()

    # Configure the tab font to be bold
    style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

    # Create the notebook to hold the notes
    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        pass

    # Load notes into the notebook
    notes = load_notes(notebook)

    # Add buttons to the main window
    new_button = ttk.Button(root, text="New Note", 
                            command=lambda: add_note(notebook, notes), style="info.TButton")
    new_button.pack(side=tk.LEFT, padx=10, pady=10)

    delete_button = ttk.Button(root, text="Delete", 
                            command=lambda: delete_note(notebook, notes), style="primary.TButton")
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    save_button = ttk.Button(root, text="Save", 
                            command=lambda: save_notes(notebook), style="secondary.TButton")
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
