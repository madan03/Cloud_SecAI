import sys
from install.install_prowler import main as install_main
from prowler_cmd.run_prowler import run_prowler_check
from DataPre.data_pre import main as data_pre_main
from Anomaly_test.anomaly import main as anomaly_main
from Pre_analy.Pre_anal_ml import main as pre_anal_ml_main

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

        # Step 3: Run the data preprocessing
        print("Running data_pre.py...")
        data_pre_main()
        print("Data preprocessing completed.\n")

        # Step 4: Run the anomaly detection
        print("Running anomaly.py...")
        anomaly_main()
        print("Anomaly detection completed.\n")

        # Step 5: Run the machine learning analysis
        print("Running Pre_anal_ml.py...")
        pre_anal_ml_main()
        print("Machine learning analysis completed.\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)  # Exit the program with a non-zero status to indicate failure