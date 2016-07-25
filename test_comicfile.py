from unittest import TestCase
from unittest.mock import patch

from comicfile import ComicFile

class TestComicFile(TestCase):

    def setUp(self):
        self.comic_file = ComicFile()

    @patch('comicfile.ZipFile')
    def test_page_count(self, mock_zip_file):
        """
        `page_count` works successfully if, given the members returned by
        `ZipFile.namelist`, it returns the number of members that don't
        end in a slash.
        """

        # Store as tuples to use as dictionary keys.
        members_dict = {('dir/', 'dir/file1', 'dir/file2'):2,
                        ('file1.jpg', 'file2.jpg', 'file3.jpg'):3
        }
        
        # Make the file point to something to prevent FileNoneError.
        self.comic_file.file_path = __file__

        for file_tuple, count in members_dict.items():
            mock_zip_file.return_value.__enter__.return_value.namelist.return_value \
                    = list(file_tuple)
            self.assertEqual(count, self.comic_file.page_count())
