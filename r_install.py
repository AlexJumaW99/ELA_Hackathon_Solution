import subprocess
import os

venv_activate_script = "pip install -r requirements.txt"


# Specify the Python file you want to run
python_script = "runner.py"

# Run the Python script within the virtual environment
subprocess.run(f'{venv_activate_script} && python {python_script}', shell=True)
