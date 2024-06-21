import tkinter as tk
from tkinter import ttk
import json
from ttkbootstrap import Style
import markdown
from tkhtmlview import HTMLLabel  # Import HTMLLabel from tkhtmlview
from tools import add_note, load_notes, save_notes, delete_note, get_text, on_tab_modified
from logs import log
import os
import sys

# Global variable declaration
frame_status = 1
markdown_frame = None
root = None
notebook = None

def init_notes():
    # Determine the path to notes.json
    if hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        script_dir = sys._MEIPASS
    else:
        # Running in a normal Python environment
        script_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(script_dir, 'notes.json')

    # Check if notes.json exists
    if not os.path.exists(json_path):
        # If it does not exist, create the file and write an empty dictionary
        with open(json_path, 'w') as f:
            json.dump({}, f, indent=4)
        log(f"Created {json_path}")
    else:
        log(f"{json_path} already exists")

    return json_path


def on_text_modified(event, widget):
    # Handle the text modification event
    print("Text modified")
    # Reset the modified flag to continue detecting future changes
    widget.edit_modified(False)



def render_markdown_content():
    global notebook, markdown_frame
    
    if markdown_frame:
        # Clear previous content
        for widget in markdown_frame.winfo_children():
            widget.destroy()
        
        # Get current tab index and content
        
        try :
            selected_tab = notebook.select()
            
            tab_index = notebook.index(selected_tab)
            markdown_content = get_text(tab_index, notebook)
            
        except tk.TclError:
            log("Error: No tab selected")
            markdown_content = ""
        
        # Render Markdown to HTML
        try:
            html_content = markdown.markdown(markdown_content)
        except AttributeError:
            html_content = "<h1>Markdown Preview</h1><p>No content to preview</p>"
        
        # Update HTMLLabel with new content
        html_label = HTMLLabel(markdown_frame, html=html_content)
        html_label.pack(fill=tk.BOTH, expand=True)
        

def tab_event_handler(notebook, paned_window):
    on_tab_modified(notebook)
    show_markdown_frame(paned_window)

def show_markdown_frame(paned_window):
    global frame_status, markdown_frame, root, notebook
    
    
    if frame_status == 0:
        # Hide frame and resize window to 500x500
        paned_window.forget(markdown_frame)
        root.geometry("500x500")
        frame_status = 1
    else:
        if not markdown_frame:
            # Create markdown frame only once
            markdown_frame = ttk.Frame(paned_window, width=500, height=500)
            markdown_frame.pack_propagate(False)
            
        # Render markdown content whenever the frame is shown or tab changes
        render_markdown_content()
        
        # Add the markdown frame to the paned_window if it's not already added
        if not any(frame is markdown_frame for frame in paned_window.panes()):
            paned_window.add(markdown_frame, weight=1)
        
        # Resize window to 1000x500
        root.geometry("1000x500")
        frame_status = 0

def main(): 
    global root, notebook
    
    init_notes()

    
    root = tk.Tk()
    root.title("Notes App")
    root.geometry("500x500")  # Initial window size to accommodate only the left frame
    style = Style(theme='darkly')
    style = ttk.Style()

    # Configure the tab font to be bold
    style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

    # Create the PanedWindow to hold the frames
    paned_window = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Create the frame for the notes and buttons
    left_frame = ttk.Frame(paned_window, width=500, height=500)
    left_frame.pack_propagate(False)
    paned_window.add(left_frame, weight=1)

    # Create the notebook to hold the notes
    notebook = ttk.Notebook(left_frame, style="TNotebook")
    notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Bind the <<NotebookTabChanged>> event to render_markdown_content
    notebook.bind("<<NotebookTabChanged>>", lambda event: tab_event_handler(notebook, paned_window))

    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
    except FileNotFoundError:
        notes = []

    # Load notes into the notebook
    load_notes(notebook)

    # Add buttons to the left frame
    new_button = ttk.Button(left_frame, text="New Note", 
                            command=lambda: add_note(notebook, notes), style="success.TButton")
    new_button.pack(side=tk.LEFT, padx=10, pady=10)

    delete_button = ttk.Button(left_frame, text="Delete", 
                            command=lambda: delete_note(notebook, notes), style="danger.TButton")
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    save_button = ttk.Button(left_frame, text="Save", 
                            command=lambda: save_notes(notebook), style="light.TButton")
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    markdown_button = ttk.Button(left_frame, text="Markdown", 
                                command=lambda: show_markdown_frame(paned_window), style="info.TButton")
    markdown_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()


