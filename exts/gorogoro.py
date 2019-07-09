import discord
from discord.ext import commands

from lxml import html

import requests as req
import urllib.request
import time
from bs4 import BeautifulSoup

import os, random, re, typing, traceback, logging, random

class Ping(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._WAIFU_GACHA_CHANNEL = 557963012472832021
        self._BOT_TESTING_CHANNEL = 556930111270682624

        # url = 'https://mangarock.com/manga/latest'
        #
        # response = req.get(url)
        # soup = BeautifulSoup(response.content, 'lxml')
        # for tag in soup.find_all("meta"):
        #     print(type(tag))
        #
        # print(soup.prettify())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if 'nigga' in message.content.lower() and message.channel.id == self._BOT_TESTING_CHANNEL:
            await message.delete()
            await message.channel.send('BAD WORD MAN')


def setup(bot: commands.Bot):
    logging.info('>>> Setting up [ gorogoro ] ')
    bot.add_cog(Ping(bot))
    logging.info('>>> Done setting up [ gorogoro ]')
