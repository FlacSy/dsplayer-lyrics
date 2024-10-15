from setuptools import setup, find_packages

setup(
    name='dsplayer-lyrics',  
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'dsplayer',
        'aiohttp',
        'bs4',
    ],
    entry_points={
        'dsplayer.plugins': [
            'lyrics = dsplayer_lyrics.lyrics:LyricsPlugin',
        ],
    },
)