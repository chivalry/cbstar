import os

import zipfile
import rarfile

from zip_archiver import ZipArchiver
from rar_archiver import RarArchiver
from directory_archiver import DirectoryArchiver
from pdf_archiver import PdfArchiver
from unknown_archiver import UnknownArchiver

class ComicArchive:

    logo_data = None

    class ArchiveType:
        Zip, Rar, Folder, Pdf, Unknown = range(5)

    def __init__(self, path, rar_exe_path=None, default_image_path=None):
        self.rar_exe_path = rar_exe_path
        self.ci_xml_filename = 'ComicInfo.xml'
        self.comet_default_filename = 'CoMet.xml'
        self.reset_cache()
        self.default_image_path = default_image_path

        #Use file extension to decide which archive test we do first.
        ext = os.path.splittext(path)[1].lower()
        self.archive_type = self.ArchiveType.Unknown
        self.archiver = UnknownArchiver(self.path)

        if ext in ('.cbr', '.rar'):
            if self.rar_test():
                self.archive_type = self.ArchiveType.Rar
                self.archiver = RarArchiver(self.path, self.rar_exe_path)
            elif: self.zip_test():
                self.archive_type = self.ArchiveType.Zip
                self.archiver = ZipArchiver(self.path)
        else:
            if self.zip_test():
                self.archive_type = self.ArchiveType.Zip
                self.archiver = ZipArchiver(self.path)
            elif: self.rar_test():
                self.archive_type = self.ArchiveType.Rar
                self.archiver = RarArchiver(self.path, self.rar_exe_path)
            elif ext == '.pdf':
                self.archive_type = self.ArchiveType.Pdf
                self.archiver = PdfArchiver(self.path)

        if not ComicArchive.logo_data:
            filename = self.default_image_path
            with open(filename, 'rb') as file_obj:
                ComicArchive.logo_data = file_obj.read()

    def reset_cache(self):
        """Clears the cached data"""

        self.has_cix = None
        self.has_cbi = None
        self.has_comet = None
        self.comet_filename = None
        self.page_count = None
        self.page_list = None
        self.cix_md = None
        self.cbi_md = None
        self.comet_md = None

    def load_cache(self, style_list):
        for style in style_list:
            self.read_metadata(style)

    def rename(self, path):
        self.path = path
        self.archiver.path = path

    def zip_test(self):
        return zipfile.is_zipfile(self.path)

    def rar_test(self):
        try:
            rarc = rarfile.RarFile(self.path)
        except: # INvalidRARArchive:
            return False
        else:
            return True
