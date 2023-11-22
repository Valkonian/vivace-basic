from bs4 import BeautifulSoup
import requests

class Scraper():
    def __init__(self):
        self.file = open("getURL.txt", "r") #open the file, i tried to do this with 'with' but it had a stroke and cried
        self.linesRead = self.file.readlines() #read file
        self.url = self.linesRead[0].strip() #read URLs
        self.request = self.linesRead[1] #get command
        self.page = requests.get(self.url) #get the page from the url
        self.soup = BeautifulSoup(self.page.text, features="html.parser") #soup it
        self.file.close()

    def SpotifySongStreams(self):
        self.allData = self.soup.find_all('table')[1] #take all data from target table
        self.titles = self.allData.find_all('th') #find headers
        self.data = self.allData.find_all('td') #find table data
        self.tableTitles = [ title.text for title in self.titles ] #list of all the table headers
        self.tableDataPrimitive = [ entry.text for entry in self.data ] #create primitive (unclean) table data
        self.tableDataClean = [] #for cleaned table data
        self.titlesLength = len(self.tableTitles) #length of the header list
        self.dataLength = int(len(self.tableDataPrimitive)) # length of the data list
        for i in range(0, self.dataLength, 3):
            self.temp = [self.tableDataPrimitive[i], self.tableDataPrimitive[i+1], self.tableDataPrimitive[i+2]] #create temp list to add to cleaned data
            self.tableDataClean.append(self.temp) #add to cleaned data
        return self.tableTitles, self.tableDataClean #return headers, cleaned data

    def SpotifyTotalStreams(self):
        self.allData = self.soup.find_all('table')[0] #take all data from target table
        self.titlesPrimitive = self.allData.find_all('th') #find primary headers
        self.titlesSecondary = [] #list for secondary headers
        self.data = self.allData.find_all('td') #all table data, including secondary headers
        self.titlesPrimary = [ title.text for title in self.titlesPrimitive ] #list of header
        self.titlesPrimary.pop(0) #remove blank header
        self.tableDataPrimitive = [ entry.text for entry in self.data ] #all the table data, unformatted
        self.tableDataClean = [] #formatted table data
        self.dataLength = int(len(self.tableDataPrimitive)) #length of the table data list
        for i in range(0, self.dataLength, 5):
            self.titlesSecondary.append(self.tableDataPrimitive[i]) #take secondary headers
            self.temp = [self.tableDataPrimitive[i+1], self.tableDataPrimitive[i+2], self.tableDataPrimitive[i+3], self.tableDataPrimitive[i+4]] #create temp list for appending to clean data
            self.tableDataClean.append(self.temp) #add to cleaned data
        return self.titlesPrimary, self.titlesSecondary, self.tableDataClean #return the primary headers, secondary headers, and cleaned table data
    
    def SpotifyListeners(self):
        self.allData = self.soup.find_all('table')[0] #get table
        self.titles = self.allData.find_all('th') #get table headers
        self.data = self.allData.find_all('td') #get tabe data
        self.tableTitles = [ title.text for title in self.titles] #list of table holders
        self.tableDataPrimitive = [ entry.text for entry in self.data ] #uncleaned table data
        self.tableDataClean = [] #for cleaned data
        self.dataLength = int(len(self.tableDataPrimitive)) #length of the list
        for i in range(0, self.dataLength, 5):
            self.temp = [self.tableDataPrimitive[i], self.tableDataPrimitive[i+1], self.tableDataPrimitive[i+2], self.tableDataPrimitive[i+3], self.tableDataPrimitive[i+4]] #temp list to append to cleaned data
            self.tableDataClean.append(self.temp) 
        return self.tableTitles, self.tableDataClean
    
    def getTopListenedKworbLinks(self):
        self.allData = self.soup.find_all('table')[0]
        self.data = self.allData.find_all('td')
        self.dataLength = len(self.data)
        self.hrefNameDict = {}
        for i in range(0, self.dataLength):
            self.currentData = self.data[i]
            for anchor in self.currentData.find_all('a'):
                self.name = anchor.contents[0]
                self.anchors = anchor.get('href')
                self.anchors = 'https://kworb.net/spotify/' + self.anchors
                self.hrefNameDict.update({str(self.name): self.anchors})
        return self.hrefNameDict
        

    def clearFile(self):
        open("getURL.txt", "w").close() #clear the file

scrape = Scraper()
print(scrape.getTopListenedKworbLinks())