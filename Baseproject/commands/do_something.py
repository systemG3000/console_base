def do_something_handler(args):
    # Your logic here
    return ("Did something successfully!", "green", 3)

def register_commands():
    return {
        "do_something": {
            "handler": do_something_handler,
            "description": "Performs a test action for demonstration"
        }
    }
