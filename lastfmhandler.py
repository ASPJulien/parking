import requests
import urllib.parse
import confighandler

apikey = confighandler.get_config()["apikey"]


def get_track_playcount(user, track):
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={apikey}&artist={track['artist']['#text']}&track={urllib.parse.quote(track['name'].lower())}&format=json&username={user}").json()
    return r['track']['userplaycount']


# from track
def get_album_playcount(user, track):
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={apikey}&artist={track['artist']['#text']}&album={track['album']['#text']}&format=json&username={user}").json()
    return r['album']['userplaycount']


# from track
def get_artist_playcount(user, track):
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=artist.getInfo&api_key={apikey}&artist={track['artist']['#text']}&format=json&username={user}").json()
    return r['artist']['stats']['userplaycount']


def get_tracks_recent(user):
    return requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={apikey}&format=json&limit=5").json()


# from track
def get_album(track):
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={apikey}&artist={track['artist']['#text']}&album={track['album']['#text']}&format=json").json()

    return r['album']


def get_user_info(user):
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={user}&api_key={apikey}&format=json").json()
    return r
