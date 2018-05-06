import dropbox
import os
import time
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
        try:
            with open(file_from, 'rb') as f:
                self.dbx.files_upload(f.read(), file_to,mode=dropbox.files.WriteMode('overwrite', None))
            if(file_from == "ledger.txt"):
                return
        except:
            pass
        os.remove(file_from)
    def download_file(self, file_from):
        """download file from Dropbox
        """
        self.dbx.files_download_to_file(file_from, "/" + file_from)
    def delete_file(self, file_from):
        """delete file from Dropbox
        """
        self.dbx.files_delete('/' + file_from)
