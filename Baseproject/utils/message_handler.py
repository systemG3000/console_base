from datetime import datetime
from config.config_manager import Config

def handle_message(text_widget, message: str, level: int = 3):
    """
    Display message in GUI, and log if message level <= config.log_level.
    """
    config = Config()
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} [L{level}] {message}\n"

    # Show in GUI
    text_widget.configure(state='normal')
    text_widget.insert("end", full_message)
    text_widget.configure(state='disabled')
    text_widget.see("end")

    # Log if level is high enough
    if level <= config.log_level:
        with open(config.log_file_name, "a") as f:
            f.write(full_message)
