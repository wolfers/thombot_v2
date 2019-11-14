from discord.ext import commands
import discord

class moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def role(self, ctx, add_or_remove, role_param):
        roles = {"fighters": 409580553776398347,
                "hunters": 409580657786748928,
                "smoot": 409581784284659712,
                "bring-back-old-torb": 409582089508356106,
                "ubersriek 5": 471467530599399451,
                "minecraft": 499746775436099627,
                "tenno-maggots": 533476718757937152,
                "gmod": 610217420124192802,
                "amaru-mains": 642149050132463616}
        if roles[role_param]:
            role_obj = ctx.guild.get_role(roles[role_param])
            if arg1 == "add":
                    await ctx.author.add_roles(role_obj)
                    return ctx.send("Role successfully added!")
            if arg2 == "remove":
                await ctx.author.remove_roles(role_obj)
                return await ctx.send("Role successfully removed!")
            return await ctx.send("Unable to add role, something went wrong!")
        return await ctx.send("that's not a role!")
            #return error message(wrong arguments or something)

def setup(bot):
    bot.add_cog(moderation(bot))