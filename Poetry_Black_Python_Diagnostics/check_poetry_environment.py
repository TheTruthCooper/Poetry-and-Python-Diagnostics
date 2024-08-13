import os
import subprocess
import sys

def check_poetry_environment():
    # Step 1: Check if Poetry is installed
    try:
        subprocess.run(["poetry", "--version"], check=True)
        print("Poetry is installed.")
    except subprocess.CalledProcessError:
        print("Poetry is not installed. Please install Poetry before running this script.")
        sys.exit(1)

    # Step 2: Check if Poetry environment is active
    try:
        result = subprocess.run(["poetry", "env", "info", "--path"], check=True, capture_output=True, text=True)
        env_path = result.stdout.strip()
        print(f"Poetry environment is active at: {env_path}")
    except subprocess.CalledProcessError:
        print("Poetry environment is not active. Please activate the environment using 'poetry shell' or create it with 'poetry install'.")
        sys.exit(1)

    return env_path

def check_black_installed():
    # Step 3: Verify that `black` is installed
    try:
        subprocess.run(["poetry", "run", "black", "--version"], check=True)
        print("Black is installed in the active environment.")
        return True
    except subprocess.CalledProcessError:
        print("Black is not installed in the active environment.")
        return False

def run_diagnostics(env_path):
    # Step 4: Rerun diagnostics to find and log issues
    diagnostics_output = os.path.join(env_path, "diagnostics_report.txt")
    try:
        print("Running diagnostics...")
        result = subprocess.run(["poetry", "run", "pip", "check"], check=False, capture_output=True, text=True)
        with open(diagnostics_output, "w") as report_file:
            report_file.write(result.stdout)
            report_file.write(result.stderr)
        print(f"Diagnostics completed. Report saved at: {diagnostics_output}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run diagnostics: {str(e)}")
        sys.exit(1)

def main():
    env_path = check_poetry_environment()
    
    if not check_black_installed():
        run_diagnostics(env_path)

if __name__ == "__main__":
    main()




