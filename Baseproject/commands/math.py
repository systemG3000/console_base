import math

def add(args):
    a, b = map(float, args)
    return a + b

def subtract(args):
    a, b = map(float, args)
    return a - b

def multiply(args):
    a, b = map(float, args)
    return a * b

def divide(args):
    a, b = map(float, args)
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def power(args):
    a, b = map(float, args)
    return a ** b

def sqrt(args):
    (a,) = map(float, args)
    if a < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(a)

def log(args):
    (a,) = map(float, args)
    if a <= 0:
        raise ValueError("Logarithm undefined for zero or negative values.")
    return math.log(a)

def abs_val(args):
    (a,) = map(float, args)
    return abs(a)

# Subcommand registry
math_subcommands = {
    "add":       {"func": add,      "args": 2, "desc": "Add two numbers"},
    "subtract":  {"func": subtract, "args": 2, "desc": "Subtract two numbers"},
    "multiply":  {"func": multiply, "args": 2, "desc": "Multiply two numbers"},
    "divide":    {"func": divide,   "args": 2, "desc": "Divide two numbers"},
    "power":     {"func": power,    "args": 2, "desc": "Raise first to the power of second"},
    "sqrt":      {"func": sqrt,     "args": 1, "desc": "Square root of number"},
    "log":       {"func": log,      "args": 1, "desc": "Natural logarithm"},
    "abs":       {"func": abs_val,  "args": 1, "desc": "Absolute value"},
}

# Main dispatcher
def math_handler(args):
    if not args:
        return (math_usage(), "yellow", 2)

    subcommand = args[0].lower()
    sub_args = args[1:]

    if subcommand == "help":
        return (math_usage(), "blue", 3)

    if subcommand in math_subcommands:
        spec = math_subcommands[subcommand]
        if len(sub_args) != spec["args"]:
            return (f"{subcommand} expects {spec['args']} arguments.\n\n" + math_usage(), "yellow", 2)
        try:
            result = spec["func"](sub_args)
            return (f"Result: {result}", "green", 3)
        except Exception as e:
            return (f"Error: {e}", "red", 1)
    else:
        return (f"Unknown math subcommand: {subcommand}\n\n" + math_usage(), "yellow", 2)

def math_usage():
    lines = ["Usage: math <subcommand> [args]", "Available subcommands:"]
    for name, meta in sorted(math_subcommands.items()):
        lines.append(f"  {name:<10} - {meta['desc']}")
    lines.append("Type 'math help' for this message.")
    return "\n".join(lines)

# Register command
def register_commands():
    return {
        "math": {
            "handler": math_handler,
            "description": "Math utility with subcommands like add, subtract, sqrt, etc."
        }
    }

