import requests
import os


# initialise variables
SERVER = os.environ['SERVER_URL']
directory = 'log.txt'
first_half = []
timestamp =[]
second_half = []
split_text2 = []
pop_flag = False
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
  with open(directory) as file:
    log_list = file.readlines()
    bot_log_formatted = f'{bot_log}\n'

# If not in internal log, write to it. Else, do nothing.
  if bot_log_formatted not in log_list:
    write_to_logs(bot_log)    

      
def write_to_logs(bot_log):
  with open(directory, mode='a') as file:
    file.write(f'{bot_log}\n')

# request logs
response = requests.get(url=SERVER)
text = response.text

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
  char = ''
  j = 1
  title = ''
  
  # check for game joins
  if 'join' in second_half[idx]:
    while second_half[idx][j] != ' ':
      char += second_half[idx][j]
      j +=1
    bot_log = f'{timestamp[idx]} : {char} is back online!'
    read_internal_logs(bot_log)
    pop_flag = True
    
  # check for sleeping
  elif 'is now sleeping, 1 out of 1 needed' in second_half[idx]:
    while second_half[idx][j] != ' ':
      char += second_half[idx][j]
      j +=1
    bot_log = f'{timestamp[idx]} : {char} slept! Another sus-less night'
    read_internal_logs(bot_log)
    pop_flag = True

  # check for advancements
  elif 'advancement' in second_half[idx]:
    while second_half[idx][j] != ' ':
      char += second_half[idx][j]
      j +=1
    while second_half[idx][j] != '[':
      j +=1
    while second_half[idx][j] != ']':
      title += second_half[idx][j]
      j +=1
    title += second_half[idx][j]
    bot_log = f'{timestamp[idx]} : {char} did a thing! Achieved {title}! POG'
    read_internal_logs(bot_log)
    pop_flag = True
  if pop_flag is True:
    second_half.pop(idx)
    timestamp.pop(idx)
  else:
    idx += 1
