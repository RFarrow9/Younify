Younify
===========

This is a tool currently being developed to integrate youtube and spotify. If your work blocks spotify but allows youtube, or you have disparate libaries of 'bookmarks', and you want those songs in spotify - this is the tool for you (you know, when its done).

The eventual end being a simple button that can integrate in a browser of your choice, that when clicked will go grab the track from the youtube video tab you're on and find it in spotify if it exists, and if it doesn't, it'll grab the file, download, convert, and put it in your local files for you for use in spotify or media player of your choice.

This is currently pre-alpha, and will be difficult to use without some significant environment modifications, and understanding of how this terrible code is organised.

Modules
=========

The code is currently split into the following modules:

* classification - this will handle classification of youtube videos, as well as artist and song assignment

* framework - holds arrays for processing and handles temp file updates, and multithreading for youtube_converter

* frontend - no longer being used

* scratch - scratch pad for redundant code/testing code

* spotify - interacts with spotify api surprisingly

* youtube_converter - downloads and handles conversion of videos

* yt_frontend - code in progress for GUI
