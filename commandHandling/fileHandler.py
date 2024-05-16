import json

class FileGet():
    def __init__(self, filepath, extension, command):
        self.lines = []
        if extension == '.txt':
            with open(filepath) as self.file:
                self.read = self.file.readlines()
                for line in self.read:
                    self.lines.append(line.strip())
                print(self.lines)
        elif extension == '.json':
            with open(filepath) as self.file:
                self.read = json.load(self.file)
                print(self.read)
                