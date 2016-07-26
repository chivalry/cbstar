import os
import platform

class RarArchiver:
    """
    RAR implementation
    
    https://github.com/davide-romanini/comictagger/blob/master/comicapi/comicarchive.py
    """

    devnull = None

    def __init__(self, path, exe_path):
        self.path = path
        self.exe_path = exe_path

        RarArchiver.devnull = RarArchiver.devnull or open(os.devnull, 'w')

        # Windows only, keeps the cmd.exe from popping up.
        if platform.system() == 'Windows':
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        else:
            self.startupinfo = None
