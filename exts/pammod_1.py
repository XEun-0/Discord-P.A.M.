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

        # bot_token = json.load(open(AUTH_FILE, 'r'))[AUTH_FIELD]

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

    #further testing
    @commands.command(aliases=['pl2'])
    async def plans_2(self, ctx: commands.Context, message: typing.Optional[discord.Message] = None):
        await ctx.send(discord.__version__)
        #msg = await self._bot.wait_for_message(author=message.author)

    #Listeners
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass



def setup(bot: commands.Bot):
    logging.info('>>> Setting up [ plans ] ')
    bot.add_cog(Plans(bot))
    logging.info('>>> Done setting up [ plans ] ')
