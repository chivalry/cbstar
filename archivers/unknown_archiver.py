class UnknownArchiver:

    """Unknown implementation"""

    def __init__(self, path):
        self.path = path

    def get_comment(self):
        return ""

    def set_comment(self, comment):
        return False

    def read_member(self, member):
        return ""

    def write_member(self, member, data):
        return False

    def remove_member(self, member):
        return False

    def get_member_filename_list(self):
        return []
