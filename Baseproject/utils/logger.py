from datetime import datetime
from tkinter import END

def log_message(message, text_widget, filename=None, to_file=False):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}\n"

    text_widget.configure(state='normal')
    text_widget.insert(END, full_message)
    text_widget.configure(state='disabled')
    text_widget.see(END)

    if to_file and filename:
        with open(filename, "a") as f:
            f.write(full_message)
