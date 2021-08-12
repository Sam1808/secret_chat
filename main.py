import asyncio
import aiofiles
import datetime


async def tcp_echo_client(chat_url, chat_port):
    reader, _ = await asyncio.open_connection(chat_url, chat_port)
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    data = await reader.readline()
    message = f"[{now}] {data.decode()}"
    print(message.strip())

    async with aiofiles.open('chat_history.txt', mode='a') as file:
        await file.write(message)

if __name__ == '__main__':
    chat_url = 'minechat.dvmn.org'
    chat_port = 5000

    while True:
        asyncio.run(tcp_echo_client(chat_url, chat_port))

