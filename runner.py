import subprocess
import os

# Set the path to your virtual environment's activate script
# venv_activate_script = "./env/scripts/activate"

# Specify the Python file you want to run
python_script = "Dashboard.py"

# Run the Python script within the virtual environment
subprocess.run(f'streamlit run "{python_script}"', shell=True)