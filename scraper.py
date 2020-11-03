from bs4 import BeautifulSoup
import urllib.request
import time
import random
import json
import pprint

def getLink(url):
	waitTime = random.randrange(10,20,1)
	time.sleep(waitTime)
	try:
		response = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		print(e)
	html = response.read()
	return html

def getLyrics(finishedResponse):
	soup = BeautifulSoup(finishedResponse, 'html.parser')
	lyricsBlock = soup.find("div", attrs={"class":"ringtone"}).find_next_sibling("div")
	return lyricsBlock

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

artistAlbumList = {
    "name": "",
    "albums": []
}

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
                artistAlbumList["albums"].append(album)
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
            if newurl.startswith("https://www.azlyrics.com"):
                newurl2 = newurl
            else:
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
    artistAlbumList["albums"].append(album)


def testList(artist):
    for album in artist["albums"]:
        print("*****")
        print(album["albumName"], album["year"])
        print("*****")
        for song in album["trackList"]:
            print(song["songName"])
            print(song["url"])

def createFile(artist):
    url = "your url here"
    f = open(url, "w+")
    pprint.pprint(artist)
    jsonStr = json.dumps(artistAlbumList)
    f.write(jsonStr)
    f.close

#testList(artistAlbumList)

def getLyricsForArtist(artistname):
	# TODO - bands starting with a number have a 19 prefix
    url = "https://www.azlyrics.com/" + artistname[0]+ "/" + artistname + ".html"
    print(url)
    response = urllib.request.urlopen(url)
    html = response.read()
    bigSoup = BeautifulSoup(html, 'html.parser')
    listalbum = bigSoup.find("div", attrs={"id":"listAlbum"})
    itemized_list = listalbum.find_all("div")

    artistAlbumList["name"] = artistname
    goThroughList(itemized_list)
    getAnArtistsLyrics(artistAlbumList)
    createFile(artistAlbumList)

def cleanUpTags(tagged):
    # basic cleanup. further clean-up needs to be done somewhere else
    stringifiedSongLyrics = str(tagged)
    removedBreaks = stringifiedSongLyrics.replace("<br/>","")
    removedOpenDivs = removedBreaks.replace("<div>","")
    removedClosedDivs = removedOpenDivs.replace("</div>","")
    return removedClosedDivs

def getAnArtistsLyrics(artist):
    for album in artist["albums"]:
        for song in album["trackList"]:
            songHtml = getLink(song["url"])
            songLyrics = getLyrics(songHtml)
            song["lyrics"] = cleanUpTags(songLyrics)
