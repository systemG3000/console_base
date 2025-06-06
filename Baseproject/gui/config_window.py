import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Checkbutton, OptionMenu, IntVar, BooleanVar
from config.config_manager import Config
from utils.window_geometry import apply_geometry_tracking

class ConfigWindow:
    def __init__(self, master):
        self.top = Toplevel(master)
        self.top.title("Configuration")
        self.config = Config()

        apply_geometry_tracking(self.top, self.config, key="config")

        # Frame for padding
        main_frame = tk.Frame(self.top, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Log file entry
        Label(main_frame, text="Log File Name:").grid(row=0, column=0, sticky="w")
        self.log_file_entry = Entry(main_frame, width=40)
        self.log_file_entry.insert(0, self.config.log_file_name)
        self.log_file_entry.grid(row=0, column=1, pady=5)

        # Log everything checkbox (legacy toggle)
        self.log_everything_var = BooleanVar(value=self.config.log_everything)
        Checkbutton(
            main_frame,
            text="Log all messages (legacy option)",
            variable=self.log_everything_var
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        # Log level dropdown
        Label(main_frame, text="Log Level (1=crit, 2=warn, 3=status):").grid(row=2, column=0, sticky="w")
        self.log_level_var = IntVar(value=self.config.log_level)
        OptionMenu(main_frame, self.log_level_var, 1, 2, 3).grid(row=2, column=1, sticky="w", pady=5)

        # Save button
        Button(main_frame, text="Save", command=self.save).grid(row=3, column=0, columnspan=2, pady=10)

    def save(self):
        self.config.log_file_name = self.log_file_entry.get()
        self.config.log_everything = self.log_everything_var.get()
        self.config.log_level = self.log_level_var.get()
        self.config.save()
        self.top.destroy()
