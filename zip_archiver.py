from zipfile import ZipFile

class ZipArchiver:
    """
    Zip implementation
    
    https://github.com/davide-romanini/comictagger/blob/master/comicapi/comicarchive.py
    """

    def __init__(self, path):
        self.path = path

    def get_archive_comment(self):
        with ZipFile(self.path, 'r') as zip_file:
            return zip_file.comment
