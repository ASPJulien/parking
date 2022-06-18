import lastfmhandler

users = {}


def lastfm_user_exists(user):
    a = lastfmhandler.get_user_info(user)
    return 'error' not in a
