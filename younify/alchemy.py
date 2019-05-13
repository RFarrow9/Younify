from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine, MetaData
from datetime import datetime

"""
This file handles the database interactions

Currently the database is a hosted azure instance

How can this be sharded/Horizontal partitioning?
Bring through the dates correctly.
Should each user only be able to see their own information?
Should we 'cache' information for users to shortcut computation? How often would this change?
How would we define a user? Could we do it by unique spotify user??
"""

conn = "mssql+pyodbc://rfarrow:sWEz7vdyDXjr@younify.database.windows.net/younify?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn)
try:
    engine.connect()
except:
    print("Could not connect to engine")


Base = declarative_base()
session = sessionmaker()
session.configure(bind=engine)

def DropAllTables():
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()

def AddTestUser():
    testuser = User()
    testuser.name = "Test"
    testuser.fullname = "Test_User"
    testuser.nickname = "testyuser"
    testuser.new = "fsubv"
    #testuser.insert_dt = datetime.now()
    s = session()
    s.add(testuser)
    s.commit()


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    new = Column(String)
   #created = Column(datetime)


class Playlist(Base):
    __tablename__ = "Playlists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    url = Column(String)
    title = Column(String)
    song_count = Column(Integer)
    #created = Column(datetime, default=datetime.utcnow)
    # Playlist attributes here
    # Relationships below here
    user = relationship(User, backref=backref('user', uselist=False))


class Album(Base):
    __tablename__ = "Albums"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    #created = Column(datetime, default=datetime.utcnow)
    # Album attributes here


class Audiobook(Base):
    __tablename__ = "Audiobooks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
   # created = Column(datetime, default=datetime.utcnow)
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
 #   created = Column(datetime, default=datetime.utcnow)


def main():
    print("Nothing to do here.")


def prime():
    DropAllTables()
    Base.metadata.create_all(engine)
    AddTestUser()


if __name__ == "__main__":
    main()