from distutils.core import setup

setup(
    name='Younify',
    version='0.1.0',
    author='Robert Farrow',
    author_email='rob.farrow@hotmail.com',
    packages=['younify'],
    url='https://github.com/RFarrow9/Younify',
    license='LICENSE',
    description='Youtube-Spotify interface API',
    long_description=open('README.md').read(),
    install_requires=[
        "eyed3 == 0.8.10",
        "PyQt5 == 5.12.1",
        "python - magic == 0.4.15",
        "python - magic - bin == 0.4.14",
        "python3 - openid == 3.1.0",
        "pywin32 == 224",
        "QDarkStyle == 2.6.5",
        "qtconsole == 4.4.4",
        "requests == 2.21.0",
        "spotipy == 2.4.4",
        "SQLAlchemy == 1.2.19",
        "urllib3 == 1.24.2",
        "youtube - dl == 2019.7.2", 'logzero', 'youtube_dl'
    ],
)
