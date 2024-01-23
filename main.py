from keep_alive import keep_alive
import discord
import os
from time import sleep
import pytz
from datetime import datetime


channelid = 12345678 #change channelid based on the channel you want the bot to post to

def getTime(): #gets the time, note this is in singapore
  utc_now = datetime.utcnow()

  # Convert the UTC time to the Singapore time zone
  sgt_zone = pytz.timezone('Asia/Singapore')
  sgt_now = utc_now.astimezone(sgt_zone)
      
  # Format the time in AM/PM format
  time_str = sgt_now.strftime("%I:%M:%S %p")
  return time_str
      


def whoalive(list):
  msg = ''
  if list:
    msg += 'Online\n----------\n'
    count = 1
    for member in list:
      msg += '{1}. {0}\n'.format(member,count)
      count+=1
  else:
    msg = 'No members are online.'
  
  return msg



intents = discord.Intents.all()
intents.presences = True


#client = MyClient(intents=intents)
client = discord.Client(intents=intents)

#this code is to check in the terminal if the code is running
@client.event
async def on_ready(): #get the list of currently online people
  print('A tax evader known as {0.user}'.format(client) +' has entered through a portal.')
  
  text_channel = client.get_channel(channelid)
  for member in text_channel.members:
    if ((str(member.status) != "offline") and not member.bot):
        x.append(member)

@client.event
async def on_message(message): #check if the msg is sent by the bot itself
  if message.author == client.user:
    return

  if message.content.startswith('/bmbot'): 
    msg = message.content.split()
    if msg[1] == 'whoalive':
      response = whoalive(x)
      await message.channel.send(response)
    
              

x = [] #this list is here because I had issues with messasges being sent twice when event detected. Also used for summary of whos online (check whoalive function)
@client.event #consider using task like the example given above
async def on_presence_update(before, after):
    channel = client.get_channel(channelid) #find channel to send messasge to.
    activ = after.status
    if ((after.status != before.status)and(str(before.status) == 'offline') and (before not in x) and (str(after.status=='online'))and (not after.bot)): #if user came online
      time_str = getTime()    
      msg = '{0} is now online. The time is {1}'.format(str(before),time_str)
      x.append(before)
      await channel.send(msg)
    elif ((str(after.status) == 'offline') and (before.status != activ) and (before in x) and (str(before.status=='online'))and (not after.bot)): #if user goes offline
      x.remove(before)
      time_str = getTime()
      msg = '{0} is now offline. The time is {1}'.format(str(before),time_str)
      await channel.send(msg)






while __name__ == '__main__':
  try:
    keep_alive()
    client.run(os.environ['token'])
  except discord.errors.HTTPException as e:
    print(e)
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    sleep(7)
    os.system('kill 1')
