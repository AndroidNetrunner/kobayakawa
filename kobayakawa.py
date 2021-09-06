import asyncio
import discord
import random
from discord import activity
from discord.abc import User
from discord.enums import Status
from discord.ext import commands
from game_data import Game_data, active_game
from start_round import notify_turn, start_round
from ready_game import ready_game
from change import *

token = open("token.txt",
             'r').read()
game = discord.Game("도움말은 $help 입력")
bot = commands.Bot(command_prefix='$',
                   status=discord.Status.online, activity=game)

@bot.command()
async def 시작(ctx):
    if ctx.channel.id in active_game:
        await ctx.send("이미 시작한 게임이 존재합니다.")
        return
    current_game = Game_data()
    active_game[ctx.channel.id] = current_game
    current_game.main_channel = ctx
    current_game.members.append(ctx.message.author)
    current_game.start = True
    current_game.can_join = True
    embed = discord.Embed(title="코바야카와에 오신 것을 환영합니다!", description="코바야카와는 카드 15장으로 즐길 수 있는 간단한 베팅게임입니다.")
    embed.add_field(
        name="참가 방법", value="게임에 참가하고 싶다면 $참가를 입력해주세요.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def 리셋(ctx):
    if ctx.channel.id in active_game:
        del active_game[ctx.channel.id]
        await ctx.send("게임이 초기화되었습니다.")
    else:
        await ctx.send("시작한 게임이 존재하지 않습니다.")

@bot.command()
async def 참가(ctx):
    if ctx.channel.id not in active_game:
        await ctx.send("현재 시작한 게임이 없습니다.")
        return
    current_game = active_game[ctx.channel.id]
    if current_game.can_join == True:
        player = ctx.message.author
        if player not in current_game.members:
            current_game.members.append(player)
            await ctx.send("{}님이 참가하셨습니다. 현재 플레이어 {}명".format(player.name, len(current_game.members)))
        else:
            await ctx.send("{}님은 이미 참가중입니다.".format(player.name))
    else:
        await ctx.send("참가가 이미 마감되었습니다.")

@bot.command()
async def 마감(ctx):
    if ctx.channel.id not in active_game:
        await ctx.send("시작한 게임이 존재하지 않습니다.")
        return
    current_game = active_game[ctx.channel.id]
    if len(current_game.members) < 3:
    	await ctx.send("플레이어 수가 3명 미만입니다. 게임을 시작할 수 없습니다.")
    	return
    if current_game.can_join:
        current_game.can_join = False
        await ctx.send("참가가 마감되었습니다.")
        ready_game(current_game)
        await start_round(current_game)
    else:
        await ctx.send("현재 진행중인 게임이 없습니다.")

@bot.event
async def on_raw_reaction_add(payload):
    current_game = None
    for channel_id in active_game:
        for member in active_game[channel_id].members:
            if payload.user_id == member.id:
                current_game = active_game[channel_id]
                break
    if not current_game:
        return
    current_round = current_game.round_info
    if payload.user_id == current_round.turn.id:
        if str(payload.emoji) == "0\u20E3":
            await draw_hand(current_round)
        elif str(payload.emoji) == "1\u20E3":
            await draw_support_card(current_round)
            await current_game.main_channel.send(f"코바야카와 카드가 {current_round.support_card}로 변경되었습니다.")
        elif str(payload.emoji) == "⭕":
            await change_hand(current_round)
        elif str(payload.emoji) == "❌":
            await keep_hand(current_round)

bot.run(token)