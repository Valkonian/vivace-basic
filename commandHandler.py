from typing import Any
from constantData import commandWords, keywords, targetData, targetDataTypes, commonUrls, linkTypes, extensions, dupeWords
import sys
from colorama import Fore
import json
from fileHandler import FileGet
from webscraper import Scraper
commandDictionary = {}

class ImportCmds():
  def __init__(self):
    self.commands = []
    self.file = open('commands.txt')
    for line in self.file: #for every line in the file
      self.commands.append(line.strip()) #append the stripped line to the commands list
    self.file.close() #close the file when done
    open("commands.txt", "w").close()
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Target file (currently commands.txt) cleared.{Fore.WHITE}') #clear the file when done as to not leave leftover commands that have already been retrieved
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
      # print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  command: {self.command}{Fore.WHITE}')
      self.cmdContents = self.command.split() #split command by word, storing each in a list

  def baseKWcheck(self):
    self.baseKW = self.cmdContents[0] #get basic key word, i.e. get or send
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Base keyword: {self.baseKW}{Fore.WHITE}')
    if self.baseKW in commandWords: #if valid base kw
      print(f'{Fore.LIGHTGREEN_EX}[PASS] ✓ Base keyword accepted.{Fore.WHITE}')
      self.cmdContents.pop(0) #remove base kw
      return self.cmdContents, self.baseKW
    else:
      print(f'{Fore.LIGHTRED_EX}[FAIL] ✗ Base keyword not found. Exiting...{Fore.WHITE}') #invalid base kw/no base kw found
      sys.exit()

