from typing import Any
from dictionaries import commandWords, keywords, targetData, targetDataTypes
commandDictionary = {}

class ImportCmds():
    def __init__(self):
        self.commands = []
        self.file = open('commands.txt')
        for line in self.file: #for every line in the file
            self.commands.append(line.strip()) #append the stripped line to the commands list
        self.file.close() #close the file when done
        open("commands.txt", "w").close()
        print('Cleared') #clear the file when done as to not leave leftover commands that have already been retrieved

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
    def __init__(self):
        for i in range(len(commandDictionary)):
            self.string = 'command' + str(i) #make key for dictionary
            self.command = commandDictionary[self.string] #input key into command dictionary
            self.cmdContents = self.command.split() #split command by word, storing each as a list

    def checkAgainstDicts(self):
        try:
            self.baseKW = commandWords[self.cmdContents[0]] #get basic command word, i.e. get or send
            self.baseKWpassed = True 
        except KeyError:
            self.baseKWpassed = False
        if self.baseKWpassed:
            print('Passed,', self.baseKW)
        else:
            print('Failed.')
        

take = ImportCmds()
give = ExportCmds()

if give.passed:
    print('Yes')
    i = 0
    for index in take.commands:
        commandDictionary.update({'command' + str(i): index})
        i += 1
    # print(commandDictionary)
    interpret = InterpretCmds()
    interpret.checkAgainstDicts()
else:
    print('No')