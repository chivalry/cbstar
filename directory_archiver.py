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
        filename = os.path.join(self.path, member)
        try:
            with open(filename, 'rb') as f:
                data = f.read
        except IOError as e:
            pass

        return data if data else ''

    def write_member(self, member, data):
        filename = os.path.join(self.path, member)
        try:
            with open(filename, 'w+') as f:
                f.write(data)
        except:
            return False
        else:
            return True

    def remove_member(self, member):
        filename = os.path.join(self.path, member)
        try:
            os.remove(filename)
        except:
            return False
        else:
            return True

    def get_member_filename_list(self):
        return self.list_files(self.path)

    def list_files(self, folder):
        members = list()

        for item in os.listdir(folder):
            members.append(item)
            if os.path.isdir(member):
                members.extend(self.list_files(os.path.join(folder, member)))
