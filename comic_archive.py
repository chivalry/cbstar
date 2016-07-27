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
