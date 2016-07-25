from unittest import TestCase
from unittest import skip
from unittest.mock import patch
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import os
import random

from comicfile import ComicFile

class TestComicFile(TestCase):

    # Store keys as tuples to use as dictionary keys.
    members_dict = {
        ('dir/', 'dir/file1', 'dir/file2'):['dir/file1', 'dir/file2'],
        ('file1.jpg', 'file2.jpg', 'file3.jpg'):['file1.jpg', 'file2.jpg', 'file3.jpg']
    }


    def setUp(self):
        self.comic_file = ComicFile()

    @patch('comicfile.ZipFile')
    def test_page_names(self, mock_zip_file):
        """
        `page_names` works successfully if it returns the results of
        `ZipFile.namelist` with members having trailing slashes removed.
        """

        self.prevent_file_none_error()

        for members, pages in self.members_dict.items():
            mock_zip_file.return_value.__enter__.return_value.namelist.return_value \
                    = list(members)
            self.assertEqual(sorted(pages), sorted(self.comic_file.page_names()))


    @patch('comicfile.ZipFile')
    def test_page_count(self, mock_zip_file):
        """
        `page_count` works successfully if, given the members returned by
        `ZipFile.namelist`, it returns the number of members that don't
        end in a slash.
        """

        self.prevent_file_none_error()

        for members, pages in self.members_dict.items():
            mock_zip_file.return_value.__enter__.return_value.namelist.return_value \
                    = list(members)
            self.assertEqual(len(pages), self.comic_file.page_count())

    def test_delete_page(self):
        """
        Success means that, if the page exists, the final file has one
        page less than the original and, where p is the page number, page
        p of the new file is equal to page p+1 of the original file.
        """

        with TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, 'test_delete_page.zip')
            with ZipFile(zip_path, mode='w', compression=ZIP_DEFLATED) as zip_file:
                for i in range(10):
                    file_name = ('0' + str(i))[:2]
                    with open(os.path.join(tmp_dir, file_name), 'w') as tmp_file:
                        tmp_file.write(file_name)
                        zip_file.write(tmp_file.name)

            self.comic_file.file_path = zip_path
            print(self.comic_file.file_path)
            print(self.comic_file.save_path)
            orig_count = self.comic_file.page_count()
            orig_pages = self.comic_file.page_names()

            self.comic_file.delete_page()
            new_count = self.comic_file.page_count()
            new_pages = self.comic_file.page_names()
            self.assertEqual(new_count, orig_count - 1)
            self.assertNotIn('01', new_pages)

            self.comic_file.delete_page(5)
            new_count = self.comic_file.page_count()
            new_pages = self.comic_file.page_names()
            self.assertEqual(new_count, orig_count - 2)
            self.assertNotIn('06', new_pages)

    def prevent_file_none_error(self):
        self.comic_file.file_path = __file__

    def print_info(self, archive_name):
        zf = ZipFile(archive_name)
        for info in zf.infolist():
            print(info.filename)
            print('\tComment:\t', info.comment)
            print('\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)')
            print('\tZIP version:\t', info.create_version)
            print('\tCompressed:\t', info.compress_size, 'bytes')
            print('\tUncompressed:\t', info.file_size, 'bytes')
            print()

