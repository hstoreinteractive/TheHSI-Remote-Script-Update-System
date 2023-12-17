# TheHSI Remote Script Update System

### The remote_update Package only works under Windows at the Moment
### The Update Script works on most common Platforms
### The path of to the program that should be updated should not contain spaces

## What is this?
This is a Python project for updating Python code on a remote Maschine

## How to Use
### Server (Windows):
 - Install git & python3:
   ```bat
   winget install -e Git.Git python3
   ```
 - Clone Repository:
   ```bat
   git clone https://github.com/hstoreinteractive/TheHSI-Remote-Script-Update-System.git
   cd HSI-Remote-Script-Update-System
   ```
 - Integrate it into your Script:
   ```python
   import remote_update
   
   remote_update.listen('password', __file__, True)
   ```
### Client (Windows):
 - Install git & python3:
   ```bat
   winget install -e Git.Git python3
   ```
 - Clone Repository:
   ```bat
   git clone https://github.com/hstoreinteractive/TheHSI-Remote-Script-Update-System.git
   cd HSI-Remote-Script-Update-System
   ```
 - Change the values in update.py:
   ```python
   HOST = "127.0.0.1"  # The server's hostname or IP address
   PORT = 6489  # The port used by the server ( Default: 6489 )
   FILE = "new_codebase.py" # File with updated code
   ```
 - Install all requirements:
   ```bat
   pip install -r requirements.txt
   ```
 - Run the update:
   ```bat
   python update.py
   ```
### Client (Linux):
 - Install git & python3:
   ```bash
   sudo apt install -y git python3 python3-pip
   ```
 - Clone Repository:
   ```bash
   git clone https://github.com/hstoreinteractive/TheHSI-Remote-Script-Update-System.git
   cd HSI-Remote-Script-Update-System
   ```
 - Change the values in update.py:
   ```python
   HOST = "127.0.0.1"  # The server's hostname or IP address
   PORT = 6489  # The port used by the server ( Default: 6489 )
   FILE = "new_codebase.py" # File with updated code
   ```
 - Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```
 - Run the update:
   ```bash
   python update.py
   ```
