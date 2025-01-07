import sys
from install.install_prowler import main as install_main
from prowler_cmd.run_prowler import run_prowler_check

if __name__ == "__main__":
    try:
        # Step 1: Run the installation
        print("Running install_prowler.py...")
        install_main()
        print("Installation completed.\n")

        # Step 2: Run the prowler check
        print("Running run_prowler.py...")
        run_prowler_check()
        print("Prowler check completed.\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)  # Exit the program with a non-zero status to indicate failure



