import sklearn.feature_extraction

"""
We generate a model for basic multiclass text classification.

    1. Collect a set of 4000 youtube urls
    2. Harvest the metadata from these in a csv format
    3. Label the data
    
We can use a semi autonomous method for this, as the framework for a first pass classification (using simple length of the video)
and metadata harvesting is already in place. There will need to be a manual check after this to place the videos, and we will need
a fair distribution (no skew) of songs/playlists/audiobooks/albums/other.

With the data harvested, we can use the sklearn tf-idf algorithm to generate a set of features, and with labelling done, we can use t-sne
to visualise the data. Does it naturally aggregate by type, or does it cluster on something else? If we only feed it the data from the 
metadata (description and title only) does this effect the clustering?

Then we can teach an xgboost (or random forest) to hopefully parse out whether the video is a song/playlist/album.

With that done, we might be able to use ml in future to pull out the artist from the title.

"""




