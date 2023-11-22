from bs4 import BeautifulSoup
import requests

url = 'https://kworb.net/spotify/artist/3TVXtAsR1Inumwj472S9r4_songs.html'
page = requests.get(url) #get the page from the url
soup = BeautifulSoup(page.text, features="html.parser")


allData = soup.find_all('table')[1]
titles = allData.find_all('th')
data = allData.find_all('td')
tableTitles = [ title.text for title in titles ]
tableDataPrimitive = [ entry.text for entry in data ]
tableDataClean = []
titlesLength = len(tableTitles)
dataLength = int(len(tableDataPrimitive))
for i in range(0, dataLength, 3):
    temp = [tableDataPrimitive[i], tableDataPrimitive[i+1], tableDataPrimitive[i+2]]
    tableDataClean.append(temp)
print(tableDataClean)