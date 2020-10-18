"""
Shared imports are here, as well as all other parts of the younify program.
"""

import logging, os, sys, eyed3, re, queue, time
import ctypes, unittest, json
from datetime import datetime

with open('c:\\config\\config.json') as f:
    config = json.load(f)

logloc = config['logging']['path']
icon = config["yt_frontend"]["icon"]
dark = config["yt_frontend"]["dark"]
temp_processing = config["framework"]["processing"]
temp_working = config["framework"]["working"]
temp_failed = config["framework"]["failed"]
bookmarks = config["testing"]["bookmarks"]
spotify_dir = config["youtube_converter"]["spotify_dir"]
spotify_cache = config["spotify"]["cache"]
artwork = config["youtube_converter"]["artwork"]
bookmarks = config["testing"]["bookmarks"]
database_connection = config["alchemy"]["connection"]
test_audio_file = config["filehandler_test"]["test_audio_file"]

#"mssql+pyodbc://rfarrow:sWEz7vdyDXjr@younify.database.windows.net/younify?driver=ODBC+Driver+17+for+SQL+Server"


enclosure_queue = queue.Queue()
fetch_threads = int(os.getenv('NUMBER_OF_PROCESSORS', 4))

# from younify import motley
# from younify import alchemy
# from younify import spotify
# from younify import app
# from younify import fingerprinter
# from younify import frames