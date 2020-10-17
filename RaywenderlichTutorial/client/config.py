import re
import os

# Config file location
# (It will be generated there if not found)
_path = "config.txt"

# Contents of the config file on generation
_default_content = """
######################################
## Configuration for the Boxes game ##
######################################

# A multiplier for the UI scale.
# This does not have to be a whole number.
scale = 1

# The port and ip address of the server.
ip = localhost
port = 8888
"""

# Only read from the config file once
loaded = False

# Default values
scale = 1
ip = "localhost"
port = 8888

def load():
    global loaded
    if loaded:
        return
    loaded = True
    reload()

def reload():
    global scale, ip, port
    
    if os.path.exists(_path) and os.path.isfile(_path):
        # If the file exists, try open it
        try:
            config = open(_path)
        except IOError as e:
            print("Error opening config file:")
            print(e)
            config = None
    else:
        # If it does not, try create it
        try:
            config = open(_path, "w+")
            config.write(_default_content)
        except IOError as e:
            print("Unable to create config file")
            print(e)
            config = None

    if config is not None:

        # The regex pattern for a single line
        pattern = re.compile(""
            + r"^\s*" # Allow whitespace before the line
            + r"([^\s#=]+)" # Property name
            + r"\s*=\s*" # Equals (allowing for whitespace)
            + r"([^\n#]+)" # Property value
            )

        properties = {}

        # Extract things that look like properties
        lines = config.readlines()
        for line in lines:
            match = pattern.match(line)
            if match is not None:
                properties[match.group(1)] = match.group(2)

        # This is v. important! Aside from the good 
        # practice in not holding onto the file after we're
        # done with it, it also ensures that any buffered
        # text is actually written.
        config.close()

        # Check properties that are actually used
        # Supply defaults if they cannot be read

        def parse(selector, key: str, properties: dict, default):
            try:
                return selector(properties[key])
            except:
                print(f"Failed to read \"{key}\" from config file")
                return default

        scale = parse(float, "scale", properties, scale)
        port = parse(int, "port", properties, port)
        ip = parse(str, "ip", properties, ip)

