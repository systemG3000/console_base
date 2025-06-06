from tkinter import Frame, Label, Entry, Button, Canvas, scrolledtext, END, WORD
from gui.config_window import ConfigWindow
from config.config_manager import Config
from logic.command_parser import parse_input
from utils.message_handler import handle_message

class BaseApp:
    def __init__(self, root):
        self.root = root
        self.config = Config()  # Load singleton config instance
        self._setup_window()
        self._setup_top_frame()
        self._setup_log_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """
        When the window is closed:
        - Save the current geometry to config
        - Log the geometry (optionally, based on log level)
        - Destroy the window
        """
        geometry = self.root.geometry()
        self.config.window_geometry = geometry
        self.config.save()

        msg = f"Window geometry saved as {geometry}"
        handle_message(self.status_log, msg, level=3)  # Level 3 = info/debug

        self.root.destroy()

    def _setup_window(self):
        self.root.title("Base Application")
        self.root.geometry(self.config.window_geometry)  # Use saved geometry
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def _setup_top_frame(self):
        self.top_frame = Frame(self.root, padx=5, pady=5)
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.columnconfigure(1, weight=1)

        Label(self.top_frame, text="Command:").grid(row=0, column=0, sticky="w")
        self.entry = Entry(self.top_frame)
        self.entry.grid(row=0, column=1, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)

        Button(self.top_frame, text="Submit", command=self.submit_command).grid(row=0, column=2, padx=5)

        self.status_light = Canvas(self.top_frame, width=20, height=20)
        self.status_light.grid(row=0, column=3)
        self.set_status_light("gray")

        Button(self.top_frame, text="Config", command=self.open_config).grid(row=0, column=4, padx=5)

    def _setup_log_frame(self):
        self.log_frame = Frame(self.root)
        self.log_frame.grid(row=1, column=0, sticky="nsew")
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        self.status_log = scrolledtext.ScrolledText(self.log_frame, wrap=WORD, state='disabled')
        self.status_log.grid(row=0, column=0, sticky="nsew")

    def submit_command(self):
        text = self.entry.get().strip()
        self.entry.delete(0, END)

        response, status, level = parse_input(text)

        if response == "[CONFIG_WINDOW_TRIGGER]":
            self.open_config()
        else:
            handle_message(self.status_log, response, level=level)

        self.set_status_light(status)

    def set_status_light(self, color: str):
        self.status_light.delete("all")
        self.status_light.create_oval(2, 2, 18, 18, fill=color, outline='black')

    def open_config(self):
        """
        Save current geometry and open the Config GUI
        """
        self.config.window_geometry = self.root.geometry()
        self.config.save()
        ConfigWindow(self.root)

    def _on_enter(self, event):
        self.submit_command()
