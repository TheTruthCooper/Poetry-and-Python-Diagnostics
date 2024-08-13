# # STOP README FIRST!    <-------           *** THIS DIAGNOSTICS, ALBEIT SIMPLE, ASSUMES GENERAL WORKING KNOWLEDGE OF THE ## Requirements AND HOW THEY COMMUNICATE  
# Feel Free to e-mail questions/concerns and comments to andrewcooper19941994@gmail.com

# Poetry Environment and Black Validator

This script ensures that your Python environment is correctly configured using Poetry and verifies that the `black` code formatter is installed. If `black` is not installed, it reruns a diagnostic to identify any issues and logs them in a readable format.

## Requirements

- Python 3.7+
- Poetry
- Git

## Installation

1. Ensure that Python and Poetry are installed on your system.

2. Clone your repository and navigate to the project directory:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

3. Ensure Poetry dependencies are installed:

   ```bash
   poetry install
   ```

## Usage

1. Run the script:

   ```bash
   python validate_environment.py
   ```

2. The script will:

   - Check if Poetry is installed and an active environment is present.
   - Verify if `black` is installed in the environment.
   - If `black` is not found, it will run a diagnostics check and output the results to a `diagnostics_report.txt` file.

## Output

- If `black` is installed successfully, you will see confirmation messages in the terminal.
- If `black` is missing or there are issues, a detailed report will be saved as `diagnostics_report.txt` in the active environment's path.

## Contributing

Feel free to contribute to this project by submitting a pull request or opening an issue.

## License

This project is licensed under the MIT License.



#####      DEVELOPER NOTE FOR ADDITIONAL FUNCTIONALITY AND POSSIBLE GENERAL CONFLICTION AREAS AND A POTENTIAL FIX FOR EACH     #####

To ensure the script is robust and can handle potential issues effectively, you might consider adding or noting the following points:

1. Dependency Issues
Potential Issue: If there are conflicts or missing dependencies within the Poetry environment, the script might fail to install or validate black.
Plan: Consider adding a check to ensure all dependencies are up-to-date and compatible. This could be done by running poetry update or checking the output of poetry check.

def check_poetry_dependencies():
    try:
        subprocess.run(["poetry", "check"], check=True)
        print("All Poetry dependencies are correct.")
    except subprocess.CalledProcessError:
        print("There are issues with the dependencies. Consider running 'poetry update'.")


    ^  <----   This can be removed from the script entirely once you are extremely meticulous about ensuring your environment is up to date and in working order
                <!-- This in turn Encourages the user(s) to regularly run *poetry lock* and *poetry install* to sync their environment with the latest dependencies. -->


### Relevant Common Issues with Dependencies

EX 1.
. Poetry Dependency Issues
Error: Dependency Conflicts
Description: When running poetry install or poetry update, you might encounter dependency conflicts where two packages require incompatible versions of a third package.
Solution: Manually adjust the pyproject.toml file to resolve conflicts, possibly by specifying compatible versions or using the poetry update command with specific package names.


EX 2.
Error: Missing Dependencies
Description: After pulling changes from a git repository, poetry install may fail due to missing dependencies not listed in pyproject.toml.
Solution: Run poetry lock to update the lock file and ensure all necessary dependencies are correctly listed.






2. Poetry Environment Activation Issues
Potential Issue: Sometimes, the Poetry environment may not activate properly due to misconfigurations or if it's not created yet.
Plan: Add a check that automatically attempts to create the environment if it doesn't exist or prompts the user to manually intervene.
python
Copy code
def create_or_check_poetry_environment():
    try:
        result = subprocess.run(["poetry", "env", "use", "python3"], check=True, capture_output=True, text=True)
        print("Poetry environment is ready.")
    except subprocess.CalledProcessError:
        print("Failed to use or create the Poetry environment. Please check your Python installation or create an environment manually.")
Additional Note: Include instructions in the README about common Poetry setup issues, like Python version mismatches.


### Relevant Common Issues with Environment Activation

EX 1.
Poetry Environment Activation Issues
Error: Environment Not Activated
Description: If the Poetry environment isn't activated, commands like poetry run black will fail.
Solution: Run poetry shell to manually activate the environment or poetry install to create it if it doesn’t exist.

