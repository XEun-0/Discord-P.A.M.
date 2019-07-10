from discord.ext import commands
import git

import logging, json

PATH_OF_GIT_REPO = r'.git'
AUTH_INFO = 'owner_info.json'
AUTH_EMAIL = 'email'

class Lily(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._res_path = 'res/'

    # @commands.command()
    # @commands.is_owner()
    # async def git_add(self, ctx: commands.Context):
    #     repo = git.Repo(PATH_OF_GIT_REPO)
    #     repo.git.add(u=True)
    #     repo.git.add('--all')
    #     repo.git.commit('-m', 'c8', author='buttereflay@gmail.com')
    #
    #     origin = repo.remote(name='origin')
    #     origin.push()
    #
    #     logging.info(type(repo))

    @commands.command(aliases=['gitpush'])
    @commands.is_owner()
    async def git_push(self, ctx: commands.Context):
        oe_token = json.load(open(AUTH_INFO, 'r'))[AUTH_EMAIL]
        await ctx.send("```[ Lily ]: Checking git repo...```")
        try:
            repo = git.Repo(PATH_OF_GIT_REPO)
            repo.git.add(update=True)
            repo.git.commit('-m', 'c7', author=oe_token)
            origin = repo.remote(name='origin')
            origin.push()
            await ctx.send('```[ Lily ]: UPDATED: {}```'.format(repo.active_branch))
        except git.GitCommandError as exc:
            await ctx.send('```[ Lily ]: UP-TO-DATE```')

def setup(bot: commands.Bot):
    logging.info('>>> Setting up [ lily ] ')
    bot.add_cog(Lily(bot))
    logging.info('>>> Done setting up [ lily ] ')
