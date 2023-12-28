import os
import platform

def get_operating_system():
    system = platform.system()
    
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        # Check for specific Linux distributions
        try:
            with open("/etc/os-release", "r") as os_release_file:
                lines = os_release_file.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        distro_id = line.split("=")[1].strip().lower()
                        if distro_id == "kali":
                            return "Kali Linux"
                        elif distro_id == "ubuntu":
                            return "Ubuntu"
        except FileNotFoundError:
            pass  # /etc/os-release file not found, treat it as generic Linux
        
        # Check for Termux
        if "termux" in os.environ.get("SHELL", "").lower():
            return "Termux"

    elif system == "Darwin":
        return "macOS"
    else:
        return "Unknown"

if __name__ == "__main__":
    print("Operating System:", get_operating_system())
