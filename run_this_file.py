import subprocess
import os

# Set the path to your virtual environment's activate script
venv_create_script = "py -m venv env"

# Specify the Python file you want to run
python_script = "venv_activate.py"
# Run the Python script within the virtual environment
subprocess.run(f'{venv_create_script} && python {python_script}', shell=True)
