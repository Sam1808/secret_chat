import asyncio
import aiofiles
import logging
import json
import os
from receive import get_arguments


async def submit_message(reader, writer, message: str):
    writer.write(f"{message}\n\n".encode())
    data = await reader.readline()
    logging.debug(data.decode())
    writer.close()


async def register_user(chat_url, send_port, name=None):
    reader, writer = await asyncio.open_connection(chat_url, send_port)
    data = await reader.readline()
    logging.debug(data.decode())
    writer.write("\n".encode())
    data = await reader.readline()
    logging.debug(data.decode())
    if name:
        writer.write(f"{name}\n".encode())
    writer.write("\n".encode())
    data = await reader.readline()
    logging.debug(data.decode())
    writer.close()

    async with aiofiles.open('register_info.txt', mode='w') as file:
        await file.write(data.decode())


async def authorise_user(chat_url, send_port, message, token=False):
    if not token:
        async with aiofiles.open('register_info.txt', mode='r') as file:
            register_raw_data = await file.read()
        register_info = json.loads(register_raw_data)
        token = register_info['account_hash']
    reader, writer = await asyncio.open_connection(chat_url, send_port)
    data = await reader.readline()
    logging.debug(data.decode())
    writer.write(f"{token}\n\n".encode())
    data = await reader.readline()
    if not json.loads(data.decode()):
        logging.debug('Unknown Token. Please check it. ')
        writer.close()
        return logging.debug(data.decode())

    await submit_message(reader, writer, message)


def add_arguments():
    p = get_arguments()
    p.add_argument('--message', help='Your message to chat', required=True, type=str)
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
    message = sanitize_text(options.message)
    name = sanitize_text(options.name)

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)

    if options.new_user or not os.path.exists('register_info.txt'):
        asyncio.run(register_user(chat_url, send_port, name))
    asyncio.run(authorise_user(chat_url, send_port, message, token))
