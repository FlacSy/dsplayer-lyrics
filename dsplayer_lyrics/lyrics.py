from typing import Dict, Any
import aiohttp
import urllib.parse
from bs4 import BeautifulSoup
from dsplayer.plugin_system.plugin_interface import PluginInterface
from dsplayer.engines_system.engine_interface import EngineInterface
from dsplayer.utils.debug import Debuger


class LyricsPlugin(PluginInterface):
    def __init__(self):
        self.name = "LyricsPlugin"
        self.settings = {}
        self.debug_mode = False
        self.debug_print = Debuger(self.debug_mode).debug_print
        self.debug_print("LyricsPlugin initialized")

    def debug(self):
        self.debug_mode = True

    def on_plugin_load(self) -> None:
        self.debug_print("LyricsPlugin loaded")

    def on_plugin_unload(self) -> None:
        self.debug_print("LyricsPlugin unloaded")

    def get_plugin_name(self) -> str:
        self.debug_print(f"Plugin name: {self.name}")
        return self.name

    def get_settings(self) -> Dict[str, Any]:
        self.debug_print(f"Current settings: {self.settings}")
        return self.settings

    def update_settings(self, settings: Dict[str, Any]) -> None:
        self.debug_print(f"Updating settings: {settings}")
        self.settings.update(settings)

    def get_plugin_type(self) -> str:
        return "addon"
    
    async def search_lyric(self, query: str) -> Dict[str, Any]:
        self.debug_print(f"Searching for lyrics with query: {query}")
        url = self._generate_url(query)
        async with aiohttp.ClientSession() as session:
            lyric_url = await self._get_lyrics(session, url)
            lyrics = await self._get_lyric(session, lyric_url)
            return {"lyrics": lyrics}

    async def _get_lyrics(self, session, url):
        async with session.get(url) as resp:
            text = await resp.text()
            soup = BeautifulSoup(text, 'html.parser')
            lyric = soup.find('td', class_='text-left visitedlyr')
            lyric_url = lyric.find('a').get('href')
            return lyric_url

    def _generate_url(self, query: str) -> str:
        text = urllib.parse.quote_plus(query)
        return f"https://search.azlyrics.com/search.php?q={text}&x=4bb721140c09e63a8847f05a3bc72bc43797e3a8f0be36eda0f7d0d08325544b"

    async def _get_lyric(self, session, url: str) -> str:
        async with session.get(url) as resp:
            text = await resp.text()
            soup = BeautifulSoup(text, 'html.parser')
            lyric = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
            lyric = lyric.find('div', class_=None).text
            return lyric


# if __name__ == "__main__":
#     import asyncio
#     plugin = LyricsPlugin()
#     plugin.debug()
#     print(asyncio.run(plugin.search_lyric("ЧСВ"))['lyrics'])