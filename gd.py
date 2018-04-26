#cloudDrive
#Dixon Styres

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

class TransferData():
    def __init__(self):
        self.gauth = GoogleAuth()
        self.drive = GoogleDrive(self.gauth)
    def upload_file(self, file_from):
        """upload a file to drive
        """
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            file2 = self.drive.CreateFile({'id': file1['id']})
            if(file2['title'] == file_from):
                #print("downloaded from drive")
                file2.SetContentFile(file_from)
                file2.Upload()
                return
        file1 = self.drive.CreateFile({'title': file_from})
        file1.SetContentFile(file_from)
        file1.Upload()
        os.remove(file_from)
    def download_file(self, file_from):
        """download a file from drive
        """
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            file2 = self.drive.CreateFile({'id': file1['id']})
            if(file2['title'] == file_from):
                #print("downloaded from drive")
                file2.GetContentFile(file_from) #download the file
    def delete_file(self, file_from):
        """delete a file
        """
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            file2 = self.drive.CreateFile({'id': file1['id']})
            if(file2['title'] == file_from):
                file2.Delete() #delete the file
