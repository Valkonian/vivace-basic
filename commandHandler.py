from typing import Any
from constantData import commandWords, keywords, targetData, targetDataTypes, commonUrls
import sys
commandDictionary = {}

class ImportCmds():
    def __init__(self):
        self.commands = []
        self.file = open('commands.txt')
        for line in self.file: #for every line in the file
            self.commands.append(line.strip()) #append the stripped line to the commands list
        self.file.close() #close the file when done
        open("commands.txt", "w").close()
        print('[INFO] Target file (currently commands.txt) cleared') #clear the file when done as to not leave leftover commands that have already been retrieved
        if len(self.commands) == 0:
            self.passed = False
        else:
            self.passed = True

class ExportCmds():
    def __init__(self):
        #checking if command file is empty
        self.leftovers = []
        self.file = open('commands.txt')
        for line in self.file:
            self.leftovers.append(line.strip()) #Append to leftovers
        if len(self.leftovers) == 0: #if leftovers empty
            self.passed = True #passed requirements
        else: #if not
            self.passed = False #failed requirements
    
    def exportCommand(self, commands):
        self.file = open('commands.txt', 'w')
        self.toWrite = "\n".join(commands) #add new line to each command
        self.file.write(self.toWrite) #write
        self.file.close() #close

class InterpretCmds():
    def __init__(self, currentI): #make key for dictionary
        self.string = 'command' + str(currentI)
        self.command = commandDictionary[self.string] #input key into command dictionary
        self.cmdContents = self.command.split() #split command by word, storing each as a list

    def checkAgainstDicts(self):
        self.baseKW = self.cmdContents[0] #get basic key word, i.e. get or send
        print('[INFO] Base keyword:', self.baseKW)
        if self.baseKW in commandWords: 
            print('[INFO] Base keyword accepted.')
            if self.baseKW == 'get':
                self.cmdContents.pop(0)
                allCmds = Cmds(self.cmdContents)
        else:
            print('[ERROR] Base keyword not found. Exiting...')
            sys.exit()

class Cmds():

    def __init__(self, listIn):
        self.kwDict = {}
        self.extraInfo = {}
        for i in range(len(listIn)):
            if listIn[i] in keywords or listIn[i] in targetData or listIn[i] in targetDataTypes:
                self.kwDict.update({str(listIn[i]): i})
            else:
                self.extraInfo.update({str(listIn[i]): i})
        print('[INFO] Keyword Dictionary:', self.kwDict)
        print('[INFO] Extra Information Dictionary:', self.extraInfo)
        self.Get(self.kwDict, self.extraInfo)

    def Get(self, kwDict, extraInfo):
        self.flagSQL = False
        self.flagData = False
        if 'database' in kwDict or 'database' in extraInfo:
            self.flagSQL = True
            print('[INFO] ✓ Database')
        elif 'data' in kwDict or 'data' in extraInfo:
            self.flagData = True
            print('[INFO] ✓ Data')


    
take = ImportCmds()
give = ExportCmds()

if take.passed:
    print('[INFO] ImportCmds() passed.')
    if give.passed:
        print('[INFO] Target file (currently commands.txt) has been emptied correctly.')
        i = 0
        for index in take.commands:
            commandDictionary.update({'command' + str(i): index})
            i += 1
        # print(commandDictionary)
        interpret = InterpretCmds(0)
        interpret.checkAgainstDicts()
    else:
        print('[ERROR] Target file (currently commands.txt) is not empty.') #this will be handled in future.
else:
    print('[ERROR] Target file (currently commands.txt) is empty. Exiting...')
    sys.exit()