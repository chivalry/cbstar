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


    def __init__(self, file=None):
        """Initialization for the class."""
        self.file = file

    def __str__(self):
        """Return a sring representation of the object."""
        return 'string'

    def open(self, file):
        """Set the file to the passed parameter"""
        self.file = file

    def save(self, file=None):
        """
        Save the file to the destination or a default location if it isn't provided.
        """
        return

    def delete_page(self, page, in_place=False):
        """Remove the indicated page from the archive and save it."""
        return

    def set_attribute(self, name, value, in_place=False):
        """Set the comic book archive attribute to the passed value."""
        return

    def append_attribute(self, name, value, in_place=False):
        """Append the passed value to the named attribute."""
        return

    def page_count(self):
        """Return the number of pages in the file."""
        if self.file == None:
            return -1

        zip = ZipFile(self.file)
        members = zip.namelist()
        # Remove folder members if there are any.
        members = [item for item in members if not item.endswith('/')]
        return len(members)

    @property
    def file_type(self):
        if self.file == None:
            return self.FileType.none
        elif self.file.endswith('.zip') or self.file.endswith('.cbz'):
            return self.FileType.zip
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
