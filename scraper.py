from bs4 import BeautifulSoup
import urllib.request
import time
import random
import json

# TODO: replace classes with dicts to be serializable

class Album:
    def __init__(self, albumName, year):
        self.albumName = albumName
        self.year = year
        self.trackList = []

class Song:
    def __init__(self, songName, url, songLyrics=""):
        self.songName = songName
        self.songLyrics = songLyrics
        self.year = 0
        self.url = url

def getLink(url):
	waitTime = random.randrange(10,20,1)
	time.sleep(waitTime)
	response = urllib.request.urlopen(url)
	html = response.read()
	return html

def getLyrics(finishedResponse):
	soup = BeautifulSoup(finishedResponse, 'html.parser')
	lyricsBlock = soup.find("div", attrs={"class":"ringtone"}).find_next_sibling("div")
	print(lyricsBlock)

# ring = [x for x in artistAlbumList if x.albumName == "\"The Album\""]
# print(ring[0].trackList)

def getAnAlbumsLyrics(album):
    for each in album[0].trackList:
    	songHtml = getLink(each.url)
    	songLyrics = getLyrics(songHtml)
    	print(songLyrics)


######

#response = urllib.request.urlopen("https://www.azlyrics.com/a/abba.html")
#html = response.read()

# bigSoup = BeautifulSoup(text, 'html.parser')

# listalbum = bigSoup.find("div", attrs={"id":"listAlbum"})

# itemized_list = listalbum.find_all("div")

#for member in itemized_list:
#    membertext = member['class'][0]
#    if membertext == "album":
#        print(member.b.contents[0])
#    elif membertext == "listalbum-item":
#        print(member.a.get('href'))
#        print("name",member.a.contents[0])

# artistAlbumList = []

artistAlbumList = []

def goThroughList(list):
    album = ""
    for member in list:
        membertext = member['class'][0]
        if membertext == "album":
            if album == "" :
                nameWithQuotes = member.b.contents[0]
                newname = nameWithQuotes.replace("\"", "")
                member.b.extract()
                year = 0
                if len(member) > 0:
                    yearWithParens = member.contents[1]
                    year = ''.join(char for char in yearWithParens if char not in '()')
                else:
                    year = 3333
                #album = Album(newname, year)
                album = {
                    "albumName": newname,
                    "year": year,
                    "trackList": []
                }
            else:
                artistAlbumList.append(album)
                nameWithQuotes = member.b.contents[0]
                newname = nameWithQuotes.replace("\"", "")
                member.b.extract()
                year = 0
                if len(member) > 0:
                    yearWithParens = member.contents[1]
                    year = ''.join(char for char in yearWithParens if char not in '()')
                else:
                    year = 3333
                #album = Album(newname, year)
                album = {
                    "albumName": newname,
                    "year": year,
                    "trackList": []
                }
        elif membertext == "listalbum-item":
            newurl = member.a.get('href')
            newurl2 = "https://www.azlyrics.com" + newurl[2:]
            newname = member.a.contents[0]
            #song = Song(newname, newurl2)
            song = {
                "songName": newname,
                "songLyrics": "",
                "year": 0,
                "url": newurl2
            }
            album["trackList"].append(song)
    artistAlbumList.append(album)

#goThroughList(itemized_list)

def testList(test):
    for each in test:
        print("*****")
        print(each["albumName"], each["year"])
        print("*****")
        for song in each["trackList"]:
            print(song["songName"])
            print(song["url"])

#testList(artistAlbumList)

def getLyricsForArtist(artistname):
    url = "https://www.azlyrics.com/" + artistname[0]+ "/" + artistname + ".html"
    print(url)
    response = urllib.request.urlopen(url)
    html = response.read()
    bigSoup = BeautifulSoup(html, 'html.parser')
    listalbum = bigSoup.find("div", attrs={"id":"listAlbum"})
    itemized_list = listalbum.find_all("div")

    goThroughList(itemized_list)
    testList(artistAlbumList)
    #jsonStr = json.dumps(artistAlbumList)
    #print(jsonStr)


getLyricsForArtist("kimpetras")
