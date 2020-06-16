import asyncio

import discord
from discord.ext import commands

from exts.pam_err import PAMsErrors, PAM_Disappointed, PAM_WrongAnswer
from PIL import Image, ImageDraw, ImageFont
import os, random, re, typing, traceback, logging, random, json


class Plans(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._talked = 0
        self._res_path = 'res/'
        self._progmember = ""
        self._def_regex = re.compile(r'<@!?(\d+)>|<@&(\d+)>|<#(\d+)>')
        self._PLANS_CHANNEL = 592103673920749594
        self._BOT_CHANNEL = 556930111270682624
        self._attr_list = []
        self._plans_running = False

        # bot_token = json.load(open(AUTH_FILE, 'r'))[AUTH_FIELD]

    def text_wrap(self, text, font, max_width):
        lines = []
        if font.getsize(text)[0] <= max_width:
            lines.append(text)
        else:
            words = text.split(' ')
            i = 0
            while i < len(words):
                line = ''
                while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                    line = line + words[i] + " "
                    i += 1
                if not line:
                    line = words[i]
                    i += 1
                lines.append(line)
        return lines

    # Testing
    @commands.command(name="ie")
    @commands.is_owner()
    async def runimgedit(self, ctx: commands.Context, *, message=None):
        self._generate_plan_template()
        if message is not None:
            self._test_picture_edit(message)
        channel = ctx.channel
        await channel.send(content="", file=discord.File(self._res_path + 'pam/plan1.png'))

    def _test_picture_edit(self, msg):
        print("called")
        image = Image.open(self._res_path + 'pam/bg.png')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self._res_path + 'pam/fonts/Roboto-Black.ttf', size=35)
        (x, y) = (10, 0)
        message = "Here's the plan.."
        color = 'rgb(0, 0, 0)'  # black color

        # draw the message on the background
        draw.text((x, y), message, fill=color, font=font)
        (x, y) = (10, 37)
        # name = 'hello'
        # name = self.text_wrap(msg, font, 900)
        name = msg
        # color = 'rgb(255, 255, 255)'  # white color
        draw.text((x, y), name, fill=color, font=font)

        # save the edited image

        image.save(self._res_path + 'pam/plan1.png')

    def _generate_plan_template(self):
        pass

    @commands.command(aliases=['pl'])
    async def plans(self, ctx: commands.Context):
        if not self._plans_running:
            self._plans_running = True
            await ctx.send("Begin P.A.M. Protocol")

            def check(m: discord.Message):
                return (m.content is not None) and \
                       (m.channel.id == self._BOT_CHANNEL or m.channel.id == self._PLANS_CHANNEL) and \
                       (m.author is ctx.author)
            try:
                title_varm: discord.Message = await ctx.send(
                    "[20 Seconds] Enter in Title of Event(If it has not been decided, type in \"idk\"):")
                title: discord.Message = await self._bot.wait_for('message', timeout=20.0, check=check)
                await title_varm.delete()
                await title.delete()

                date_varm: discord.Message = await ctx.send(
                    "[20 Seconds] Enter in Date of Event (If it has not been decided, type in \"idk\"):")
                date: discord.Message = await self._bot.wait_for('message', timeout=20.0, check=check)
                await date_varm.delete()
                await date.delete()

                desc_varm: discord.Message = await ctx.send(
                    "[20 Seconds] Enter in Description of Event (If it has not been decided, type in \"idk\"):")
                desc: discord.Message = await self._bot.wait_for('message', timeout=20.0, check=check)
                await desc_varm.delete()
                await desc.delete()

                time_varm: discord.Message = await ctx.send(
                    "[20 Seconds] Enter in Time of Event (If it has not been decided, type in \"idk\"):")
                time: discord.Message = await self._bot.wait_for('message', timeout=20.0, check=check)
                await time_varm.delete()
                await time.delete()

                loc_varm: discord.Message = await ctx.send(
                    "[20 Seconds] Enter in Location of Event (If it has not been decided, type in \"idk\"):")
                loc: discord.Message = await self._bot.wait_for('message', timeout=20.0, check=check)
                await loc_varm.delete()
                await loc.delete()

                # double check
                await ctx.send("The Title you chose is: \" {.content} \", \n"
                               "The Date you chose is: \" {.content} \", \n"
                               "The Description you chose is: \" {.content} \", \n"
                               "The Time you chose is: \" {.content} \", \n"
                               "The Location you chose is: \" {.content} \", \n"
                               "is that correct? (Y/N)".format(title, date, desc, time, loc))
                # Don't make P.A.M. sad :c
                _ans: discord.Message = await self._bot.wait_for('message', check=check)
                if _ans.content.lower() == 'n':
                    raise PAM_Disappointed
                elif _ans.content.lower() != 'y':
                    raise PAM_WrongAnswer
            except PAM_WrongAnswer:  # lazy programming part 1
                self._plans_running = False
                await ctx.send(
                    'P.A.M. asked for a yes or no and you gave her \"{}\".. what\'s wrong with you?'.format(_ans.content))
                await ctx.send('P.A.M. went to sleep..')
            except PAM_Disappointed:  # lazy programming part 2
                self._plans_running = False
                await ctx.send(
                    'P.A.M. says you are not satisfied with her performance.. She went to sleep..')
            except asyncio.TimeoutError:
                self._plans_running = False
                await ctx.send('P.A.M. went to sleep..')
            else:
                self._plans_running = False
                self._attr_list.append(title)
                self._attr_list.append(date)
                self._attr_list.append(desc)
                self._attr_list.append(time)
                self._attr_list.append(loc)

                self._attr_list = self.cleanup_event(self._attr_list)

                print(self._attr_list)

                await ctx.send("P.A.M. is now finishing things up.. [End of process.. for now..]")
        else:
            pass

    def cleanup_event(self, list):
        nlist = []
        for message in list:
            if message.content.startswith('idk'):
                nlist.append('TBA')
            else:
                nlist.append(message.content)

        return nlist

def setup(bot: commands.Bot):
    logging.info('>>> Setting up [ P.A.M. ] ')
    bot.add_cog(Plans(bot))
    logging.info('>>> Done setting up [ P.A.M. ] ')
