import markdown
import json
import tkinter as tk
from tkinter import ttk, messagebox
from logs import log


def convert_to_HTML(text):
    return markdown.markdown(text)


def add_note(notebook, notes):
    # Create a new tab for the note
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")
    
    # Create entry widgets for the title and content of the note
    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    
    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)
    
    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
    
    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)
    log("Note added")

    
    # Create a function to save the note
    def save_note():
        # Get the title and content of the note
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)
        
        # Add the note to the notes dictionary
        notes[title] = content.strip()
        
        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        
        # Add the note to the notebook
        note_content = tk.Text(notebook, width=40, height=10, font=("TkDefaultFont", 25))

        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)
        log("Note added")
    # Add a save button to the note frame
    save_button = ttk.Button(note_frame, text="Save", 
                            command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)
    

def load_notes(notebook):
    notes = {}
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
        num = 0
        for title, content in notes.items():
            # Add the note to the notebook
            note_content = tk.Text(notebook, width=40, height=10, font=("TkDefaultFont", 25))
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)
            
            note_content.bind("<<Modified>>", lambda event, widget=note_content: on_text_modified(event, widget))
        log("Notes loaded")

    except FileNotFoundError:
        # If the file does not exist, do nothing
        pass
    return notes

# Create a function to delete a note
def delete_note(notebook, notes):
    # Get the current tab index
    current_tab = notebook.index(notebook.select())
    
    # Get the title of the note to be deleted
    note_title = notebook.tab(current_tab, "text")
    
    # Show a confirmation dialog
    confirm = messagebox.askyesno("Delete Note", 
                                f"Are you sure you want to delete {note_title}?")
    
    if confirm:
        # Remove the note from the notebook
        notebook.forget(current_tab)
        
        # Remove the note from the notes dictionary
        notes.pop(note_title)
        
        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        log("Note deleted")


def save_notes(notebook):
    current_tab = notebook.index(notebook.select())
    note_title = notebook.tab(current_tab, option="text")
    
    # Get the content widget (should be a tk.Text widget)
    tab_id = notebook.select()
    content_widget = notebook.nametowidget(tab_id)
    
    if isinstance(content_widget, tk.Text):
        note_content = content_widget.get("1.0", tk.END)
        
        data = {}
    
        try:
            with open('notes.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            pass
    
        data[note_title] = note_content
    
        with open('notes.json', 'w') as file:
            json.dump(data, file, indent=4)
        
        log("Notes saved")
    else:
        log("Error: Content widget is not a tk.Text widget")

        
def get_text(tab_index, notebook):
    current_tab = notebook.index(notebook.select())

    content_widget = notebook.nametowidget(notebook.select())
    
    try:
        note_content = content_widget.get("1.0", tk.END)
        return note_content
    except AttributeError:
        log("Error: Content widget is not a tk.Text widget")
        return None

def on_text_modified(event, widget):
    # Handle the text modification event
    log("Text modified")
    
    widget.edit_modified(False)
    

def on_tab_modified(notebook):
    
    # Handle the tab modification event
    log("Tab modified")
    #save_notes(notebook)
    
    
