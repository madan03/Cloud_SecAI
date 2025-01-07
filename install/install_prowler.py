import os
import sys
import subprocess

def check_pip():
    """Check if pip is installed."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL)
        print("pip is already installed.")
        return True
    except subprocess.CalledProcessError:
        print("pip is not installed.")
        return False

def install_pip():
    """Installs pip if it is not found."""
    if sys.platform == "win32":
        # Use ensurepip on Windows to avoid manual download
        print("Installing pip on Windows using ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    elif sys.platform.startswith("linux"):
        print("Installing pip on Linux...")
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3-pip"])
    elif sys.platform == "darwin":
        print("Installing pip on macOS...")
        subprocess.check_call(["brew", "install", "python3"])
    print("pip installed successfully.")

def check_prowler():
    """Check if prowler is installed."""
    try:
        subprocess.check_call(["prowler", "-v"], stdout=subprocess.DEVNULL)
        print("Prowler is already installed.")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Prowler is not installed.")
        return False

def install_prowler():
    """Installs prowler using pip."""
    print("Installing Prowler...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "prowler"])
    print("Prowler installed successfully!")

def main():
    """Main function to check pip and install prowler based on OS."""
    print(f"Detected OS: {sys.platform}")

    # Check for pip and install if needed
    if not check_pip():
        install_pip()
        # Retry checking pip after installation
        if not check_pip():
            print("pip installation failed. Exiting.")
            sys.exit(1)

    # Check for prowler and install if needed
    if not check_prowler():
        install_prowler()
    
    # Confirm prowler installation
    check_prowler()

if __name__ == "__main__":
    main()