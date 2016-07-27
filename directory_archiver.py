class DirectoryArchiver:
    """
    Directory implementation
    
    https://github.com/davide-romanini/comictagger/blob/master/comicapi/comicarchive.py
    """

    def __init__(self, path):
        self.path = path
        self.comment_file_name = 'ComicTaggerFoldercomment.txt'

    def get_comment(self):
        return self.read_member(self.comment_file_name)

    def set_comment(self, comment):
        return self.write_member(self.comment_file_name, comment)

    def read_member(self, member):
        data = ''
        filename = os.path.join(self.path, member)
        try:
            with open(filename, 'rb') as f:
                data = f.read
        except IOError as e:
            pass

        return data
