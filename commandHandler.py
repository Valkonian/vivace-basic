from typing import Any
from constantData import commandWords, keywords, targetData, targetDataTypes, commonUrls, dataResources
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
        Cmds(self.cmdContents, self.baseKW)
    else:
      print('[ERROR] Base keyword not found. Exiting...')
      sys.exit()

class Cmds():

  def __init__(self, listIn, baseKW):
    self.kwDict = {}
    self.extraInfo = {}
    for i in range(len(listIn)):
      if listIn[i] in keywords or listIn[i] in targetData or listIn[i] in targetDataTypes or listIn[i] in dataResources:
        self.kwDict.update({str(listIn[i]): i})
      else:
        self.extraInfo.update({str(listIn[i]): i})
    print('[INFO] Keyword Dictionary:', self.kwDict)
    print('[INFO] Extra Information Dictionary:', self.extraInfo)
    self.Get(self.kwDict, self.extraInfo)

  def Get(self, kwDict, extraInfo):
    self.trueCount = 0
    self.flagSQL = False
    self.flagLink = False
    self.flagFile = False
    if 'database' in kwDict or 'database' in extraInfo:
      self.flagSQL = True #handling database, therefore sql command
      self.trueCount += 1
      print('[INFO] ✓ Database')
    if 'link' in kwDict or 'link' in extraInfo:
      self.flagLink = True #handling data
      self.trueCount += 1
      print('[INFO] ✓ Data')
    if 'file' in kwDict or 'file' in extraInfo:
      self.flagFile = True #handling file
      self.trueCount += 1
      print('[INFO] ✓ File')
    # else:
    #   print('[ERROR] ✗ No datatype keyword found.') #no keyword found, will handle this later
    #   sys.exit()
    print(f'[INFO] trueCount = {self.trueCount}')
    if self.trueCount <= 1: #as long as only one data type has been given
      if self.flagSQL: #if database command,
        self.exInfValues = [ *extraInfo.values() ] #list of values
        self.exInfKeys = [ *extraInfo.keys() ] #list of keys
        if 'all' in kwDict: #if get all
          self.select = '*' #wildcard
        else:
          self.position = self.exInfValues.index(0) #else get field name
          self.select = str(self.exInfKeys[self.position]) 
        print(f'[INFO] select = {self.select}')
        if 'key' in kwDict: #if using key
          self.keyPos1 = kwDict['key'] + 1 #position of key, add 1 to get next word in command
          self.keyPos2 = kwDict['key'] + 2 #get next word in command again
          self.position1 = self.exInfValues.index(self.keyPos1)
          self.key1 = str(self.exInfKeys[self.position1])
          self.position2 = self.exInfValues.index(self.keyPos2)
          self.key2 = str(self.exInfKeys[self.position2]) #getting based on value & not key
          print(f'[INFO] keyPos1 = {self.keyPos1}, position1 = {self.position1}, key1 = {self.key1}, keyPos2 = {self.keyPos2}, position2 = {self.position2}, key2 = {self.key2}')
          self.where = self.key1 + ' = "' + self.key2 + '"' #create part of sql command following WHERE
          print(f'[INFO] where = {self.where}')
        if 'table' in extraInfo:
          self.tablePos = extraInfo['table'] + 1 #get table name (1 after keyword table)
          self.position = self.exInfValues.index(self.tablePos)
          self.table = str(self.exInfKeys[self.position])  #get based on value not key
          print(f'[INFO] table = {self.table}')
        self.sqlCmd = 'SELECT ' + self.select + ' FROM ' + self.table + ' WHERE ' + self.where #create full command
        print(f'[INFO] sql command = {self.sqlCmd}')
        return self.sqlCmd
        #pass to database handling file later

      elif self.flagFile:
        self.exInfValues = [ *extraInfo.values() ]
        self.exInfKeys = [ *extraInfo.keys() ]
        self.filePathValue = kwDict['file'] + 1
        self.fileNameValue = kwDict['file'] + 2
        self.position1 = self.exInfValues.index(self.filePathValue)
        self.position2 = self.exInfValues.index(self.fileNameValue)
        self.filePathKey = str(self.exInfKeys[self.position1])
        self.fileNameKey = str(self.exInfKeys[self.position2])
        print(f'[INFO] filePathValue = {self.filePathValue}, fileNameValue = {self.fileNameValue}, position1 = {self.position1}, position2 = {self.position2}, filePathKey = {self.filePathKey}, fileNameKey = {self.fileNameKey}')
        self.filePathFull = self.filePathKey + self.fileNameKey
        print(f'[INFO] filePathFull = {self.filePathFull}')
        return self.filePathFull
        #pass to file handler later

      if self.flagLink:
        pass
        
    else:
      print('[ERROR] Too many target data types given. Exiting...')
      sys.exit()
    

  
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
    take
else:
  print('[ERROR] Target file (currently commands.txt) is empty. Exiting...')
  sys.exit()