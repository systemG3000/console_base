# commands/getvar.py

from utils.shared_state import state

def getvar_handler(args):
    if not args:
        items = state.all()
        if not items:
            return ("No variables set.", "gray", 2)
        lines = [f"{k} = {v}" for k, v in items.items()]
        return ("\n".join(lines), "blue", 3)

    key = args[0]
    value = state.get(key, "[undefined]")
    return (f"{key} = {value}", "blue", 3)

def register_commands():
    return {
        "getvar": {
            "handler": getvar_handler,
            "description": "Get a variable or list all"
        }
    }
