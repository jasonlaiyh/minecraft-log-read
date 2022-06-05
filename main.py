# TODO : Using monitors, run the py file every 25 or so minutes
# TODO : use reactions on the bot's own (last) message, if it detects a reaction, update the logs. import discord
from webserver import keep_alive
import discord
import os
import requests
botToken = os.environ['botToken']

client = discord.Client()

@client.event
async def on_ready():
  print('Friend {0.user} is now logged in'.format(client))

# initialise variables
SERVER = os.environ['SERVER_URL']
directory = 'log.txt'
first_half = []
timestamp =[]
second_half = []
split_text2 = []
pop_flag = False
write_flag = False
i = 0
idx = 0

# warnings/logs to be filtered out
filteredWords = ['UUID',
                'uuid',
                'entity',
                'EntityVillager',
                'authlib',
                'voicechat',
                'Server thread/WARN']


def read_internal_logs(bot_log):
  global write_flag
  with open(directory) as file:
    log_list = file.readlines()
    bot_log_formatted = f'{bot_log}\n'

# If not in internal log, write to it. Else, do nothing.
  if bot_log_formatted not in log_list:
    write_to_logs(bot_log)
    # if write_flag is True:
      
    #   write_flag = False
    

      
def write_to_logs(bot_log):
  global write_flag
  with open(directory, mode='a') as file:
    file.write(f'{bot_log}\n')
    write_flag = True



@client.event
async def on_message(message):
  if message.author == client.user:
    return
  elif message.content.startswith('!hi') :
    await message.channel.send('Hi friend!')
  elif message.content.startswith('!checkLogs'):
    global i
    global idx
    
    # request logs
    response = requests.get(url=SERVER)
    text = response.text
    i = 0
    idx = 0
    # get rid of newline
    split_text=text.split('\n')
    
    # filtering
    for ind in range(len(filteredWords)):
      split_text = [item for item in split_text if filteredWords[ind] not in item]
    
    # split resulting text into two parts (timestamps and chat)
    for entry in split_text:
      split_text2.append(entry.split(']:'))
      
    while i < len(split_text2)-1: 
      first_half.append(split_text2[i][0])
      second_half.append(split_text2[i][1])
      timestamp.append(first_half[i].split(']')[0][1:])      
      i +=1
    
    
    while idx < len(timestamp):
      
      # initialise local variables
      player = ''
      j = 1
      title = ''
      chat = ''
      # check for game joins
      if 'join' in second_half[idx]:
        while second_half[idx][j] != ' ':
          player += second_half[idx][j]
          j +=1
        bot_log = f'{timestamp[idx]} ::: {player} is back online!'
        await message.channel.send(bot_log)
        read_internal_logs(bot_log)
        pop_flag = True
        
      # check for sleeping
      elif 'is now sleeping, 1 out of 1 needed' in second_half[idx]:
        while second_half[idx][j] != ' ':
          player += second_half[idx][j]
          j +=1
        bot_log = f'{timestamp[idx]} ::: {player} slept! Another sus-less night'
        await message.channel.send(bot_log)
        read_internal_logs(bot_log)
        pop_flag = True
    
      #check for disconnections
      elif 'lost connection: Disconnected' in second_half[idx]:
        while second_half[idx][j] != ' ':
          player += second_half[idx][j]
          j +=1
        bot_log = f'{timestamp[idx]} ::: {player} dc-ed! RIP Internet'
        await message.channel.send(bot_log)
        read_internal_logs(bot_log)
        pop_flag = True  
    
      # check for advancements
      elif 'advancement' in second_half[idx]:
        while second_half[idx][j] != ' ':
          player += second_half[idx][j]
          j +=1
        while second_half[idx][j] != '[':
          j +=1
        while second_half[idx][j] != ']':
          title += second_half[idx][j]
          j +=1
        title += second_half[idx][j]
        bot_log = f'{timestamp[idx]} ::: {player} did a thing! Achieved {title}! POG'
        await message.channel.send(bot_log)
        read_internal_logs(bot_log)
        pop_flag = True
    
    
    # 
    # add death messages
        
    # chat receipts
      elif 'Async Chat Thread' in first_half[idx]:
        while second_half[idx][j] != '<':
          j +=1
        while second_half[idx][j] != '>':
          player += second_half[idx][j]
          j +=1
        chat = second_half[idx][j+1:]
        player = player[1:] 
        bot_log = f'{timestamp[idx]} ::: {player} :"{chat} "'
        await message.channel.send(bot_log)
        read_internal_logs(bot_log)
        pop_flag = True
        
      if pop_flag is True:
        first_half.pop(idx)
        second_half.pop(idx)
        timestamp.pop(idx)
      else:
        idx += 1
    first_half.clear()
    timestamp.clear()
    second_half.clear()
    split_text2.clear()
  
keep_alive()  
client.run(botToken)

