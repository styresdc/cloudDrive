#cloudDrive
#Dixon Styres

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

class TransferData():
    def __init__(self):
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
    def upload_file(self, file_from):
        file1 = self.drive.CreateFile({'title': file_from})
        file1.SetContentFile(file_from)
        file1.Upload()
    def download_file(self, file_from):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            file2 = self.drive.CreateFile({'id': file1['id']})
            if(file2['title'] == file_from):
                print("true")
                file2.GetContentFile(file_from) #download the file
