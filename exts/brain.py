#!/usr/bin/env python3

import discord
from discord.ext import commands

import sys, json, traceback, logging

class Brain(commands.Cog):
    def __init__(self, bot: commands.bot):
        self._bot = bot

def setup(bot: commands.Bot):
    logging.info('>>> Setting up [ brain ] ')
    bot.add_cog(Brain(bot))
    logging.info('>>> Done setting up [ brain ] ')
