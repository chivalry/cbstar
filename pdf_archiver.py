class PdfArchiver:

    def __init__(self, path):
        self.path = path

    def get_comment(self):
        return ""

    def set_comment(self, comment):
        return False

    def read_member(self, page_num):
        return subprocess.check_output(
            ['mudraw', '-o', '-', self.path, str(int(os.path.basename(page_num)[:-4]))])

    def write_member(self, member, data):
        return False

    def remove_member(self, member):
        return False

    def get_member_filename_list(self):
        out = []
        pdf = PdfFileReader(open(self.path, 'rb'))
        for page in range(1, pdf.getNumPages() + 1):
            out.append("/%04d.jpg" % (page))
        return out
