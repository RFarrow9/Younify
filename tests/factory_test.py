from app import factory
import pytest


def test_this():
    assert True


def test_that():
    assert True


def test_1():
    url = "https://www.youtube.com/watch?v=qoo27n_MPjY"
    runner = factory.VideoFactory(url).classify()
    # print(runner.timestamps)
    assert True
