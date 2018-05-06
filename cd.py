#cloudDrive
#Dixon Styres

import db
import gd
import box
import os
import traceback
from multiprocessing import Process
import time

filedict = {}
num_files = 0
dbUp = db.TransferData()
gdUp = gd.TransferData()
boxUp = box.TransferData()

"""read in a file and split/upload it to enable aggregation. only text files for now
Splits a file on "Spliting Text"
backup ability if selected
"""
class FileSplit:
    def __init__(self, file_path, back):
        self.file_path = file_path
        self.file_count = 0
        self.back = back
    def split(self):
        """split a file on "Splitting text" and make duplicates if redundant mode
        """
        if(self.back == 'y'):
            files = open(self.file_path,'r').read().split('Splitting Text')
            names = [self.file_path + str(num) for num in range(len(files))]
            for num,file in enumerate(files):
                open(names[num],'w').write(file)
                self.file_count += 1
            backNames = [self.file_path + str(num) + 'b' for num in range(len(files))]
            for num,file in enumerate(files):
                open(backNames[num],'w').write(file)
        else:
            files = open(self.file_path,'r').read().split('Splitting Text')
            names = [self.file_path + str(num) for num in range(len(files))]
            for num,file in enumerate(files):
                open(names[num],'w').write(file)
                self.file_count += 1
    def ledgerWrite(self):
            """append to the ledger when adding files, upload as well
            """
            if(self.back == 'y'):
                open("ledger.txt",'a').write(str(num_files) + ' ' + str(self.file_count) + ' ' + self.file_path + ' ' + "y" + '\n')
            else:
                open("ledger.txt",'a').write(str(num_files) + ' ' + str(self.file_count) + ' ' + self.file_path + ' ' + "n" + '\n')
            dbUp.upload_file("ledger.txt", '/ledger.txt')
    def uploader(self):
        j = 0
        a = []
        b = []
        for x in range(0,self.file_count):
            if(j == 0):
                a.append(Process(target = dbUp.upload_file, args = (self.file_path + str(x), '/' + self.file_path + str(x)),))
                a[x].start()
                j+=1
            elif(j == 1):
                a.append(Process(target = gdUp.upload_file, args = (self.file_path + str(x),)))
                a[x].start()
                j+=1
            elif(j == 2):
                a.append(Process(target = boxUp.upload_file, args = (self.file_path + str(x),)))
                a[x].start()
                j = 0
        if(self.back == 'y'):
            j = 0
            for x in range(0,self.file_count):
                if(j == 0):
                    b.append(Process(target = dbUp.upload_file, args = (self.file_path + str(x)+'b', '/'+self.file_path+str(x)+'b'),))
                    b[x].start()
                    j+=1
                elif(j == 1):
                    b.append(Process(target = gdUp.upload_file, args = (self.file_path + str(x)+'b',)))
                    b[x].start()
                    j+=1
                elif(j == 2):
                    b.append(Process(target = boxUp.upload_file, args = (self.file_path + str(x)+'b',)))
                    b[x].start()
                    j = 0
        global num_files
        num_files += 1