EX 2.
Error: Incorrect Python Version
Description: If the active environment uses a different Python version than expected, this could cause errors when installing or running packages.
Solution: Use poetry env use <python-version> to specify the correct Python version, ensuring it matches the version specified in pyproject.toml.




3. Handling Large Projects
Potential Issue: In large projects, black might take a long time to run or may fail if certain files are not formatted correctly.
Plan: Consider implementing a timeout for the black check and catching any black formatting errors, logging them for user review.

import time

def check_black_installed_with_timeout(timeout=60):
    try:
        start_time = time.time()
        subprocess.run(["poetry", "run", "black", "--version"], check=True, timeout=timeout)
        print("Black is installed in the active environment.")
        return True
    except subprocess.TimeoutExpired:
        print(f"Black check timed out after {timeout} seconds.")
        return False
    except subprocess.CalledProcessError:
        print("Black is not installed in the active environment.")
        return False

###  Common Relevant Issues Handling Large Projects

EX : 1
Error: Timeouts During black Execution
Description: In large projects, running black may take a long time, leading to timeouts.
Solution: Run black on specific files or directories, or increase the timeout duration in the script.

Ex : 2
Error: Memory Consumption
Description: black might consume a lot of memory on very large projects, causing system slowdowns or crashes.
Solution: Run black in smaller batches or on individual files to reduce memory usage.



4. Handling Diagnostic Output
Potential Issue: If diagnostics produce a large amount of output, it might be difficult to sift through the report.
Plan: Consider splitting the output into sections, highlighting critical errors or warnings, or using a more structured logging format (e.g., JSON) that could be parsed later.
python

import json

def run_diagnostics(env_path):
    diagnostics_output = os.path.join(env_path, "diagnostics_report.json")
    try:
        result = subprocess.run(["poetry", "run", "pip", "check"], check=False, capture_output=True, text=True)
        diagnostics = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
        with open(diagnostics_output, "w") as report_file:
            json.dump(diagnostics, report_file, indent=4)
        print(f"Diagnostics completed. Report saved at: {diagnostics_output}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run diagnostics: {str(e)}")
        sys.exit(1)


### Common Relevant Issues with Specific Diagnostic Reports

EX : 1
Handling Diagnostic Output
Error: Overwhelming Amount of Output
Description: The diagnostics report could be very lengthy and difficult to parse.
Solution: Structure the output using sections or convert the report to JSON format to allow easier parsing and filtering.

EX : 2
Error: Important Errors Buried in Logs
Description: Critical errors might be difficult to spot within a large diagnostics file.
Solution: Highlight critical errors or warnings in the report or provide a summary of key issues at the top of the diagnostics file.


5. Cross-Platform Compatibility
Potential Issue: The script might behave differently on Windows, macOS, or Linux due to differences in shell environments, file paths, and command-line tools.
Plan: Test the script on different operating systems or include platform-specific instructions. You could use os.name or platform.system() to adjust paths and commands dynamically.

import platform

def get_platform_info():
    system = platform.system()
    print(f"Running on: {system}")
    return system

### Common Relevant Cross-Platform Compatibility Issues

EX : 1
Cross-Platform Compatibility
Error: Different Command Behavior
Description: Commands that work on Unix-like systems (Linux/macOS) might not work on Windows due to differences in command-line tools.
Solution: Use platform-specific commands or tools and adjust paths and environment settings based on the operating system using os.name or platform.system().

EX : 2
Error: File Path Differences
Description: File paths may differ between operating systems, causing file not found errors.
Solution: Use os.path.join() to create OS-independent file paths or handle path differences based on the detected platform.





### FINAL COMMENTS

1.  Script Updates/Automated Script Updates: Encourage users to keep the script updated by pulling the latest version from the repository or subscribing to updates.

2.  Automated Testing: Consider adding automated tests to verify the script’s functionality across different environments and configurations.

By planning for these contingencies, the script will be more robust, user-friendly, and reliable in various environments and use cases.



Summary of Key Takeaways:

###     Dependency Conflicts: Common when multiple packages have incompatible requirements.
###     Environment Activation Issues: Happens when the correct Python version or the Poetry environment isn’t properly set up.
###     Large Project Handling: black may timeout or consume too much memory.
###     Diagnostic Output Management: Long and unstructured output might hide important errors.
###     Cross-Platform Compatibility: Command and file path differences between operating systems are common issues.
###     Addressing these potential problems ensures the script is more resilient and user-friendly across different environments and use cases.