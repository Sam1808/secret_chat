import asyncio
import aiofiles
import configargparse
import datetime


async def fetch_chat_messages(chat_url, receive_port, history_filename):
    try:
        reader, _ = await asyncio.open_connection(chat_url, receive_port,)
        encoded_message = await reader.readline()
        now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        message = f'[{now}] {encoded_message.decode()}'
        print(message.strip())

        async with aiofiles.open(history_filename, mode='a') as file:
            await file.write(message)

    except Exception as err:
        print(f'Error:{err}')


def get_arguments():
    arguments = configargparse.ArgParser()
    arguments.add_argument(
        '--config',
        is_config_file=True,
        help='Show config file (default config.yaml)',
        default='config.yaml'
    )
    arguments.add_argument('--chat_url', help='Specify chat URL', type=str)
    arguments.add_argument('--send_port', help='Specify chat PORT', type=int)
    arguments.add_argument('--receive_port', help='Specify chat PORT', type=int)
    arguments.add_argument('--debug', help='Specify DEBUG mode', type=bool)
    arguments.add_argument('--token', help='Specify your chat TOKEN', type=str)
    arguments.add_argument('--history_filename', help='Specify history filename', type=str)
    arguments.add_argument('--new_user', help='Register new user', type=bool)
    arguments.add_argument('--name', help='Specify your name', type=str)
    return arguments


if __name__ == '__main__':

    parser = get_arguments()
    options = parser.parse_args()

    chat_url = options.chat_url
    receive_port = options.receive_port

    while True:
        asyncio.run(fetch_chat_messages(chat_url, receive_port, options.history_filename))
