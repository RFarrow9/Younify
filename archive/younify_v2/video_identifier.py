import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from typing import *

"""

This is a file used to hold the training of a model that is is used to identify a video on youtube as either a song, album, playlist or other.

features used:
    - length of video
    - likes
    - views
    - title contains "-"
    - title contains "music video"
    - description contains "artist"
    - description contains "download"
    - description contains "playlist"
    - title contains "mix"
    - title contains "album"


"""


def train_xgboost_model():
    data = pd.read_csv("./resources/output_enriched_unlabelled_v0.csv")
    data = data.drop_duplicates().drop(['artist', 'url'], axis=1)
    inputs = data[["length", "title", "description"]]
    outputs = data["type"]

    # Now we need to fit the outputs to a label encoder
    enc = LabelEncoder()
    enc.fit(outputs)
    print(enc.classes_)
    outputs = enc.transform(outputs)

    # Now we transform our inputs into features
    pd.set_option('mode.chained_assignment', None)
    length_series = pd.to_numeric(inputs['length'], errors='coerce')
    inputs['length'] = pd.Series(length_series)

    def str_in_col(row, str: str, column: str) -> int:
        try:
            if str in row[column].lower():
                return 1
        except:
            return 0
        return 0

    inputs['dash_present_in_title'] = inputs.apply(str_in_col, str="-", column="title", axis=1)
    inputs['soundtrack_present_in_title'] = inputs.apply(str_in_col, str="soundtrack", column="title", axis=1)
    inputs['download_present_in_description'] = inputs.apply(str_in_col, str="download", column="description", axis=1)
    inputs['music_video_in_title'] = inputs.apply(str_in_col, str="music video", column="title", axis=1)
    inputs['music_video_in_description'] = inputs.apply(str_in_col, str="music video", column="description", axis=1)
    inputs['playlist_in_title'] = inputs.apply(str_in_col, str="playlist", column="title", axis=1)
    inputs['playlist_in_description'] = inputs.apply(str_in_col, str="playlist", column="description", axis=1)
    inputs['mix_present_in_title'] = inputs.apply(str_in_col, str="mix", column="title", axis=1)
    inputs['album_in_title'] = inputs.apply(str_in_col, str="album", column="title", axis=1)

    inputs.drop(['title', 'description'], axis=1, inplace=True)
    seed = 7
    test_size = 0.33
    for col in inputs.columns:
        print(col)
    x_train, x_test, y_train, y_test = train_test_split(inputs, outputs, test_size=test_size, random_state=seed)
    model = XGBClassifier()
    model.fit(x_train, y_train)
    print(model)

    y_pred = model.predict(x_test)

    predictions = [round(value) for value in y_pred]
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))




if __name__ == "__main__":
    train_xgboost_model()