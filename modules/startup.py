# Written by JohnnyJoPo -- https://github.com/JohnnyJoPo
# On behalf of: N/A (personal hobby project)
# June 30, 2021

# startup.py is opened from run.py and checks for the correct version of python (minimum 3.6.0)
# and checks if gui.py and msgBank.py are located in the modules folder
# If the check passes, it loads the GUI and the application runs

# Import Python Standard Library modules
import sys
try:
    # Import application modules
    import gui
    import msgBank
except Exception:
    print("Error importing modules.\nPlease check that the following modules are located in the same directory as startup:\n\n"\
        "-> gui\n" \
        "-> msgBank\n" \
        "Press Enter to exit")
    input()
    exit()
print("\nPython version " + str(sys.version) + "\n")
versionNum = float(sys.version[0:3])
if versionNum < 3.6:
    print("\nPython 3.6.0 or higher is needed to run this program.")
    print("Download the latest version from https://www.python.org/downloads/")
    print("Press Enter to exit")
    input()
else:
    print("Exam Practice\nVersion 1.0\n\nStarting up\n---")
    gui.start()