import os
import platform
from rarfile import RarFile
from time import sleep

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

    def __del__(self):
        RarArchiver.devnull.close()

    def get_rar_obj(self):
        for tries in range(7):
            try:
                rarc = RarFile(self.path)
            except (OSError, IOError) as e:
                print('get_rar_obj(): [{}] {} attempt #{}'.format(e, self.path, tries),
                      file=os.stderr)
                time.sleep(1)
            else:
                return rar_obj
        return e
