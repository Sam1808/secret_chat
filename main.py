import asyncio
import aiofiles
import configargparse
import datetime


async def tcp_echo_client(chat_url, chat_port, file_history):
    reader, _ = await asyncio.open_connection(chat_url, chat_port)
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    data = await reader.readline()
    message = f"[{now}] {data.decode()}"
    print(message.strip())

    async with aiofiles.open(file_history, mode='a') as file:
        await file.write(message)

if __name__ == '__main__':
    p = configargparse.ArgParser()
    p.add_argument(
        '--my-config',
        is_config_file=True,
        help='Show my config file (default config.yaml)',
        default='config.yaml'
    )
    p.add_argument('--url', help='Specify chat URL', type=str)
    p.add_argument('--port', help='Specify chat PORT', type=int)
    p.add_argument('--history', help='Specify history filename', type=str)

    options = p.parse_args()

    chat_url = options.url
    chat_port = options.port

    while True:
        asyncio.run(tcp_echo_client(chat_url, chat_port, options.history))

