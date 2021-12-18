from discord import Member, utils

from loader import bot




@bot.command()
async def unmute_user(member: Member):
    role = utils.get(member.guild.roles, id=809817869914341396)

    await member.edit(roles=())
    await member.add_roles(role)
    await member.send('Ты размучен! :)')

