import dropbox
import os

class TransferData:
    def __init__(self):
        try:
            self.access_token = str(os.environ["DBTOKEN"])
        except KeyError:
            print "Please set the environment variable DBTOKEN"
            exit()

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)
