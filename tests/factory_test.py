from app import factory
import pytest


def test_this():
    assert True


def test_that():
    assert True


def test_videofactory_instantiates_playlist():
    runner = factory.VideoFactory("https://www.youtube.com/watch?v=qoo27n_MPjY").classify()
    assert isinstance(runner, factory.YoutubePlaylist)


def test_videofactory_instantiates_song():
    runner = factory.VideoFactory("https://www.youtube.com/watch?v=IJ8i49EqgYI").classify()
    assert isinstance(runner, factory.YoutubeSong)