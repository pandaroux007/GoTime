import re, json, socket
import webbrowser
from urllib import request
from threading import Thread
from packaging import version
from typing import Callable
# ------------------------ app code files
from usefulElements import *
from appInfos import *

class SystemCheckUpdate():
    def __init__(self, master=None):
        # ------------------------ internal value(s)
        self._callback_end_check_update: Callable = None
        self._master = master

    # ------------------------ public methods
    def run_check_update(self) -> bool:
        try:
            Thread(target=self._process_check_update, daemon=True).start()
            return True
        except Exception:
            return False
    
    def set_callback_end_check_update(self, func: Callable = None):
        self._callback_end_check_update = func
    
    # ------------------------ private methods
    def _check_connection(self) -> bool:
        try:
            # ------------------------ check the access to github api
            socket.create_connection(("api.github.com", 443), timeout=1)
            return True
        except (socket.timeout, OSError): # no internet or api unavailable
            self._master.after(0, CTkPopup(master=self._master, title="GitHub is inaccessible", message="Unable to connect to GitHub to check update. Check your Internet connection and try again", icon=WARNING).get())
            return False
    
    def _get_data_api_github(self):
        # ------------------------ request to the github api to get the latest version
        url = "https://api.github.com/repos/" + app_author + "/" + app_name + "/releases/latest"
        with request.urlopen(url, timeout=3) as response:
            return json.loads(response.read().decode())
    
    def _trim_versions_str(self, str_current_version: str, str_new_version: str):
        self._local_version_app = re.sub(r"[^\d.]", "", str_current_version)
        self._new_version_app = re.sub(r"[^\d.]", "", str_new_version)

    def _compare_versions(self):
        # note : the 'version' module is missing on windows
        if version.parse(self._local_version_app) < version.parse(self._new_version_app):
            if self._master.after(0, CTkAskYesNo(master=self._master, title="Update available!",
                                                 message=f"A new version {self._new_version_app} of {app_name} is available!\n\nDo you want to install it?").get()):
                webbrowser.open_new(app_source_code_link + "/releases/latest")
        else:
            self._master.after(0, CTkPopup(master=self._master, title="No updates available",
                                           message=f"No new version of {app_name} is available at the moment!").get())

    def _process_check_update(self):
        if self._check_connection():
            data = self._get_data_api_github()
            latest_version_app_on_github = data['tag_name']
            self._trim_versions_str(app_version, latest_version_app_on_github)
            self._compare_versions()
        
        if self._callback_end_check_update is not None:
            self._callback_end_check_update()