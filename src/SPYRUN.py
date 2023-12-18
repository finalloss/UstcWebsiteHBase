# execution_script.py
import subprocess

file_names = ["src/SPYCS.py", "src/SPYSDS.py", "src/SPYFINANCE.py","src/SPYCYBERSEC.py"
                , "src/SPYOIC.py", "src/SPYSSE.py", "src/SPYSIST.py", "src/SPYSZ.py"]

for file_name in file_names:
    subprocess.call(["python", file_name])
