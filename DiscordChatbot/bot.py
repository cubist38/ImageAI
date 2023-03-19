import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTA4NjU0MTA1ODM2OTkxNjk4OA.G3Sin7.aIC24El0oPfRVkccGanwmiVYU2HR8Jr5jSHeg8'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

       
        if len(message.attachments) == 0:
            await message.channel.send('No image found.')
            if user_message[0] == '?':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            elif user_message == 'show':
                with open('demo.jpg', 'rb') as f:
                    picture = discord.File(f)
                    await message.channel.send(file=picture)
            else:
                await send_message(message, user_message, is_private=False)
        else:
            for attachment in message.attachments:
                if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.jpeg') or attachment.filename.endswith('.png'):
                    await attachment.save(attachment.filename)
                    with open(attachment.filename, 'rb') as f:
                        picture = discord.File(f)
                        await message.channel.send(file=picture)
                else:
                    await message.channel.send('Invalid file format. Please upload a JPEG or PNG image.')

    client.run(TOKEN)
