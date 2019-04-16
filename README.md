New website! https://younify.azurewebsites.net/

Younify
===========
## Contents
* [What is Younify?](#What is Younify?)
* [Technologies](#technologies)
* [Progress](#progress)
* [Modules so far](#modules so far)
* [Future Enhancements](#future enhancements) 

<a name="What is Younify?">
## What is Younify? <img src="younify/resources/Yin_yang.svg" alt="Logo" width="20"/>
</a>

Younify is a tool currently in early stages of development that hopefully will allow for youtube music videos/playlists to be looked up automatically in Spotify.

This is being developed in order to 

If your work blocks spotify but allows youtube, or you have disparate libaries of 'bookmarks', and you want those songs in spotify - this is the tool for you (you know, when its done).

The eventual end being a simple button that can integrate in a browser of your choice, that when clicked will go grab the track from the youtube video tab you're on and find it in spotify if it exists, and if it doesn't, it'll grab the file, download, convert, and put it in your local files for you for use in spotify or media player of your choice.

<a name="technologies">
## Technologies
</a>

Some words here

<a name="progress">
## Progress
</a>

<a name="modules so far">
## Modules so far
</a>
The code is currently split into the following modules:

* classification - this will handle classification of youtube videos, as well as artist and song assignment

* framework - holds arrays for processing and handles temp file updates, and multithreading for youtube_converter

* scratch - scratch pad for redundant code/testing code

* spotify - interacts with spotify api surprisingly

* youtube_converter - downloads and handles conversion of videos

* yt_frontend - code in progress for GUI

* alchemy - handles azure shardification and database requests

* filehandler - handles files? This will be useful for parsing existing libraries for spotify transfer

<a name="future enhancements">
## Future enhancements
</a>

We could use this code to harvest + unify spotify with current media libraries that exist in file form as well.
Use proper threading techniques
Pickle temp files
Look at migrating temp files into azure
Azure shardification by user? How do we identify the user?
Handle the spotify song limit? Still only 10k?
Develop the website to be less crap