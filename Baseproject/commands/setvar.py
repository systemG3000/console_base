# commands/setvar.py

from utils.shared_state import state

def setvar_handler(args):
    if len(args) < 2:
        return ("Usage: setvar <name> <value>", "yellow", 2)

    key = args[0]
    value = " ".join(args[1:])
    try:
        # Try to convert to float if possible
        if '.' in value or value.isdigit():
            value = float(value) if '.' in value else int(value)
    except ValueError:
        pass  # leave as string

    state.set(key, value)
    return (f"Set variable '{key}' = {value}", "green", 3)

def register_commands():
    return {
        "setvar": {
            "handler": setvar_handler,
            "description": "Set a named variable for use elsewhere"
        }
    }
