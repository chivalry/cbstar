from zipfile import ZipFile
import os
import sys
import struct
import tempfile

class ZipArchiver:
    """
    Zip implementation
    
    https://github.com/davide-romanini/comictagger/blob/master/comicapi/comicarchive.py
    """

    def __init__(self, path):
        self.path = path

    def get_comment(self):
        with ZipFile(self.path, 'r') as zip_file:
            return zip_file.comment

    def set_comment(self, comment):
        """
        This is a custom function for writing a comment to a zip file,
        since the built-in one doesn't seem to work on Windows and macOS.

        Fortunately, the zip comment is at the end of the file, and it's
        easy to manipulate.

        http://en.wikipedia.org/wiki/Zip_(file_format)#Structure
        """

        # Get file size.
        stat_info = os.stat(self.path)
        file_len = stat_info.st_size

        try:
            with open(self.path, 'r+b') as file_obj:
                # The starting position, relative to EOF.
                pos = -4

                found = False
                value = bytearray()

                # Walk backwards to find the "End of Central Directory" record.
                while (not found) and (-pos != file_len):
                    # Seek, relative to EOF.
                    file_obj.seek(pos, 2)
                    value = file_obj.read(4)

                    # Look for the end of central directory signature.
                    if bytearray(value) == bytearray([0x50, 0x4b, 0x05, 0x06]):
                        found = True
                    else:
                        pos -= 1

                if found:
                    # Now skip forward 20 bytes to the comment length word.
                    pos += 20
                    file_obj(pos, 2)

                    # Pack the length of the comment string
                    format = 'H' # one 2-byte integer
                    comment_len = struct.pack(format, len(comment))

                    # Write out thegth.
                    file_obj.write(comment_len)
                    file_obj.seek(pos + 2, 2)

                    # Write out the comment itself.
                    file_obj.write(comment)
                    file_obj.truncate()
                else:
                    raise Exception('Failed to write comment to zip file.')
        except:
            return False
        else:
            return True
    
    def read(self, arch_file):
        data = ''
        with ZipFile(self.path, 'r') as zip_file:
            try:
                data = zip_file.read(arch_file)
            except Exception as e:
                print('bad zipfile {}: {} :: {}'.format(e, self.path, arch_file),
                      file=sys.stderr)
                raise IOError
        return data

    def rebuild(self, exclude:list):
        """
        Zip helper function.

        This recompresses the zip archive, without the files in the exclude list.
        """

        with TemporaryFile(dir=os.path.dirname(self.path)) as tmp_file:
            with ZipFile(self.path, 'r') as zip_in:
                with ZipFile(tmp_file, 'w') as zip_out:
                    for item in zip_in.infolist():
                        buffer = zip_in.read(item.filename)
                        if item.filename not in exclude:
                            zip_out.writestr(item, buffer)
                    zip_out.comment = zip_in.comment
            os.remove(self.path)
            os.rename(temp_file, self.path)
            self.path = temp_file

    def remove_member(self, member):
        try:
            self.rebuild([member])
        except:
            return False
        else:
            return True
