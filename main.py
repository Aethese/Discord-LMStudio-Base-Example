'''
Minimal Discord bot example for integrating a Discord bot to watch and respond
to messages in a set channel integrating LM Studio
'''

import discord
import os
import lmstudio as lms
from dotenv import load_dotenv
load_dotenv()

TOKEN         = os.getenv('TOKEN')
WATCH_CHANNEL = int(os.getenv('WATCH_CHANNEL_ID'))
SERVER_PORT   = os.getenv('SERVER_PORT')
SERVER_API    = f'localhost:{SERVER_PORT}'
MODEL         = os.getenv('MODEL')
CHAT_LIMIT    = int(os.getenv('CHAT_LIMIT'))
if CHAT_LIMIT % 2 != 0:
	CHAT_LIMIT += 1  # can't work with odd numbers, so will give bot benefit of doubt

# example item: {'role': 'user', text: '...'}
conversation_history = []  # store all convo history, including bot's msgs

# sorry, gotta gatekeep peak
try:
	with open('prompt.txt', 'r') as f:
		INSTRUCTIONS = f.read()
except:  # most likely never created their own prompt.txt
	INSTRUCTIONS = 'respond only in rhymes, and abbreviate every word'  # pls actually create your own prompt.txt

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(
	description='Example Discord bot that integrates with LM Studio', intents=intents
)

@bot.event
async def on_ready():
	await bot.change_presence(
		activity=discord.Activity(type=discord.ActivityType.watching, name=f'{MODEL} 📦')
	)
	print(f'Logged in as {bot.user} and watching channel {WATCH_CHANNEL}')


async def build_chat(user_name: str, question: str) -> lms.Chat:
	global conversation_history  # not really good at bunch of async reads, but fine for example
	chat = lms.Chat(INSTRUCTIONS)

	if len(conversation_history) > CHAT_LIMIT:
		conversation_history = conversation_history[-CHAT_LIMIT:]

	for msg in conversation_history:
		if msg['role'] == 'user':
			chat.add_user_message(msg['text'])
		else:
			chat.add_assistant_response(msg['text'])

	new_qst = f'{user_name}: {question}'
	conversation_history.append({'role': 'user', 'text': new_qst})
	chat.add_user_message(new_qst)

	return chat

@bot.event
async def on_message(msg: discord.Message):
	# only process messages in watch channel and messages sent by users
	if msg.channel.id != WATCH_CHANNEL or msg.author.bot:
		return

	async with msg.channel.typing():
		async with lms.AsyncClient(SERVER_API) as client:
			model = await client.llm.model(MODEL)
			chat = await build_chat(msg.author.name, msg.content)
			result = await model.respond(chat)
			conversation_history.append({'role': 'bot', 'text': result.content})

		await msg.reply(result.content)

bot.run(TOKEN)