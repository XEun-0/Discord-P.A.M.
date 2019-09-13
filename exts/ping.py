import discord
from discord.ext import commands

import os, random, re, typing, traceback, logging, random, json

class Ping(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._talked = 0
        self._res_path = 'res/'
        self._progmember = ""
        self._def_regex = re.compile(r'<@!?(\d+)>|<@&(\d+)>|<#(\d+)>')

        # bot_token = json.load(open(AUTH_FILE, 'r'))[AUTH_FIELD]

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: discord.DiscordException):
        logging.debug('Misc error by {}: {}'.format(ctx.author, error))
        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if await self._bot.is_owner(ctx.author):
            traceback.print_exc()
            await ctx.send('You messed up, but I forgive you {}'.format(ctx.author.mention))
            return

        if isinstance(error, commands.NotOwner):
            await ctx.invoke(self.disobedience, ctx.author, 'what are you, autistic?')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.invoke(self.disobedience, ctx.author, 'spamming a command')
        elif isinstance(error, commands.UserInputError):
            await ctx.invoke(self.disobedience, ctx.author, 'incompetence')
        else:
            logging.error('Something fatal ocurred')

    @commands.command()
    # @commands.is_owner()
    async def ping(self,
                   ctx: commands.Context,
                   member: typing.Optional[discord.Member] = None,
                   message='face',
                   occurence: typing.Optional[int] = 10):

        await ctx.message.delete()

        r = random.randint(0, 10)
        # or member.bot
        if await self._bot.is_owner(member) or member.bot:
            if r <= 3:
                await ctx.send(' What are you, autistic? ')
            elif r <= 6 and r > 3:
                await ctx.send(' 너 자폐증이야? ')
            else:
                await ctx.send(' 自閉症ですか？ ')
        elif member is not None:
            await ctx.send(' pongs {}\'s {} {} times. '.format(member.mention, message, occurence))
        else:
            await ctx.send(' it\'s ok ')

        logging.info('>>> International Autism Calling Complete.')

    @commands.command()
    async def chop(self, message: discord.Message):

        print(message)
        print(type(message))

        channel = message.channel
        await channel.send(content="chop", file=discord.File(self._res_path + '/ramiris_chop.png'))
        logging.info('>>> [ Chop ] Complete.')

    @commands.command()
    async def git(self, ctx: commands.Context):
        await ctx.send('https://github.com/XEnophED/TesterBot')

    @commands.command()
    async def psy(self,
                  ctx: commands.Context,
                  member: typing.Optional[discord.Member] = None
                  ):
        if member is not None:
            await ctx.send(' {} gangnam style. '.format(member.mention))
        else:
            await ctx.send(' {} gangnam style. '.format(ctx.author.mention))

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     #if ">" in message.content.lower():
    #         #await message.channel.send(message.content.lower())
    #     #else:
    #     if '558420146733973524' in message.content.lower() and self._talked is 0:
    #         await message.delete()
    #         await message.channel.send('Yes, {}?'.format(message.author))
    #         self._talked = 1
    #         self._progmember = message.author
    #
    #     elif self._progmember is message.author and self._talked is 1:
    #         await message.channel.send(message.content)
    #         self._talked = 0

    # Tester Area for future use
    @commands.command()
    @commands.is_owner()
    async def test_1(self,
                     ctx: commands.Context,
                     *args):
        await ctx.send("{} poops are: {} ".format(len(args), ', '.join(args)))



def setup(bot: commands.Bot):
    logging.info('>>> Setting up [ ping ] ')
    bot.add_cog(Ping(bot))
    logging.info('>>> Done setting up [ ping ] ')
