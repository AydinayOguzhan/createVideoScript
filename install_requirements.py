import subprocess
import sys

def install_requirements():
    try:
        # Check if pip is installed
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])

        # Install the libraries listed in requirements.txt
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        print("All libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Make sure you have pip installed and try again.")

if __name__ == "__main__":
    install_requirements()
