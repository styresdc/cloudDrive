#cloudDrive
#Dixon Styres

import db
import os

filedict = {}
num_files = 0

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
            open("ledger.txt",'w').write(str(num_files) + ' ' + str(self.file_count) + ' ' + self.file_path)
    def uploader(self):
        dbUp = db.TransferData()
        for x in range(0,self.file_count):
            if(x == 0):
                dbUp.upload_file(self.file_path + str(x), '/' + self.file_path + str(x))
            elif(x == 1):
                return
            elif(x == 2):
                return
#rebuild file parts
class FileMake:
    def __init__(self, file_name, numbers):
        self.file_name = file_name
        self.numbers = numbers
    def build(self):
        with open(self.file_name + '_cloud.txt', 'w') as outfile:
            for x in range (0, self.numbers):
                    with open(self.file_name + str(x)) as infile:
                        outfile.write(infile.read())
#read ledger, create dict
class ledgerRead:
    def __init__(self):
        with open('ledger.txt', 'r') as f:
            for line in f:
                splitLine = line.split()
                filedict[int(splitLine[0])] = ",".join(splitLine[1:])
        num_files = len(filedict)
def main():
    try:
        ledgerRead()
    except:
        print("Unable to load ledger file, starting new")
    #print welcome @ selection
    #list file or upload file
    print("Welcome to cloudDrive....")
    while(True):
        print("Select '1' to upload , '2' to list files , '3' to donwnload, '4' to quit.")
        text = raw_input("Make a Selection ")
        if(text == '4'):
            print("Goodbye")
            quit()
        elif(text == '3'):
            #download file
            file_name = raw_input("Give Filename for download: ")
            fileBuild = FileMake(file_name, 3)
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
        elif(text == '1'):
            file_path = raw_input("Give Text filepath for upload: ")
            fileSplitter = FileSplit(file_path)
            try:
                fileSplitter.split()
                fileSplitter.ledgerWrite()
            except:
                print("Error Reading Source File")
            fileSplitter.uploader()
if __name__ == '__main__':
    main()
