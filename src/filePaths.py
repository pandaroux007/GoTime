import os, sys
# ------------------------ create file's paths
# https://github.com/Nuitka/Nuitka/issues/1737#issuecomment-1224488673
# https://stackoverflow.com/questions/59427353/how-to-get-the-current-path-of-compiled-binary-from-python-using-nuitka
current_dir = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))

settings_file_path = os.path.join(os.path.dirname(current_dir), "dep", "settings.json")
log_file_path = os.path.join(os.path.dirname(current_dir), 'log', "error_log.csv")
app_icon_file_path = os.path.join(os.path.dirname(current_dir), 'dep', 'icon.ico')
time_end_sound_file_path = os.path.join(os.path.dirname(current_dir), 'sound', 'digital-clock-alarm.wav')
license_file_path = os.path.join(os.path.dirname(current_dir), "LICENSE.txt")
github_icon_file_path = os.path.join(os.path.dirname(current_dir), 'dep', 'github.png')

del os, sys