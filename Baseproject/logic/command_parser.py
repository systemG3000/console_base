import os
import sys
import importlib.util
from config.config_manager import Config

# === Built-in command handlers ===

def handle_ping(args):
    return ("Pong!", "green", 3)

def handle_echo(args):
    return (" ".join(args), "green", 3)

def handle_config_command(args):
    return ("[CONFIG_WINDOW_TRIGGER]", "blue", 3)

# === Built-in command registry ===

builtin_commands = {
    "ping": {
        "handler": handle_ping,
        "description": "Responds with 'Pong!'"
    },
    "echo": {
        "handler": handle_echo,
        "description": "Echoes back your input"
    },
    "config": {
        "handler": handle_config_command,
        "description": "Opens the configuration window"
    }
}

# === Combined command registry ===

commands = dict(builtin_commands)

# === Auto-load all modules in commands/ folder ===

def load_command_modules():
    commands_dir = os.path.join(os.path.dirname(__file__), "..", "commands")
    sys.path.insert(0, commands_dir)

    for root, dirs, files in os.walk(commands_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                rel_path = os.path.relpath(os.path.join(root, file), commands_dir)
                module_name = rel_path[:-3].replace(os.path.sep, ".")
                full_path = os.path.join(commands_dir, rel_path)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, full_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "register_commands"):
                        mod_commands = mod.register_commands()
                        commands.update(mod_commands)
                except Exception as e:
                    print(f"Failed to load {module_name}: {e}")


# Load external command modules at import
load_command_modules()

# === Input parser ===

def parse_input(command: str):
    if not command.strip():
        return ("No input received.", "gray", 2)

    parts = command.strip().split()
    cmd = parts[0].lower()
    args = parts[1:]

    # === Global help ===
    if cmd in ("help", "?"):
        if not args:
            help_lines = ["Available commands:"]
            for name in sorted(commands.keys()):
                desc = commands[name].get("description", "No description")
                help_lines.append(f"  {name:10} - {desc}")
            return ("\n".join(help_lines), "blue", 3)
        else:
            sub_cmd = args[0].lower()
            if sub_cmd in commands:
                try:
                    # Attempt to call the command's handler with 'help'
                    handler = commands[sub_cmd]["handler"]
                    return handler(["help"])
                except Exception:
                    return (f"No detailed help available for '{sub_cmd}'.", "yellow", 2)
            else:
                return (f"Unknown command: '{sub_cmd}'", "red", 1)

    # === Regular command execution ===
    if cmd in commands:
        try:
            handler = commands[cmd]["handler"]
            return handler(args)
        except Exception as e:
            return (f"Error running '{cmd}': {e}", "red", 1)
    else:
        return (f"Unknown command: '{cmd}'", "red", 1)
