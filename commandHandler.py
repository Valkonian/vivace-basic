

class Import():
    def __init__(self):
        self.commands = []
        self.file = open('commands.txt')
        for line in self.file: #for every line in the file
            self.commands.append(line.strip()) #append the stripped line to the commands list
        self.file.close() #close the file when done
        open("commands.txt", "w").close()
        print('Cleared') #clear the file when done as to not leave leftover commands that have already been retrieved

class Export():
    def __init__(self):
        #checking if command file is empty
        self.leftovers = []
        self.file = open('commands.txt')
        for line in self.file:
            self.leftovers.append(line.strip())
        if len(self.leftovers) == 0:
            self.passed = True
        else:
            self.passed = False
    
    def exportCommand(self, commands):
        self.file = open('commands.txt', 'w')
        self.toWrite = "\n".join(commands)
        self.file.write(self.toWrite)
        self.file.close()
        
take = Import()
give = Export()

if give.passed:
    print('Yes')
    for index in take.commands:
        print(index)
else:
    print('No')