class Cmds():

  def initial(self, listIn, baseKW):
    self.kwDict = {} #dictionary of keywords | format: {keyword: position in command}
    self.extraDict = {} #dictionary of extra info/context | format: {keyword: position in command}
    self.dupes = {} #dictionary for words likely to come up multiple times in a command, e.g. and, or for sql commands | format: {keyword: amount of times appeared}
    for i in range(len(listIn)):
      if listIn[i] in keywords or listIn[i] in targetData or listIn[i] in targetDataTypes or listIn[i] in linkTypes: #if in a keyword dictionary in constantData.py,
        self.keyIn = str(listIn[i]).replace('-', ' ') #replace - with spaces
        # print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  keyIn {self.keyIn}{Fore.WHITE}')
        self.kwDict.update({self.keyIn: i}) #add to kwDict with position in entire command
      elif listIn[i] in dupeWords:
        self.dupeIn = str(listIn[i]) 
        if self.dupeIn in self.dupes.keys(): #if the duplicate has already been recorded
          self.dupes[self.dupeIn] = self.dupes.get(self.dupeIn, 0) + 1 #increment the count of the word by one
        else: #if not already recorded
          self.dupes.update({self.dupeIn: 1}) #word recorded once.
      else:
        self.exIn = str(listIn[i]).replace('-', ' ') #replace - with spaces
        # print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  exIn {self.exIn}{Fore.WHITE}')
        self.extraDict.update({self.exIn: i}) #add to extraDict with position in entire command
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Keyword Dictionary: {self.kwDict}{Fore.WHITE}')
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Extra Information Dictionary: {self.extraDict}{Fore.WHITE}')
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Duplicates Dictionary: {self.dupes}{Fore.WHITE}')
    return baseKW, self.kwDict, self.extraDict, self.dupes #return for get function

  def Get(self, kwDict, extraDict, dupes): 
    self.trueCount = 0 #incase 1 or more data types are provided 
    self.flagSQL = False
    self.flagLink = False
    self.flagTypeLink = False
    self.flagFile = False
    if 'database' in kwDict or 'database' in extraDict or 'database' in dupes:
      self.flagSQL = True #handling database, therefore sql command
      self.trueCount += 1
      print(f'{Fore.LIGHTGREEN_EX}[PASS] ✓ Database{Fore.WHITE}')
    if 'link' in kwDict or 'link' in extraDict or 'link' in dupes:
      self.flagLink = True #handling data
      self.trueCount += 1
      print(f'{Fore.LIGHTGREEN_EX}[PASS] ✓ Link{Fore.WHITE}')
    if 'file' in kwDict or 'file' in extraDict or 'file' in dupes:
      self.flagFile = True #handling file
      self.trueCount += 1
      print(f'{Fore.LIGHTGREEN_EX}[PASS] ✓ File{Fore.WHITE}')
    else:
      for link in linkTypes:
        if link in kwDict or link in extraDict:
          self.flagTypeLink = True #get a specific link
          self.trueCount += 1
          self.linkType = link
          print(f'{Fore.LIGHTGREEN_EX}[PASS] ✓ link, linkType = {self.linkType}{Fore.WHITE}')

    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  trueCount = {self.trueCount}{Fore.WHITE}')

    if self.trueCount == 1: #as long as only one data type has been given
      if self.flagSQL: #if database command,
        self.exInfValues = [ *extraDict.values() ] #list of values
        self.exInfKeys = [ *extraDict.keys() ] #list of keys
        if 'all' in kwDict: #if get all
          self.select = '*' #wildcard
        else:
          self.position = self.exInfValues.index(0) #else get field name
          self.select = str(self.exInfKeys[self.position]) 
        print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  select = {self.select}{Fore.WHITE}')
        if 'key' in kwDict: #if using key
          self.keyPos1 = kwDict['key'] + 1 #position of key, adding 1 to get the key category
          self.keyPos2 = kwDict['key'] + 2 #position of key, + 2 to get if =, <, >, or LIKE
          self.keyPos3 = kwDict['key'] + 3 #get word 3 after keypos to get target key value
          self.position1 = self.exInfValues.index(self.keyPos1)
          self.key1 = str(self.exInfKeys[self.position1])
          self.position2 = self.exInfValues.index(self.keyPos2)
          self.key2 = str(self.exInfKeys[self.position2]).upper() #will always be =, <, >, or like, so upper() to make like become LIKE
          self.position3 = self.exInfValues.index(self.keyPos3)
          self.key3 = str(self.exInfKeys[self.position3]) #getting based on value & not key
          self.tempList = [self.key1, self.key2, self.key3]
          print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  keyPos1: {self.keyPos1}, position1: {self.position1}, key1: {self.key1} \n          keyPos2: {self.keyPos2}, position2: {self.position2}, key2: {self.key2} \n          keyPos3: {self.keyPos3}, position3: {self.position3}, key3: {self.key3}{Fore.WHITE}')
          # print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  ')
          self.where = ' '.join(self.tempList)  #create part of sql command following WHERE
          print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  where: {self.where}{Fore.WHITE}')

        # if 'keys' in kwDict:
        #   self.keysPos = kwDict['keys']
        #   self.andTimes = dupes['and']
        #   self.allArguments = []
          

        if 'table' in extraDict:
          self.tablePos = extraDict['table'] + 1 #get table name (1 after keyword table)
          self.position = self.exInfValues.index(self.tablePos)
          self.table = str(self.exInfKeys[self.position])  #get based on value not key
          print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  table: {self.table}{Fore.WHITE}')
        else:
          print(f'{Fore.LIGHTRED_EX}[ERROR] ! No table specified. Returning error code 106...{Fore.WHITE}')
          return 106
        self.sqlCmd = 'SELECT ' + self.select + ' FROM ' + self.table + ' WHERE ' + self.where #create full command
        print(f'{Fore.LIGHTCYAN_EX}[RETURN] ⏎ sql command: {self.sqlCmd}{Fore.WHITE}')
        return 'get' 'sql', self.sqlCmd
        #pass to database handler later

      elif self.flagFile:
        self.exInfValues = [ *extraDict.values() ]
        self.exInfKeys = [ *extraDict.keys() ]
        self.filePathValue = kwDict['file'] + 1
        self.fileNameValue = kwDict['file'] + 2
        self.position1 = self.exInfValues.index(self.filePathValue)
        self.position2 = self.exInfValues.index(self.fileNameValue)
        self.filePathKey = str(self.exInfKeys[self.position1])
        self.fileNameKey = str(self.exInfKeys[self.position2])
        for item in extensions:
          if item in self.fileNameKey:
            self.extension = str(item)
        print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  filePathValue = {self.filePathValue}, fileNameValue = {self.fileNameValue}, position1 = {self.position1}, position2 = {self.position2}, filePathKey = {self.filePathKey}, fileNameKey = {self.fileNameKey}, extension = {self.extension}{Fore.WHITE}')
        self.filePathFull = self.filePathKey + self.fileNameKey
        print(f'{Fore.LIGHTCYAN_EX}[RETURN] ⏎ filePathFull = {self.filePathFull}{Fore.WHITE}')
        return 'get', 'file', self.filePathFull, self.extension
        #pass to file handler later

      elif self.flagTypeLink:
        self.exInfValues = [ *extraDict.values() ]
        self.exInfKeys = [ *extraDict.keys() ]
        self.linkPosition = kwDict[self.linkType] + 1
        self.position = self.exInfValues.index(self.linkPosition)
        self.link = str(self.exInfKeys[self.position])
        print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  linkPosition = {self.linkPosition}, position = {self.position}{Fore.WHITE}')
        print(f'{Fore.LIGHTCYAN_EX}[RETURN] ⏎ link = {self.link}')
        return 'get', 'link', self.link
        #pass to webscraper later
      
      elif self.flagLink:
        self.kwDictValues = [ *kwDict.values() ]
        self.kwDictKeys = [ *kwDict.keys() ]
        self.linkKwPos = kwDict['link'] + 1
        self.position = self.kwDictValues.index(self.linkKwPos)
        self.kwLinkType = str(self.kwDictKeys[self.position])
        print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  linkKwPos = {self.linkKwPos}, position = {self.position}, kwLinkType = {self.kwLinkType}')
        return 'get', 'linkType', self.kwLinkType
        #pass to webscraper later

    elif self.trueCount < 1:
      print(f'{Fore.LIGHTRED_EX}[FAIL] ✗ No  datatype keyword found. Exiting...{Fore.WHITE}')
      sys.exit()

    else:
      print(f'{Fore.LIGHTRED_EX}[FAIL] ✗ Too many target data types given. Exiting...{Fore.WHITE}')
      sys.exit()
  
