Younify
===========
## Contents
* [What is Younify?](#what-is)
* [Technologies](#tech)
* [Progress](#prog)
* [Modules so far](#mod)
* [Future Enhancements](#fut) 

<a name="what-is"></a>
## <img src="younify/resources/Yin_yang.svg" alt="Logo" width="20"/> What is Younify?

Younify is a tool currently in early stages of development that hopefully will allow for youtube music videos/playlists to be looked up automatically in Spotify.

This is being developed in order to learn technologies that are used in creating a full end-to-end solution. The code is written in an attempt to adhere to best 
practices for object-orientated programming, and utilising design patterns where possible. The emphasis is on writing good code, with refactoring taking place often
when better ways of doing things are found.

The eventual end solution being a simple button that can integrate in a browser of your choice, that when clicked will go grab the track from the youtube video tab
 you're on and find it in spotify if it exists, and if it doesn't, it'll grab the file, download, add metadata, convert, and put it in your local files for you for 
 use in spotify or media player of your choice.
 
 Currently there is a website, however this is relatively raw and undeveloped:
 https://younify.azurewebsites.net/
 
<a name="tech"></a>
## <img src="younify/resources/Yin_yang.svg" alt="Logo" width="20"/> Technologies
* Azure
* Object-orientated programming
* Object-Relational mapping (SQL Alchemy)
* Python
* JSON
* Multithreading
* API Interaction
* GUI Creation (QtPy)
* Github (obviously!)

<a name="prog"></a>
## <img src="younify/resources/Yin_yang.svg" alt="Logo" width="20"/> Progress
Currently the program works to process URLs with little issue, and appears to have a reasonable hitrate when pulling 
metadata from spotify. However the code to put the actual song into a spotify playlist is not yet done.

The program also interacts with the azure database using the ORM with no issues, and can successfully upload 
processed playlists, parse out what songs exist in it, and push these to a songs table with an intact foreign key
relationship.

The GUI needs some work, currently this has a manual processing tab and a processing tab, all the others are 
fillers. The processing tab does include a table, which does populate from the frameworks processing array (which
holds all the objects to be processed).

<a name="mod"></a>
## <img src="younify/resources/Yin_yang.svg" alt="Logo" width="20"/> Modules so far

The code is currently split into the following modules:

For further documentation on these files, see the headers inside the files themselves.

* youtube_converter - downloads and handles conversion of videos

* framework - holds arrays for processing and handles temp file updates, and multithreading for youtube_converter

* spotify - interacts with spotify api surprisingly

* yt_frontend - holds GUI code and linking function to frontend

* alchemy - handles azure shardification and database requests via ORM

* filehandler - handles files? This will be useful for parsing existing libraries for spotify transfer

* fingerprinting - this is a holder for a module that handles interacting with audio fingerprint APIs

<a name="fut"></a>
## <img src="younify/resources/Yin_yang.svg" alt="Logo" width="20"/> Future enhancements

* It would not be difficult to make minor extensions to the code to also handle pulling metadata out of 
files in order to sync offline libraries with spotify. 
* Make sure that multithreading is truly multithreading (there are some issues with the global interpreter
lock currently that stop true multithreading in a single python instance)
* Look at how temp files are created, perhaps we only need in progress ones as a backup for crashes. Can these be pickled?
* Can the azure database be sharded effectively? This wouldn't serve much of a purpose other than learning.
But still worth investigating.
* Might need to write something to check (if handling large numbers of objects) how many songs already exist
in the users profile. Spotify has a hard limit of 10k per device (up to five devices?)
* Website definitely needs some work