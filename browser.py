aimport subprocess
import sys
import platform
from pathlib import Path

def get_chrome_version():
    system = platform.system()

    try:
        if system == "Windows":
            # Common install locations
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in possible_paths:
                if Path(path).exists():
                    output = subprocess.check_output([path, "--version"], text=True)
                    return output.strip()
            return "Chrome not found in default locations."

        elif system == "Darwin":  # macOS
            path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if Path(path).exists():
                output = subprocess.check_output([path, "--version"], text=True)
                return output.strip()
            return "Chrome not found in default location."

        elif system == "Linux":
            # Try common Chrome binary names
            for chrome_cmd in ["google-chrome", "google-chrome-stable", "chromium-browser", "chrome"]:
                try:
                    output = subprocess.check_output([chrome_cmd, "--version"], text=True)
                    return output.strip()
                except FileNotFoundError:
                    continue
            return "Chrome not found in PATH."

        else:
            return f"Unsupported OS: {system}"

    except Exception as e:
        return f"Error: {e}"

print(get_chrome_version())

import subprocess
import platform
from pathlib import Path

def get_edge_version():
    system = platform.system()

    try:
        if system == "Windows":
            possible_paths = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ]
            for path in possible_paths:
                if Path(path).exists():
                    output = subprocess.check_output([path, "--version"], text=True)
                    return output.strip()
            return "Microsoft Edge not found in default locations."

        elif system == "Darwin":  # macOS
            path = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            if Path(path).exists():
                output = subprocess.check_output([path, "--version"], text=True)
                return output.strip()
            return "Microsoft Edge not found in default location."

        elif system == "Linux":
            for cmd in ["microsoft-edge", "microsoft-edge-stable"]:
                try:
                    output = subprocess.check_output([cmd, "--version"], text=True)
                    return output.strip()
                except FileNotFoundError:
                    continue
            return "Microsoft Edge not found in PATH."

        else:
            return f"Unsupported OS: {system}"

    except Exception as e:
        return f"Error: {e}"

print(get_edge_version())



