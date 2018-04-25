#cloudDrive
#Dixon Styres

import db
import gd
import box
import os
import traceback
from multiprocessing import Process

filedict = {}
num_files = 0
dbUp = db.TransferData()
gdUp = gd.TransferData()
boxUp = box.TransferData()

#read in a file and split/upload it to enable aggregation. only text files for now
#Splits a file on "Split"
class FileSplit:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_count = 0
        self.service = 0
    def split(self):
        files = open(self.file_path,'r').read().split('Splitting Text')
        names = [self.file_path + str(num) for num in range(len(files))]
        for num,file in enumerate(files):
            open(names[num],'w').write(file)
            self.file_count += 1
    def ledgerWrite(self):
            open("ledger.txt",'a').write(str(num_files) + ' ' + str(self.file_count) + ' ' + self.file_path + '\n')
    def uploader(self):
        j = 0
        for x in range(0,self.file_count):
            if(j == 0):
                t1 = Process(target = dbUp.upload_file, args = (self.file_path + str(x), '/' + self.file_path + str(x)),)
                #dbUp.upload_file(self.file_path + str(x), '/' + self.file_path + str(x))
                t1.start()
                j+=1
            elif(j == 1):
                t2 = Process(target = gdUp.upload_file, args = (self.file_path + str(x),))
                #gdUp.upload_file(self.file_path + str(x))
                t2.start()
                j+=1
            elif(j == 2):
                t3 = Process(target = boxUp.upload_file, args = (self.file_path + str(x),))
                #boxUp.upload_file(self.file_path + str(x))
                t3.start()
                j = 0
        t1.join()
        t2.join()
        t3.join()
        global num_files
        num_files += 1
#rebuild file parts
class FileMake:
    def __init__(self, file_name, numbers):
        self.file_name = file_name
        self.numbers = int(numbers)
    def build(self):
        with open(self.file_name + '_cloud.txt', 'w') as outfile:
            for x in range (0, self.numbers):
                    with open(self.file_name + str(x)) as infile:
                        outfile.write(infile.read())
                        os.remove(self.file_name + str(x))
    def download(self):
        j=0
        for x in range(0, self.numbers):
            if(j == 0):
                t1 = Process(target = dbUp.download_file, args = (self.file_name + str(x),))
                #dbUp.download_file(self.file_name + str(x))
                t1.start()
                j+=1
            elif(j == 1):
                t2 = Process(target = gdUp.download_file, args = (self.file_name + str(x),))
                #gdUp.download_file(self.file_name + str(x))
                t2.start()
                j+=1
            elif(j == 2):
                t3 = Process(target = boxUp.download_file, args = (self.file_name + str(x),))
                #boxUp.download_file(self.file_name + str(x))
                t3.start()
                j=0
        t1.join()
        t2.join()
        t3.join()

#read ledger, create dict
class ledgerRead:
    def __init__(self):
        with open('ledger.txt', 'r') as f:
            for line in f:
                splitLine = line.split()
                filedict[int(splitLine[0])] = ",".join(splitLine[1:])
        self.num_files = len(filedict)

def main():
    try:
        ledgerRead()
    except:
        print("Unable to load ledger file, starting new")
        #traceback.print_exc()
    #print welcome @ selection
    #list file or upload file
    print("Welcome to cloudDrive....")
    while(True):
        print("Select '1' to upload , '2' to list files , '3' to download, '4' to quit.")
        text = raw_input("Make a Selection ")
        if(text == '4'):
            print("Goodbye")
            quit()
        elif(text == '3'):
            #download file
            _=os.system("clear")
            try:
                ledgerRead()
                print("Index, Number of parts, File Name")
                print(filedict)
            except:
                print("Error reading ledger file")
                traceback.print_exc()
            file_name = raw_input("Give Index for download: ")
            file_name = filedict[int(file_name)].split(',')
            fileBuild = FileMake(file_name[1], file_name[0])
            fileBuild.download()
            fileBuild.build()
        elif(text == '2'):
            _=os.system("clear")
            try:
                ledgerRead()
                print("Number of parts, File Name")
                if(num_files == 0):
                    print(filedict[0])
                    continue
                for x in range(0, num_files):
                    print(filedict[x])
            except:
                print("Error reading ledger file")
                traceback.print_exc()
        elif(text == '1'):
            file_path = raw_input("Give Text filepath for upload: ")
            fileSplitter = FileSplit(file_path)
            try:
                fileSplitter.split()
                fileSplitter.ledgerWrite()
                fileSplitter.uploader()
                dele = raw_input("Upload complete, Delete local file? y/n")
                if(dele == "y"):
                    os.remove(self.file_path + str(x))
                else:
                    print("File not deleted")
            except:
                print("Error Reading Source File")
                traceback.print_exc()
if __name__ == '__main__':
    main()
