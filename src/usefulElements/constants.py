from sys import platform as _platform

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

WINDOWS_NAME = "win32"
MACOS_X_NAME = "darwin"
LINUX_NAME = "linux"

# ------------------------ useful variables
exploitation_system = _platform
MAX_TIME = 10800 # 3 hours in seconds