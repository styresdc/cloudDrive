import dropbox
import os

class TransferData:
    def __init__(self):
        try:
            self.access_token = str(os.environ["DBTOKEN"])
        except KeyError:
            print "Please set the environment variable DBTOKEN"
            exit()
        self.dbx = dropbox.Dropbox(self.access_token)

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox
        """

        with open(file_from, 'rb') as f:
            self.dbx.files_upload(f.read(), file_to)
        os.remove(file_from)
    def download_file(self, file_from):
        """download file from Dropbox
        """
        self.dbx.files_download_to_file(file_from, '/' + file_from)
