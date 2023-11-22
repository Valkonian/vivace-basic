from bs4 import BeautifulSoup
import requests

class Scraper():
    def __init__(self):
        self.url = 'https://kworb.net/spotify/artist/6qqNVTkY8uBg9cP3Jd7DAH_songs.html'
        self.page = requests.get(self.url) #get the page from the url
        self.soup = BeautifulSoup(self.page.text, features="html.parser")

    def SpotifySongStreams(self):
        self.allData = self.soup.find_all('table')[1]
        self.titles = self.allData.find_all('th')
        self.data = self.allData.find_all('td')
        self.tableTitles = [ title.text for title in self.titles ]
        self.tableDataPrimitive = [ entry.text for entry in self.data ]
        self.tableDataClean = []
        self.titlesLength = len(self.tableTitles)
        self.dataLength = int(len(self.tableDataPrimitive))
        for i in range(0, self.dataLength, 3):
            self.temp = [self.tableDataPrimitive[i], self.tableDataPrimitive[i+1], self.tableDataPrimitive[i+2]]
            self.tableDataClean.append(self.temp)
        print(self.tableDataClean)

scrape = Scraper()
scrape.SpotifySongStreams()