import requests
import urllib.parse
import confighandler

apikey = confighandler.get_config()["apikey"]


def get_track_playcount(user: str, track: dict) -> int:
    """
    Returns the playcount of a track
    :param user: The user's last.fm username
    :type user: str
    :param track: The track to look track playcount for
    :return: The playcount of the track
    :rtype: int
    """
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={apikey}&artist={track['artist']['#text']}&track={urllib.parse.quote(track['name'].lower())}&format=json&username={user}").json()
    return r['track']['userplaycount']


# from track
def get_album_playcount(user: str, track: dict) -> int:
    """
    Returns the playcount of an album
    :param user: The user's last.fm username
    :type user: str
    :param track: The track to look album playcount for
    :type track: dict
    :return: The playcount of the album
    :rtype: int
    """
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={apikey}&artist={track['artist']['#text']}&album={track['album']['#text']}&format=json&username={user}").json()
    return r['album']['userplaycount']


# from track
def get_artist_playcount(user: str, track: dict) -> int:
    """
    Returns the playcount of an artist
    :param user: The user's last.fm username
    :type user: str
    :param track: The track to look artist playcount for
    :type track: dict
    :return: The playcount of the artist
    :rtype: int
    """
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=artist.getInfo&api_key={apikey}&artist={track['artist']['#text']}&format=json&username={user}").json()
    return r['artist']['stats']['userplaycount']


def get_tracks_recent(user: str, count: int) -> dict:
    """
    Returns the user's most recent tracks
    :param user: The user's last.fm username
    :type user: str
    :param count: Numbre of tracks to fetch for
    :type: count: int
    :return: The user's most recent tracks
    :rtype: dict
    """
    return requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={apikey}&format=json&limit={count}").json()


# from track
def get_album(track: dict) -> dict:
    """
    Returns the album of a track
    :param track: The track to look album for
    :type track: dict
    :return: The album of the track
    :rtype: dict
    """
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={apikey}&artist={track['artist']['#text']}&album={track['album']['#text']}&format=json").json()

    return r['album']


def get_user_info(user: str) -> dict:
    """
    Returns the user's info
    :param user: The user's last.fm username
    :type user: str
    :return: The user's info
    :rtype: dict
    """
    r = requests.get(
        f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={user}&api_key={apikey}&format=json").json()
    return r