#rebuild file parts
class FileMake:
    def __init__(self, file_name, numbers, back):
        self.file_name = file_name
        self.numbers = int(numbers)
        self.back = back
        self.error = "no"
    def build(self):
        with open(self.file_name + '_cloud.txt', 'w') as outfile:
            for x in range (0, self.numbers):
                    if(self.error == "yes"):
                        with open(self.file_name + str(x) + 'b') as infile:
                            outfile.write(infile.read())
                            os.remove(self.file_name + str(x) + 'b')
                    else:
                        with open(self.file_name + str(x)) as infile:
                            outfile.write(infile.read())
                            os.remove(self.file_name + str(x))
    def download(self):
        j=0
        a = []
        for x in range(0, self.numbers):
            if(j == 0):
                a.append(Process(target = dbUp.download_file, args = (self.file_name + str(x),)))
                a[x].start()
                j+=1
            elif(j == 1):
                a.append(Process(target = gdUp.download_file, args = (self.file_name + str(x),)))
                a[x].start()
                j+=1
            elif(j == 2):
                a.append(Process(target = boxUp.download_file, args = (self.file_name + str(x),)))
                a[x].start()
                j=0
        for job in a:
            job.join()
        ##redundant backups
        for x in range(0, self.numbers):
            if(!(os.path.isfile(self.file_name + str(x))):
                self.error = "yes"
                j=0
                a = []
                for x in range(0, self.numbers):
                    if(j == 0):
                        a.append(Process(target = dbUp.download_file, args = (self.file_name + str(x) + 'b',)))
                        a[x].start()
                        j+=1
                    elif(j == 1):
                        a.append(Process(target = gdUp.download_file, args = (self.file_name + str(x) + 'b',)))
                        a[x].start()
                        j+=1
                    elif(j == 2):
                        a.append(Process(target = boxUp.download_file, args = (self.file_name + str(x)+ 'b',)))
                        a[x].start()
                        j=0
                for job in a:
                    job.join()
                return
    def delete(self):
        j=0
        a = []
        for x in range(0, self.numbers):
            if(j == 0):
                a.append(Process(target = dbUp.delete_file, args = (self.file_name + str(x),)))
                a[x].start()
                j+=1
            elif(j == 1):
                a.append(Process(target = gdUp.delete_file, args = (self.file_name + str(x),)))
                a[x].start()
                j+=1
            elif(j == 2):
                a.append(Process(target = boxUp.delete_file, args = (self.file_name + str(x),)))
                a[x].start()
                j=0
#read ledger, create dict
class ledgerRead:
    def __init__(self):
        with open('ledger.txt', 'r') as f:
            for line in f:
                splitLine = line.split()
                filedict[int(splitLine[0])] = ",".join(splitLine[1:])
        global num_files
        num_files = len(filedict)

def main():
    try:
        ledgerRead()
    except:
        try:
            print("Unable to load local ledger file, trying dropbox")
            dbUp.download_file("ledger.txt")
            ledgerRead()
        except:
            print("Unable to find ledger, starting new")
    #print welcome @ selection
    #list file or upload file
    print("Welcome to cloudDrive....")
    while(True):
        print("'1' to upload")
        print("'2' to list files")
        print("'3' to download")
        print("'4' to delete")
        print("'5' to quit")
        text = raw_input("Make a Selection ")
        if(text == '5'):
            print("Goodbye")
            quit()
        elif(text == '4'):
            #delete a file
            _=os.system("clear")
            try:
                ledgerRead()
                if(num_files == 0):
                    print("No Files in ledger")
                else:
                    print("Index, Number of parts, File Name, Redundant")
                    print(filedict)
            except:
                print("Error reading ledger file")
                traceback.print_exc()
            if(num_files > 0):
                file_num = raw_input("Give Index for deletion: ")
                file_name = filedict[int(file_num)].split(',')
                fileBuild = FileMake(file_name[1], file_name[0])
                fileBuild.delete()
                f = open("ledger.txt","r")
                lines = f.readlines()
                f.close()
                f = open("ledger.txt","w")
                for line in lines:
                    if line!=file_num + " " + file_name[0] + " " + file_name[1] + "\n":
                        f.write(line)
                f.close()
                global filedict
                filedict = {}
                ledgerRead()
                if(os.path.getsize("ledger.txt") > 0):
                    dbUp.upload_file("ledger.txt", '/ledger.txt')
                else:
                    dbUp.delete_file("ledger.txt")
        elif(text == '3'):
            #download file
            _=os.system("clear")
            try:
                ledgerRead()
                print("Index, Number of parts, File Name, Redundant")
                print(filedict)
                file_name = raw_input("Give Index for download: ")
                file_name = filedict[int(file_name)].split(',')
                fileBuild = FileMake(file_name[1], file_name[0], file_name[2])
                fileBuild.download()
                fileBuild.build()
            except:
                print("Error reading ledger file")
        elif(text == '2'):
            _=os.system("clear")
            try:
                ledgerRead()
                if(num_files == 0):
                    print("No Files in ledger")
                else:
                    print("Number of parts, File Name")
                    for x in range(0, num_files):
                        print(filedict[x])
            except:
                print("Error reading ledger file")
        elif(text == '1'):
            file_path = raw_input("Give Text filepath for upload: ")
            back = raw_input("Make redundant backups? (y/n): ")
            if(back != 'y' and back != 'n'):
                print("please select 'y' or 'n'")
            else:
                fileSplitter = FileSplit(file_path,back)
                try:
                    fileSplitter.split()
                    fileSplitter.ledgerWrite()
                    fileSplitter.uploader()
                    dele = raw_input("Upload complete, Delete local file? y/n ")
                    if(dele == "y"):
                        os.remove(self.file_path + str(x))
                    else:
                        print("File not deleted")
                except:
                    print("Error Reading Source File")
                    traceback.print_exc()
if __name__ == '__main__':
    main()
