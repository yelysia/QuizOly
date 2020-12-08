import discord
from discord.ext import commands, tasks
import os
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import keep_alive


# https://pythondiscord.com/pages/resources/guides/discordpy/
# discord.py documentation: https://discordpy.readthedocs.io/en/latest/

# gspread documentation/reference: https://gspread.readthedocs.io/en/latest/

key=os.getenv('key')
wkey=os.getenv('wkey')

client = commands.Bot(command_prefix = '!', help_command = None)


# if users choose, they can start their own bot application, fork this repl, create their own bot using that forked code,  change this string to the name of their own spreadsheet, and change the necessary discord bot tokens etc.
SPREADSHEET_NAME = "Nucleotide Hackathon question compilation"




######## events #######

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('nothing')) #or discord.Status.idle
  print('Ready')
  global row








########### commands ###########

@client.command(aliases=['latency'])
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency*1000)}ms')

# test command
@client.command(aliases=['test'])
async def nameofcommand(ctx):
  await ctx.send('message')

# help command
@client.command(aliases=['h'])
async def help(ctx):
  await ctx.send('```HELP PAGE\n\n !question or !q - Provides a random question for the user to respond to\n\n !check [question #] [answer] - checks whether the answer is correct or not, posts the questions difficulty and gives resources for the question.\n\n !ping - checks ping \n\n !help or !h - shows this message \n\n !info or !i - Gives useful links regarding Science Olympiad```')

# info command
@client.command(aliases=['i'])
async def info(ctx, *args):
  ## TODO: add the optional event argument  thing
  await ctx.send('Scioly Wiki which gives a general understanding of certain event\nhttps://scioly.org/wiki/index.php/Designer_Genes\n\n SciOly Rule Sheet which gives info on every event and what is tested:\n  http://api-static.ctlglobalsolutions.com/science/Science_Olympiad_Div_C_Rules_2021_for_Web.pdf')


# get a random question
@client.command(aliases=['q'])
async def question(ctx):
  # scope of accessing google sheet stuff 
  # THIS NEEDS TO BE PASTED IN EVERY RELEVANT COMMAND DEFINITION why :C
  scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
  creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
  gc = gspread.authorize(creds)
  sheet = gc.open(SPREADSHEET_NAME).sheet1
  
  row = random.randint(2,57) # randomly select a row that isn't the column headers
  prompt = sheet.cell(row, 4).value # reference prompt if applicable
  question = sheet.cell(row, 5).value # next column
  source = sheet.cell(row, 10).value
  
  # store row in some kind of other database?
  #for now maybe we can make it send the row number, then you in the server are supposed to do !answer [row] and then the bot passes row as an argument as in answer(ctx, row)
  await ctx.send(f'{prompt}\n```{question}\nQuestion ID: {row}\n*Source: {source}*```')


#user checks their answer (for now must input the row number for question as an argument)
@client.command(aliases=['c'])
async def check(ctx, row, *, check):
  scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
  creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
  gc = gspread.authorize(creds)
  sheet = gc.open(SPREADSHEET_NAME).sheet1
  
  answer = sheet.cell(row, 6).value
  qtype = sheet.cell(row, 3)
  resource1 = sheet.cell(row, 7).value
  resource2 = sheet.cell(row, 8).value
  studyguide = sheet.cell(row, 9).value
  difficulty = sheet.cell(row, 11).value
  
  if( qtype == 'LA' ):
    await ctx.send(f'Answers may vary. {answer}')

  if( answer.casefold() != check.casefold() ):
    await ctx.send(f'```Incorrect. The correct answer is {answer}.\nQuestion difficulty: {difficulty}```\n__Here is some extra information:__\n{resource1}\n{resource2}\nStudy guide section: {studyguide}')
  else:
    await ctx.send(f'```Correct!\nQuestion difficulty: {difficulty}```\n__Here is some extra information:__\n{resource1}\n{resource2}\n{studyguide}')    



@client.command(aliases=['s'])
async def skip(ctx, row):
  scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
  creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
  gc = gspread.authorize(creds)
  sheet = gc.open(SPREADSHEET_NAME).sheet1
  
  answer = sheet.cell(row, 6).value
  resource1 = sheet.cell(row, 7).value
  resource2 = sheet.cell(row, 8).value
  studyguide = sheet.cell(row, 9).value
  difficulty = sheet.cell(row, 11).value 
  await ctx.send(f'```The correct answer is {answer}.\nQuestion difficulty: {difficulty}```\n__Here is some extra information:__\n{resource1}\n{resource2}\nStudy guide section: {studyguide}')





keep_alive.keep_alive()   # for web server bot hosting 

client.run(os.getenv('TOKEN'))