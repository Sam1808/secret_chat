import asyncio

import configargparse


async def tcp_echo_client(chat_url, chat_port, token, my_message: str):
    reader, writer = await asyncio.open_connection(chat_url, chat_port)
    writer.write(f"{token}\n\n".encode())
    writer.write(f"{my_message}\n\n".encode())
    writer.close()


if __name__ == '__main__':
    p = configargparse.ArgParser()
    p.add_argument(
        '--my-config',
        is_config_file=True,
        help='Show my config file (default config.yaml)',
        default='config.yaml'
    )
    p.add_argument('--url', help='Specify chat URL', type=str)
    p.add_argument('--send_port', help='Specify chat PORT', type=int)
    p.add_argument('--token', help='Specify your chat TOKEN', type=str)
    p.add_argument('--receive_port', help='Specify chat PORT', type=int)
    p.add_argument('--history', help='Specify history filename', type=str)

    options = p.parse_args()

    chat_url = options.url
    chat_port = options.send_port
    chat_token = options.token

    message = '!Test.!Test.!Test.'

    # while True:
    asyncio.run(tcp_echo_client(chat_url, chat_port, chat_token, message))

