import asyncio
import aiofiles
import configargparse
import datetime


async def fetch_chat_messages(chat_url, receive_port, history_filename):
    while True:
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
        '--chat_url',
        help='Specify chat URL (default minechat.dvmn.org)',
        type=str,
        default='minechat.dvmn.org'
    )
    arguments.add_argument(
        '--receive_port',
        help='Specify chat PORT (default 5000)',
        type=int,
        default=5000
    )
    arguments.add_argument(
        '--history_filename',
        help='Specify history filename (default chat_history.txt)',
        type=str,
        default='chat_history.txt'
    )
    return arguments


if __name__ == '__main__':

    parser = get_arguments()
    options = parser.parse_args()

    chat_url = options.chat_url
    receive_port = options.receive_port

    asyncio.run(
        fetch_chat_messages(chat_url, receive_port, options.history_filename)
    )
