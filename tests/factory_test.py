from app import factory

def test_this():
    assert True


def test_that():
    assert True


def test_videofactory_instantiates_playlist():
    """A single playlist returns correctly classified"""
    runner: object = factory.VideoFactory("https://www.youtube.com/watch?v=qoo27n_MPjY").classify()
    assert isinstance(runner, factory.YoutubePlaylist)


def test_videofactory_instantiates_song():
    """A single song returns correctly classified"""
    runner = factory.VideoFactory("https://www.youtube.com/watch?v=IJ8i49EqgYI").classify()
    assert isinstance(runner, factory.YoutubeSong)


def test_videofactory_instantiates_bulk_songs():
    """Multiple songs return correctly classified"""
    urls = ["https://www.youtube.com/watch?v=cXeHwhLPKz8", "https://www.youtube.com/watch?v=ZVx2WrgAZ7g",
            "https://www.youtube.com/watch?v=UNbOr0ylYZk", "https://www.youtube.com/watch?v=XleOkGsYgO8"]
    for url in urls:
        runner = factory.VideoFactory(url).classify()
        assert isinstance(runner, factory.YoutubeSong)