take = ImportCmds()
give = ExportCmds()

if take.passed:
  print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  ImportCmds passed.{Fore.WHITE}')
  if give.passed:
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Target file (currently commands.txt) has been emptied correctly.{Fore.WHITE}')
    i = 0
    for index in take.commands:
      commandDictionary.update({'command' + str(i): index})
      i += 1
    print(f'{Fore.LIGHTBLACK_EX}[INFO] ⓘ  Command Dictionary = {commandDictionary}')
    j = 0
    for command in commandDictionary: #for every command retrieved
      interpret = InterpretCmds(j) 
      cmd = interpret.baseKWcheck()
      d = Cmds()
      determine = d.initial(cmd[0], cmd[1]) #get base keyword, kwdict and extra info
      if determine[0] == 'get': #if get
        got = d.Get(determine[1], determine[2], determine[3]) #get command
        if got[1] == 'file': #if file
          getfile = FileGet()
          print(f'\n{getfile.start(got[2], got[3])}')
      j += 1

  else:
    print(f'{Fore.LIGHTRED_EX}[ERROR] ! Target file (currently commands.txt) is not empty.{Fore.WHITE}') #this will be handled in future.
    take
else:
  print(f'{Fore.LIGHTRED_EX}[ERROR] ! Target file (currently commands.txt) is empty. Exiting...{Fore.WHITE}')
  sys.exit()