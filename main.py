import os
import subprocess
import time

def main():
    print("""
  ______ _            _____        __               _           
 |  ____| |          |  __ \      / _|             | |          
 | |__  | |_   ___  _| |  | | ___| |_ ___ _ __   __| | ___ _ __ 
 |  __| | | | | \ \/ / |  | |/ _ \  _/ _ \ '_ \ / _` |/ _ \ '__|
 | |    | | |_| |>  <| |__| |  __/ ||  __/ | | | (_| |  __/ |   
 |_|    |_|\__,_/_/\_\_____/ \___|_| \___|_| |_|\__,_|\___|_|   
 V1.0, Created by Kim Dvash, Educational Purposes only!                                                                                                                 
          """)
    print("Do you want to remove Windows Defender and its components?")
    print("After confirmation of removal, your device will RESTART!!")
    print("[Y] Yes, remove Windows Defender and proceed")
    print("[N] No, do nothing")
    
    choice = input("Choose an option: ").strip().lower()
    if choice == 'y':
        remove_defender()
    else:
        print("No action taken. Exiting...")
        return

def run_command(command):
    """Execute a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")

def remove_defender():
    print("Decoding Base64 Encoded Reg File...")
    reg_py_path = os.path.join("modules", "py", "reg_combiner.py")
    run_command(f'python "{reg_py_path}"')
    print("Running the Defender Remover PowerShell script...")
    powershell_script = os.path.join("modules", "ps1", "remover.ps1")
    run_command(f'powershell -noprofile -executionpolicy bypass -file "{powershell_script}"')
    print("Executing block.exe... - Implementing WFP Rules to block Defender network Activity...")
    block_exe_path = os.path.join("modules", "binaries", "block.exe")
    run_command(block_exe_path)
    print("Running Defender Files WatchDog.....")
    watchdog_py_path = os.path.join("modules", "py", "watchdog.py")
    run_command(f'python "{watchdog_py_path}"')
    print("Done!, do not close the watchdog!")

if __name__ == "__main__":
    main()