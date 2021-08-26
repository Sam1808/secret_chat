import asyncio
import aiofiles
import logging
import json
import os
from receive import get_arguments


async def submit_message(reader, writer, my_message: str):
    writer.write(f"{my_message}\n\n".encode())
    data = await reader.readline()
    logging.debug(data.decode())
    writer.close()


async def register_user(chat_url, send_port, my_name=False):
    reader, writer = await asyncio.open_connection(chat_url, send_port)
    data = await reader.readline()
    logging.debug(data.decode())
    writer.write("\n".encode())
    data = await reader.readline()
    logging.debug(data.decode())
    if my_name:
        writer.write(f"{my_name}\n".encode())
    writer.write("\n".encode())
    data = await reader.readline()
    logging.debug(data.decode())
    writer.close()

    async with aiofiles.open('register_info.txt', mode='w') as file:
        await file.write(data.decode())


async def authorise_user(chat_url, send_port, my_message, token=False):
    if not token:
        async with aiofiles.open('register_info.txt', mode='r') as file:
            register_info = await file.read()
        register_info = json.loads(register_info)
        token = register_info['account_hash']
    token = sanitize_text(token)
    reader, writer = await asyncio.open_connection(chat_url, send_port)
    data = await reader.readline()
    logging.debug(data.decode())
    writer.write(f"{token}\n\n".encode())
    data = await reader.readline()
    if not json.loads(data.decode()):
        logging.debug('Unknown Token. Please check it. ')
    logging.debug(data.decode())

    await submit_message(reader, writer, my_message)


def add_arguments():
    p = get_arguments()
    p.add_argument('--my_message', help='Your message to chat', required=True, type=str)
    return p


def sanitize_text(text):
    return text.encode('utf-8').replace(b'\n', b'').decode('utf-8')


if __name__ == '__main__':

    parser = add_arguments()
    options = parser.parse_args()

    chat_url = options.chat_url
    send_port = options.send_port
    token = options.token
    debug = options.debug
    my_message = sanitize_text(options.my_message)
    my_name = sanitize_text(options.my_name)

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)

    if options.new_user or not os.path.exists('register_info.txt'):
        asyncio.run(register_user(chat_url, send_port, my_name))
    asyncio.run(authorise_user(chat_url, send_port, my_message, token))
