from app import spotify


def test_spotify_instantiates():
    """Tests that the spotify singleton succesfully instantiates"""
    spot = spotify.SpotifySingleton()
    print(type(spotify.SpotifySingleton))
    assert isinstance(spot, spotify.SpotifySingleton.__wrapped__)


def test_spotify_singleton():
    """"""
    spot = spotify.SpotifySingleton()
    spot.test_num = 6
    second_spot = spotify.SpotifySingleton()
    assert second_spot.test_num == 6


def test_spotify_communicates():
    """"""
    spot = spotify.SpotifySingleton()
    spot.set_sp()
    assert spot.sp is not None


def test_spotify_gets_albums_using_oauth():
    spot = spotify.SpotifySingleton()
    spot.set_sp()
    albums = spot.artist_albums("spotify:artist:7meq0SFt3BxWzjbt5EVBbT")
    assert albums['total'] == 23