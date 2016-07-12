from zipfile import ZipFile
from enum import Enum

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
        self.file_type = self.FileType.none
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

    def delete_page(self, page):
        """Remove the indicated page from the archive and save it."""
        return

    def set_attribute(self, name, value):
        """Set the comic book archive attribute to the passed value."""
        return

    def append_attribute(self, name, value):
        """Append the passed value to the named attribute."""
        return

comic = ComicFile()
print(comic.file_type)
