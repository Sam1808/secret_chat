import asyncio


async def tcp_echo_client(chat_url, chat_port):
    reader, _ = await asyncio.open_connection(chat_url, chat_port)

    data = await reader.readline()
    print(data.decode())

if __name__ == '__main__':
    chat_url = 'minechat.dvmn.org'
    chat_port = 5000

    while True:
        asyncio.run(tcp_echo_client(chat_url, chat_port))

