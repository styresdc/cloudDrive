from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

class TransferData():
    def __init__(self):
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
    def upload_file(self, file_from):
        file1 = self.drive.CreateFile({'title': file_from})
        file1.Upload()
