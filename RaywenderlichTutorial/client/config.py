import re
import os
import sys

# This currently isn't actually printed anywhere
_help_text = """
Command arguments that can be used with Boxes:

    --scale NUMBER
            Scale the GUI by an amount.

    --ip IP
            Specify an ip for joining. Defaults to localhost.
    
    --port PORT
            Specify a port for joining or hosting. Defaults to 8888.

    --host
            Host a server. If this flag is not present, the app will
            attempt to join instead.
"""

# Only read from the config file once
loaded = False

# Default values
scale = 1
ip = "localhost"
port = 8888
host = False

def load():
    global loaded
    if loaded:
        return
    loaded = True
    reload()

def reload():
    global scale, ip, port, host
    names = ["scale", "ip", "port", "host"]

    values = dict()
    next_is_key = False
    current_key = None

    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]

        if len(arg) > 2 and arg[0:2] == "--":
            param = arg[2:]
            if not param in names:
                print("Unrecognized parameter: '", param, "'")
            else:
                values[param] = None
                current_key = param

        elif current_key is not None:
            values[current_key] = arg.strip()

        else:
            print("Unexpected cmd line argument: '", arg, "'")

        scale = float(values.get("scale", scale))
        ip = values.get("ip", ip)
        port = int(values.get("port", port))
        host = "host" in values

    



