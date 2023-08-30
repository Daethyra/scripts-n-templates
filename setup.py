import os
import subprocess
import sys
import platform
import logging

logging.basicConfig(level=logging.INFO)

class SetupEnvironment:
    def __init__(self):
        self.venv_command = "venv\\Scripts\\activate" if platform.system() == "Windows" else "source venv/bin/activate"

    def install_poetry(self):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "poetry"])
            logging.info("Poetry installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install poetry: {e}")
            raise

    def run_poetry_commands(self):
        try:
            subprocess.check_call([sys.executable, "-m", "poetry", "install"])
            subprocess.check_call([sys.executable, "-m", "poetry", "shell"])
            logging.info("Poetry commands ran successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to run poetry commands: {e}")
            raise

    def create_and_activate_venv(self):
        try:
            subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
            subprocess.check_call([self.venv_command], shell=True)
            logging.info("Virtual environment created and activated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to create and activate virtual environment: {e}")
            raise

    def upgrade_pip_and_install_requirements(self):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"])
            logging.info("Pip upgraded and requirements installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to upgrade pip and install requirements: {e}")
            raise

    def setup(self):
        if os.path.isfile("pyproject.toml"):
            self.install_poetry()
            self.run_poetry_commands()
        else:
            self.create_and_activate_venv()
            self.upgrade_pip_and_install_requirements()

if __name__ == "__main__":
    setup_env = SetupEnvironment()
    try:
        setup_env.setup()
    except Exception as e:
        logging.error(f"An error occurred during setup: {e}")
