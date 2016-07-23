from zipfile import ZipFile
from enum import Enum
import os
from os import path

class ComicFile():
    """An object representing a comic book archive file"""

    class FileType(Enum):
        none = 0
        zip = 1
        rar = 2
        sevenz = 3
        ace = 4
        tar = 5

    class ComicFileError(Exception): pass
    class FileNotFoundError(OSError): pass
    class FileNoneError(TypeError): pass

    def __init__(self, file:str=None):
        """Initialization for the class."""
        self.file = file

    def __str__(self) -> str:
        """Return a sring representation of the object."""
        return 'string'

    def open(self, file:str):
        """Set the file to the passed parameter"""
        self.file = file

    def save(self, file:str=None):
        """
        Save the file to the destination or a default location if it isn't provided.
        """
        return

    def delete_page(self, page:int=1, in_place:bool=False):
        """Remove the indicated page from the archive and save it."""
        return

    def set_attribute(self, name:str, value:str, in_place:bool=False):
        """Set the comic book archive attribute to the passed value."""
        return

    def append_attribute(self, name:str, value:str, in_place:bool=False):
        """Append the passed value to the named attribute."""
        return

    def page_count(self):
        """Return the number of pages in the file."""
        if self.file == None:
            raise ComicFile.FileNoneError()

        if not os.path.isfile(self.file):
            raise ComicFile.FileNotFoundError()

        with ZipFile(self.file) as zip:
            members = zip.namelist()
            # Remove folder members if there are any.
            pruned = [item for item in members if not item.endswith('/')]
            return len(pruned)

    @property
    def file_type(self) -> FileType:
        if self.file == None:
            return self.FileType.none
        elif self.file.endswith(('.zip', '.cbz')):
            return self.FileType.zip
        elif self.file.endswith(('.rar', '.cbr')):
            return self.FileType.rar
        elif self.file.endswith(('.7z', '.cb7')):
            return self.FileType.sevenz
        elif self.file.endswith(('.ace', '.cba')):
            return self.FileType.ace
        elif self.file.endswith(('.tar', '.cbt')):
            return self.FileType.tar
        else:
            return None

if __name__ == '__main__':
    comic = ComicFile()

    script_path = path.realpath(__file__)
    parent_dir = path.abspath(path.join(script_path, os.pardir))
    targ_dir = path.join(parent_dir, 'files')
    targ_file = path.join(targ_dir, '100 Bullets - Brian Azzarello.cbz' )

    comic.file = targ_file

    print(comic.page_count())
    print(comic.file_type)
