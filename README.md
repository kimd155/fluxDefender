# FluxDefender
![logo](logo_flux_defender.png)
*FluxDefender is an advanced educational tool designed to demonstrate the process of temporarily disabling Windows Defender. It highlights how to manage system security configurations and is intended for learning and research purposes only.*

## How It Works:

`main.py`: The core controller script that initiates the process.

    First step -
    Decoding and applying a .reg file - Transforms a base64-encoded payload into a valid .reg file.
    Execution - Utilizes PowerRun.exe to execute the .reg file with TrustedInstaller/NT System privileges.

  
`PowerRun.exe`: Ensures the .reg file is applied with the highest system privileges to alter Defender settings. (Built by Sordum.org)

**This PowerRun.exe version has been packed with UPX to avoid most AV Detections!**

`ps1 Scripts`: Executes a PowerShell script that removes all files related to Security Center and Defender. 

`block.exe`: A C++ executable that implements WFP (Windows Filtering Platform) rules to block any Defender Agent network activity. (Source code provided in the repository.)

`watchdog.py`: Monitors the system to ensure no Defender-related files are reintroduced. Utilizes sdelete64.exe (Sysinternals) to remove any detected files.

### How To use:

    pip3 install -r requirments.txt
    python3 main.py 

<sup>Disclaimer: FluxDefender is provided solely for educational and research purposes. Unauthorized use or deployment of this tool can result in legal and ethical issues. Always ensure you have permission and comply with all relevant laws and regulations when using this tool.</sup>

