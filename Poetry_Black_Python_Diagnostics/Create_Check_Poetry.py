def create_or_check_poetry_environment():
    try:
        result = subprocess.run(["poetry", "env", "use", "python3"], check=True, capture_output=True, text=True)
        print("Poetry environment is ready.")
    except subprocess.CalledProcessError:
        print("Failed to use or create the Poetry environment. Please check your Python installation or create an environment manually.")
