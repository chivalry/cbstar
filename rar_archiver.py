import os
import platform
from rarfile import RarFile
from time import sleep
from tempfile import TemporaryFile, TemporaryFolder
import subprocess

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

    def get_comment(self):
        return self.get_rar_obj().comment

    def set_comment(self, comment):
        if not self.exe_path:
            return False

        try:
            # Write comment to temp file.
            with TemporaryFile() as tmp_file:
                tmp_file.write(comment)

                curr_dir = os.path.dirname(os.path.abspath(self.path))

                # Use external program to write comment to Rar archive.
                subprocess.call([self.exe_path,
                                 'c', '-w' + curr_dir, '-c-', '-z-' + tmp_file,
                                 self.path],
                                startupinfo=self.startupinfo,
                                stdout=RarArchiver.devnull)
                time.sleep(1) if platform.system() == 'Darwin'
        except:
            return False
        else:
            return True

    def read_member(self, member):
        entries = []

        rarc = self.get_rar_obj()
        for tries in range(7):
            try:
                data = rarc.open(member).read()
                entries = [(rarc.getinfo(member), data)]
                if entries[0][0].file_size != len(entries[0][1]):
                    msg = 'read_member(): [file is not expected size: ' +
                          '{} vs {}] {}:{} attempt #{}'
                    print(msg.format(entries[0][0].file_size,
                                     len(entries[0][1],)
                                     self.path,
                                     member
                                     tries),
                          file=os.stderr)
                    continue
                except Exception as e:
                    print('read_member(): [{}] {}:{} attempt #{}'.format(
                          e, self.path, member, tries), file=os.stderr)
                    time.sleep(1)
                else:
                    if len(entries) == 1:
                        return entries[0][1]
                    else:
                        raise IOError
    
    def write_member(self, member, data):
        if not self.exe_path:
            return False

        try:
            with TemporaryFile() as tmp_file:
                tmp_file.write(data)
                subprocess.call([self.exe_path,
                                 'a', '-w' + curr_dir, '-c-', '-ep',
                                 self.path, tmp_file],
                                startupinfo=self.startupinfo,
                                stdout=RarArchiver.devnull)
                time.sleep(1) if platform.system() == 'Darwin'
        except:
            return False
        else:
            return True

    def remove_member(self, member):
        if not self.exe_path:
            return False

        try:
            subprocess.call([self.exe_path,
                             'd', '-c-',
                             self.path, member],
                            startupinfo=self.startupinfo,
                            stdout=RarArchiver.devnull)
            time.sleep(1) if platform.system() == 'Darwin'
        except:
            return False
        else:
            return True

    def get_member_filename_list(self):
        rarc = self.get_rar_obj()
        for i in range(7):
            try:
                namelist = []
                for item in rarc.infolist():
                    if item.file_size != 0:
                        namelist.append(item.filename)
            except (OSError, IOError) as e:
                print('get_member_filename_list(): [{}] {} attempt #{}'.format(
                    e, self.path, tries), file=os.stderr)
                time.sleep(1)
            else:
                return namelist
        return e
