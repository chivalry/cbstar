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
        return "Comic File: " + (os.path.basename(self.file) if self.file != None
                else "empty")

    def open(self, file:str):
        """Set the file to the passed parameter"""
        self.file = file

    def save(self, file:str=None):
        """
        Save the file to the destination or a default location if it isn't provided.
        """
        pass

    def delete_page(self, page:int=1, in_place:bool=False):
        """Remove the indicated page from the archive and save it."""
        pass

    def set_attribute(self, name:str, value:str, in_place:bool=False):
        """Set the comic book archive attribute to the passed value."""
        pass

    def append_attribute(self, name:str, value:str, in_place:bool=False):
        """Append the passed value to the named attribute."""
        pass

    def page_count(self):
        """Return the number of pages in the file."""
        if self.file == None:
            raise ComicFile.FileNoneError()

        if not os.path.isfile(self.file):
            raise ComicFile.FileNotFoundError()

        with ZipFile(self.file) as zip:
            members = zip.namelist()
            pruned = self.prune_dirs(members)
            length = len(pruned)
            return length

    def prune_dirs(self, members:list) -> list:
        """Remove folder members if there are any."""
        pruned = [item for item in members if not item.endswith('/')]
        return pruned

    @property
    def file_type(self) -> FileType:
        file_types = {'.zip': self.FileType.zip,
                      '.cbz': self.FileType.zip,
                      '.rar': self.FileType.rar,
                      '.cbr': self.FileType.rar,
                      '.7z' : self.FileType.sevenz,
                      'cb7' : self.FileType.sevenz,
                      'ace' : self.FileType.ace,
                      'cba' : self.FileType.ace,
                      'tar' : self.FileType.tar,
                      'cbt' : self.FileType.tar,
        }
        return file_types.get(ext, self.FileType.none)

if __name__ == '__main__':
    comic = ComicFile()

    script_path = path.realpath(__file__)
    parent_dir = path.abspath(path.join(script_path, os.pardir))
    targ_dir = path.join(parent_dir, 'files')
    targ_file = path.join(targ_dir, '100 Bullets - Brian Azzarello.cbz' )

    comic.file = targ_file

    print(comic.page_count())
    print(comic.file_type)
    print(comic)
    print(repr(comic))
