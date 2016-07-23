import unittest
from unittest import TestCase
from unittest.mock import Mock

import os
from zipfile import ZipFile

from comicfile import ComicFile

class TestPruneDirs(TestCase):

    def setUp(self):
        self.comic_file = ComicFile()
        self.dirs = ['/path/to/dir/', 'relative/path/to/dir/']
        self.files = ['/path/to/file', 'relative/path/to/file']

    def test_prune_dirs_returns_empty_when_passed_empty(self):
        self.assert_empty(self.comic_file.prune_dirs([]))

    def test_prune_dirs_returns_parameter_when_not_dirs(self):
        self.assertEqual(sorted(self.files),
                         sorted(self.comic_file.prune_dirs(self.files)))

    def test_prune_dirs_returns_empty_when_all_are_dirs(self):
        dirs = ['/path/to/dir/', 'relative/path/to/dir/']
        self.assert_empty(self.comic_file.prune_dirs(self.dirs))

    def test_prune_dirs_removes_dirs(self):
        members = self.dirs + self.files
        self.assertEqual(sorted(self.files),
                         sorted(self.comic_file.prune_dirs(members)))

    def assert_empty(self, list:list):
        self.assertEqual([], list)

class TestPageCount(TestCase):

    def setUp(self):
        self.comic_file = ComicFile()

    def test_page_count_raises_error_when_file_not_set(self):
        with self.assertRaises(ComicFile.FileNoneError):
            self.comic_file.page_count()

    def test_page_count_raises_error_when_file_missing(self):
        with self.assertRaises(ComicFile.FileNotFoundError):
            self.comic_file.file = '/file/does/not/exist.zip'
            self.comic_file.page_count()
        
    @unittest.skip('working on the right procedure for this one')
    def test_page_count_returns_file_count(self):
        script_path = os.path.realpath(__file__)
        parent_dir = os.path.abspath(os.path.join(script_path, os.pardir))
        targ_dir = os.path.join(parent_dir, 'files')
        targ_file = os.path.join(targ_dir, 'Archive.zip' )
        self.comic_file.file = targ_file

        # Store as tuples to use as dictionary keys.
        members_dict = {('dir/', 'dir/file1', 'dir/file2'):2,
                        ('file1.jpg', 'file2.jpg', 'file3.jpg'):3
        }
        for file_tuple, count in members_dict.items():
            test_zip_file = Mock(ZipFile)
            test_zip_file.namelist.return_value = list(file_tuple)
            self.assertEqual(count, self.comic_file.page_count())




