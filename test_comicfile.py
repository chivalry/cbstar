from unittest import TestCase
from unittest.mock import patch
from tempfile import TemporaryDirectory

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

        # Build a file with 10 "pages" to test.
        # First create the pages in a temporary directory.
        with TemporaryDirectory() as tmp_dir:
            pass

    def prevent_file_none_error(self):
        self.comic_file.file_path = __file__
