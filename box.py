#cloudDrive
#Dixon Styres

# Import two classes from the boxsdk module - Client and OAuth2
from boxsdk import Client, OAuth2
import traceback
import os

class TransferData():
    # Define client ID, client secret, and developer token.
    def __init__(self):
        self.CLIENT_ID = None
        self.CLIENT_SECRET = None
        self.ACCESS_TOKEN = None
        try:
            with open('box.cfg', 'r') as box_cfg:
                self.CLIENT_ID = box_cfg.readline().rstrip('\n')
                self.CLIENT_SECRET = box_cfg.readline().rstrip('\n')
                self.ACCESS_TOKEN = box_cfg.readline().rstrip('\n')
                # Create OAuth2 object.
                self.oauth2 = OAuth2(self.CLIENT_ID, self.CLIENT_SECRET, access_token=self.ACCESS_TOKEN)

                # Create the authenticated client
                self.client = Client(self.oauth2)
        except:
            print("box.cfg not found for boxsdk")
            print("please make an box.cfg file with CLIENT_ID,CLIENT_SECRET, and ACCESS_TOKEN on 3 lines.")
            traceback.print_exc()
            exit()
    def upload_file(self, file_from):
        """upload a file to Box
        """
        try:
            self.client.folder('0').upload(file_from, file_from, preflight_check=True)
        except:
            pass
        os.remove(file_from)
    def download_file(self, file_from):
        """download a file from Box
        """
        file_list = self.client.folder(folder_id='0').get_items(limit=100, offset=0)
        for file1 in file_list:
            if(file1['name'] == file_from):
                #print("downloaded from box")
                with open(file_from, 'wb') as open_file:
                    self.client.file(file1.id).download_to(open_file)
                    open_file.close()
    def delete_file(self, file_from):
        """delete file from box
        """
        file_list = self.client.folder(folder_id='0').get_items(limit=100, offset=0)
        for file1 in file_list:
            if(file1['name'] == file_from):
                self.client.file(file1.id).delete()
