from typing import Any
from constantData import commandWords, keywords, targetData, targetDataTypes, commonUrls, linkTypes
import sys
from colorama import Fore
from webscraper import scrape
commandDictionary = {}

class ImportCmds():
  def __init__(self):
    self.commands = []
    self.file = open('commands.txt')
    for line in self.file: #for every line in the file
      self.commands.append(line.strip()) #append the stripped line to the commands list
    self.file.close() #close the file when done
    open("commands.txt", "w").close()
    print(f'{Fore.BLUE}[INFO] ⓘ  Target file (currently commands.txt) cleared.{Fore.WHITE}') #clear the file when done as to not leave leftover commands that have already been retrieved
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
    print(f'{Fore.BLUE}[INFO] ⓘ  Base keyword: {self.baseKW}{Fore.WHITE}')
    if self.baseKW in commandWords: 
      print(f'{Fore.GREEN}[PASS] ✓ Base keyword accepted.{Fore.WHITE}')
      self.cmdContents.pop(0)
      Cmds(self.cmdContents, self.baseKW)
    else:
      print(f'{Fore.RED}[FAIL] ✗ Base keyword not found. Exiting...{Fore.WHITE}')
      sys.exit()

class Cmds():

  def __init__(self, listIn, baseKW):
    self.kwDict = {}
    self.extraInfo = {}
    for i in range(len(listIn)):
      if listIn[i] in keywords or listIn[i] in targetData or listIn[i] in targetDataTypes or listIn[i] in linkTypes:
        self.kwDict.update({str(listIn[i]): i})
      else:
        self.extraInfo.update({str(listIn[i]): i})
    print(f'{Fore.BLUE}[INFO] ⓘ  Keyword Dictionary: {self.kwDict}{Fore.WHITE}')
    print(f'{Fore.BLUE}[INFO] ⓘ  Extra Information Dictionary: {self.extraInfo}{Fore.WHITE}')
    if baseKW == 'get':
      self.Get(self.kwDict, self.extraInfo)

  def Get(self, kwDict, extraInfo):
    self.trueCount = 0
    self.flagSQL = False
    self.flagLink = False
    self.flagTypeLink = False
    self.flagFile = False
    if 'database' in kwDict or 'database' in extraInfo:
      self.flagSQL = True #handling database, therefore sql command
      self.trueCount += 1
      print(f'{Fore.GREEN}[PASS] ✓ Database{Fore.WHITE}')
    if 'link' in kwDict or 'link' in extraInfo:
      self.flagLink = True #handling data
      self.trueCount += 1
      print(f'{Fore.GREEN}[PASS] ✓ Link{Fore.WHITE}')
    if 'file' in kwDict or 'file' in extraInfo:
      self.flagFile = True #handling file
      self.trueCount += 1
      print(f'{Fore.GREEN}[PASS] ✓ File{Fore.WHITE}')
    else:
      for link in linkTypes:
        if link in kwDict or link in extraInfo:
          self.flagTypeLink = True
          self.trueCount += 1
          self.linkType = link
          print(f'{Fore.GREEN}[PASS] ✓ link, linkType = {self.linkType}{Fore.WHITE}')

    print(f'{Fore.BLUE}[INFO] ⓘ  trueCount = {self.trueCount}{Fore.WHITE}')
    if self.trueCount == 1: #as long as only one data type has been given
      if self.flagSQL: #if database command,
        self.exInfValues = [ *extraInfo.values() ] #list of values
        self.exInfKeys = [ *extraInfo.keys() ] #list of keys
        if 'all' in kwDict: #if get all
          self.select = '*' #wildcard
        else:
          self.position = self.exInfValues.index(0) #else get field name
          self.select = str(self.exInfKeys[self.position]) 
        print(f'{Fore.BLUE}[INFO] ⓘ  select = {self.select}{Fore.WHITE}')
        if 'key' in kwDict: #if using key
          self.keyPos1 = kwDict['key'] + 1 #position of key, add 1 to get next word in command
          self.keyPos2 = kwDict['key'] + 2 #get next word in command again
          self.position1 = self.exInfValues.index(self.keyPos1)
          self.key1 = str(self.exInfKeys[self.position1])
          self.position2 = self.exInfValues.index(self.keyPos2)
          self.key2 = str(self.exInfKeys[self.position2]) #getting based on value & not key
          print(f'{Fore.BLUE}[INFO] ⓘ  keyPos1 = {self.keyPos1}, position1 = {self.position1}, key1 = {self.key1}, keyPos2 = {self.keyPos2}, position2 = {self.position2}, key2 = {self.key2}{Fore.WHITE}')
          self.where = self.key1 + ' = "' + self.key2 + '"' #create part of sql command following WHERE
          print(f'{Fore.BLUE}[INFO] ⓘ  where = {self.where}{Fore.WHITE}')
        if 'table' in extraInfo:
          self.tablePos = extraInfo['table'] + 1 #get table name (1 after keyword table)
          self.position = self.exInfValues.index(self.tablePos)
          self.table = str(self.exInfKeys[self.position])  #get based on value not key
          print(f'{Fore.BLUE}[INFO] ⓘ  table = {self.table}{Fore.WHITE}')
        self.sqlCmd = 'SELECT ' + self.select + ' FROM ' + self.table + ' WHERE ' + self.where #create full command
        print(f'{Fore.BLUE}[INFO] ⓘ  sql command = {self.sqlCmd}{Fore.WHITE}')
        return self.sqlCmd, 'sql'
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
        print(f'{Fore.BLUE}[INFO] ⓘ  filePathValue = {self.filePathValue}, fileNameValue = {self.fileNameValue}, position1 = {self.position1}, position2 = {self.position2}, filePathKey = {self.filePathKey}, fileNameKey = {self.fileNameKey}{Fore.WHITE}')
        self.filePathFull = self.filePathKey + self.fileNameKey
        print(f'{Fore.BLUE}[INFO] ⓘ  filePathFull = {self.filePathFull}{Fore.WHITE}')
        return self.filePathFull, 'file'
        #pass to file handler later

      elif self.flagTypeLink:
        self.exInfValues = [ *extraInfo.values() ]
        self.exInfKeys = [ *extraInfo.keys() ]
        self.linkPosition = kwDict[self.linkType] + 1
        self.position = self.exInfValues.index(self.linkPosition)
        self.link = str(self.exInfKeys[self.position])
        print(f'{Fore.BLUE}[INFO] ⓘ  linkPosition = {self.linkPosition}, position = {self.position}, link = {self.link}{Fore.WHITE}')
        return self.link, 'link'
        #pass to webscraper later
      
      elif self.flagLink:
        self.kwDictValues = [ *kwDict.values() ]
        self.kwDictKeys = [ *kwDict.keys() ]
        self.linkKwPos = kwDict['link'] + 1
        self.position = self.kwDictValues.index(self.linkKwPos)
        self.kwLinkType = str(self.kwDictKeys[self.position])
        print(f'{Fore.BLUE}[INFO] ⓘ  linkKwPos = {self.linkKwPos}, position = {self.position}, kwLinkType = {self.kwLinkType}')
        return self.kwLinkType, 'linkType'
        #pass to webscraper later

    elif self.trueCount < 1:
      print(f'{Fore.RED}[FAIL] ✗ No  datatype keyword found. Exiting...{Fore.WHITE}')
      sys.exit()

    else:
      print(f'{Fore.RED}[FAIL] ✗ Too many target data types given. Exiting...{Fore.WHITE}')
      sys.exit()
    

  
take = ImportCmds()
give = ExportCmds()

if take.passed:
  print(f'{Fore.BLUE}[INFO] ⓘ  ImportCmds() passed.{Fore.WHITE}')
  if give.passed:
    print(f'{Fore.BLUE}[INFO] ⓘ  Target file (currently commands.txt) has been emptied correctly.{Fore.WHITE}')
    i = 0
    for index in take.commands:
      commandDictionary.update({'command' + str(i): index})
      i += 1
    print(f'{Fore.BLUE}[INFO] ⓘ  Command Dictionary = {commandDictionary}')
    j = 0
    for command in commandDictionary:
      interpret = InterpretCmds(j)
      interpret.checkAgainstDicts()
      j += 1
  else:
    print(f'{Fore.RED}[ERROR] ! Target file (currently commands.txt) is not empty.{Fore.WHITE}') #this will be handled in future.
    take
else:
  print(f'{Fore.RED}[ERROR] ! Target file (currently commands.txt) is empty. Exiting...{Fore.WHITE}')
  sys.exit()