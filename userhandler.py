import lastfmhandler

users = {}


def lastfm_user_exists(user):
    a = lastfmhandler.get_user_info(user)
    if 'error' in a:
        return False
    else:
        return True
