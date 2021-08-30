import asyncio
import aiofiles
import configargparse
import datetime


async def tcp_echo_client(chat_url, receive_port, file_history):
    try:
        reader, _ = await asyncio.open_connection(chat_url, receive_port, )
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        data = await reader.readline()
        message = f"[{now}] {data.decode()}"
        print(message.strip())

        async with aiofiles.open(file_history, mode='a') as file:
            await file.write(message)

    except Exception as err:
        print(f'Error:{err}')


def get_arguments():
    p = configargparse.ArgParser()
    p.add_argument(
        '--my-config',
        is_config_file=True,
        help='Show my config file (default config.yaml)',
        default='config.yaml'
    )
    p.add_argument('--chat_url', help='Specify chat URL', type=str)
    p.add_argument('--send_port', help='Specify chat PORT', type=int)
    p.add_argument('--receive_port', help='Specify chat PORT', type=int)
    p.add_argument('--debug', help='Specify DEBUG mode', type=bool)
    p.add_argument('--token', help='Specify your chat TOKEN', type=str)
    p.add_argument('--history', help='Specify history filename', type=str)
    p.add_argument('--new_user', help='Register new user', type=bool)
    p.add_argument('--my_name', help='Specify your name', type=str)
    return p


if __name__ == '__main__':

    parser = get_arguments()
    options = parser.parse_args()

    chat_url = options.chat_url
    receive_port = options.receive_port

    while True:
        asyncio.run(tcp_echo_client(chat_url, receive_port, options.history))
