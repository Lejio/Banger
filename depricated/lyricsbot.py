from lyricsgenius import Genius
import os

def getsong(song):

  GENIUS_TOKEN = os.environ['GENIUS_TOKEN']

  genius = Genius(access_token=GENIUS_TOKEN)

  song = genius.search_song(title=song)

  print(song.lyrics)

  return song.lyrics

from urllib2 import Request, urlopen

request = Request('https://api.lyrics.ovh/v1/Imagine Dragons/Bones')

response_body = urlopen(request).read()
print(response_body)
