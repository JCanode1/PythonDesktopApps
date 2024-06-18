import markdown
import tkinter as tk
from tkhtmlview import HTMLLabel
from tools import convert_to_HTML

text = "#Test string"
html = convert_to_HTML(text)

root = tk.Tk()

try:
    frame = HTMLLabel(root, html=f"<html><body>{html}</body></html>")
    print("HTMLLabel created.")
    frame.pack(fill="both", expand=True)
except Exception as e:
    print(f"Error creating or setting content in HTMLLabel: {e}")
    exit(1)
except:
    print("An unknown error occurred while creating or setting content in HTMLLabel.")
    exit(1)

try:
    root.mainloop()
    
except Exception as e:
    print(f"Error running Tkinter main loop: {e}")
    exit(1)
except:
    print("An unknown error occurred in the main loop.")
    exit(1)
