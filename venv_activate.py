import subprocess
import os

venv_activate_script = "./env/scripts/activate"


# Specify the Python file you want to run
python_script = "r_install.py"

# Run the Python script within the virtual environment
subprocess.run(f'"{venv_activate_script}" && python {python_script}', shell=True)
