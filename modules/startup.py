import sys
try:
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