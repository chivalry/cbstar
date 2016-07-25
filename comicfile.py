from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from enum import Enum
import os
from os import path
from tempfile import TemporaryDirectory
import shutil

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
    class PageOutOfRangeError(IndexError): pass

    def __init__(self, file_path:str, save_path:str=None):
        """Initialization for the class."""
        self.file_path = file_path
        self.save_path = save_path or file_path

    def __str__(self) -> str:
        """Return a sring representation of the object."""
        return os.path.basename(self.file_path) if self.file_path != None else "empty"

    @property
    def file_type(self) -> FileType:
        file_types = {'.zip': self.FileType.zip,
                      '.cbz': self.FileType.zip,
                      '.rar': self.FileType.rar,
                      '.cbr': self.FileType.rar,
                      '.7z' : self.FileType.sevenz,
                      '.cb7': self.FileType.sevenz,
                      '.ace': self.FileType.ace,
                      '.cba': self.FileType.ace,
                      '.tar': self.FileType.tar,
                      '.cbt': self.FileType.tar,
        }

        ext = os.path.splitext(self.file_path)
        return file_types.get(ext, self.FileType.none)

    def page_names(self):
        """Returns a list of the pages in the archive."""
        if not os.path.isfile(self.file_path):
            raise ComicFile.FileNotFoundError()

        with ZipFile(self.file_path) as zip:
            members = zip.namelist()
            pruned = [item for item in members if not item.endswith('/')]
            return pruned

    def page_count(self):
        """Return the number of pages in the file."""
        return len(self.page_names())

    def delete_page(self, page:int=1):
        """
        Remove the indicated page from the archive and save it. Page order is
        determined by case-insensitive sorting order.
        """

        # Loop through pages, writing each one to a new zip archive except the
        # page to delete, then write to the `save_path` location.
        base_name = os.path.basename(self.file_path)
        with ZipFile(self.file_path, 'r') as zip_in:
            with TemporaryDirectory() as tmpdir_path:
                tmp_zip_path = os.path.join(tmpdir_path, base_name)
                with ZipFile(tmp_zip_path, 'w', ZIP_DEFLATED) as zip_out:
                    i = 1
                    for page in zip_in.infolist():
                        buffer = zip_in.read(page.filename)
                        if i != page:
                            zip_out.writestr(page, buffer)
                        i += 1
        self.save_path = self.file_path if self.save_path == None else self.save_path
        shutil.copy(tmp_zip_path, self.save_path)
                        

    def set_attribute(self, name:str, value:str):
        """Set the comic book archive attribute to the passed value."""
        pass

    def append_attribute(self, name:str, value:str):
        """Append the passed value to the named attribute."""
        pass

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
