from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine, MetaData

"""
This file handles the database interactions

Currently the database is a hosted azure instance

Question remains is how this can be sharded?

Should each user only be able to see their own information?
Should we 'cache' information for users to shortcut computation? How often would this change?
How would we define a user? Could we do it by unique spotify user??
"""

conn = "mssql+pyodbc://rfarrow:sWEz7vdyDXjr@younify.database.windows.net/younify?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn)
engine.connect()

Base = declarative_base()
session = sessionmaker()
session.configure(bind=engine)

def DropAllTables():
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    new = Column(String)


class Playlist(Base):
    __tablename__ = "Playlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    url = Column(String)
    # Playlist attributes here
    user = relationship(User, backref=backref('user', uselist=False))


class Album(Base):
    __tablename__ = "Albums"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    # Album attributes here


class Audiobook(Base):
    __tablename__ = "Audiobooks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    # Audiobook attributes here


class Song(Base):
    __tablename__ = "Songs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    playlist_id = Column(Integer, ForeignKey(Playlist.id))  # Can be null, if populated, must exist in Playlists table
    album_id = Column(Integer, ForeignKey(Album.id))  # Can be null, if populated, must exist in Albums table
    url = Column(String)
    title = Column(String)
    artist = Column(String)
    found = Column(String)
    artist_id = Column(String)
    song_id = Column(String)
    user = relationship(User, backref=backref('song', uselist=False))
    playlist = relationship(Playlist, backref=backref('playlist', uselist=False))


if __name__ == "__main__":
    DropAllTables()
    Base.metadata.create_all(engine)