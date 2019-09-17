import asyncio

import discord
from discord.ext import commands

from PIL import Image, ImageDraw, ImageFont
import os, random, re, typing, traceback, logging, random, json

PLAN_LOG = 'plan_log.json'

class Plans(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._talked = 0
        self._res_path = 'res/'
        self._progmember = ""
        self._def_regex = re.compile(r'<@!?(\d+)>|<@&(\d+)>|<#(\d+)>')
        self._plans_count = 0
        self._plans = self._plans_log_exists()
        self._PLANS_CHANNEL = 592103673920749594
        self._attr_list = []
        
    # Channel ID: 592103673920749594
    # Formatting:
    #   Location
    #   Date
    #   Description
    #   Time
    @commands.command(aliases=['pl'])
    async def plans(self,
                    ctx: commands.Context,
                    member: typing.Optional[discord.Member] = None,
                    role: typing.Optional[discord.Role] = None,
                    *,
                    message=None):
        title = ["Title:",
                 "Date:",
                 "Location:",
                 "Time:",
                 "Description:",
                 "Going Emoji:",
                 "Not Going Emoji"
                 ]

        if message is not None:
            splits = self._makeplan(message, title)
            await ctx.send("```{}```".format(message))
            if role is not None:
                msg = await ctx.send('Aright {}, we got plans...\n```{}```'.format(role.mention, splits))
            elif member is not None:
                msg = await ctx.send('Aright {}, we got plans...\n```{}```'.format(member.mention, splits))
            else:
                msg = await ctx.send("Aright, we got plans...\n```{}```".format(splits))

            await self._add_goingnotgoing_reaction(msg)

            print(type(msg))
            print(msg)
        else:
            plans_list = self._list_plans()
            if plans_list is "":
                await ctx.send('```None```')
            else:
                await ctx.send('```{}```'.format(plans_list))

    @commands.command()
    @commands.is_owner()
    async def pupdate(self,
                      ctx: commands.Context,
                      search_id: typing.Optional[int],
                      *,
                      key=None
                      ):
        if search_id:
            await ctx.send("```{} {}```".format(search_id, key))

    # Plans command utility
    async def _add_goingnotgoing_reaction(self, message):
        await message.add_reaction('\U0001f44d')
        await message.add_reaction('\U0001F346')
        # await message.add_reaction('\U0001F41E')

    def _makeplan(self,
                  message,
                  title
                  ):
        msg_tokens = message.split('>')

        msg_list = list(map(lambda x: x.strip(), msg_tokens))
        logging.info("ATTEMPT TO LOG")

        # JSON format data construction
        with open(PLAN_LOG, 'w') as outfile:
            extendable_format = {'id': len(self._plans['Plans']) + 1}
            for t, s in zip(title, msg_list):
                extendable_format.update({t.replace(':', ''): s})
            self._plans['Plans'].append(extendable_format)
            json.dump(self._plans, outfile, indent=4)
        split_args = list(map(lambda x, y: x + ' ' + y, title, msg_list))

        logging.info("[[[Plan Made]]]")

        return ' \n\n'.join(split_args)

    def _plans_log_exists(self):
        if not os.path.isfile(PLAN_LOG) and not os.access(PLAN_LOG, os.R_OK):
            logging.info(" PLAN_LOG DOES NOT EXIST; CREATING")
            plans_dict = {'Plans': []}
            with open(PLAN_LOG, 'w+') as outfile:
                json.dump(plans_dict, outfile, indent=4)
        else:
            logging.info(" PLAN_LOG EXISTS; LOADING")
            with open(PLAN_LOG) as outfile:
                plans_dict = json.load(outfile)
                logging.info(len(plans_dict['Plans']))
        return plans_dict

    def _list_plans(self):
        message = []
        plans_ext_dict = json.loads(open(PLAN_LOG, 'r').read())
        for i in plans_ext_dict['Plans']:
            plan_block = []
            for k, v in i.items():
                plan_block.append('{}: {} '.format(k, v))
                # logging.info('{}: {} '.format(k, v))
            formatted_plan_block = ' \n'.join(plan_block)
            message.append(formatted_plan_block)
        return ' \n\n'.join(message)

    @commands.command(name="idemoji")
    @commands.is_owner()
    async def emoji_id_identifier(self, ctx: commands.Context):
        tauthor = ctx.guild
        temojis = tauthor.emojis
        logging.info(temojis)
        # await ctx.send(emoji)
        await ctx.send(type(tauthor))
