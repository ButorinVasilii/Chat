
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js
import asyncio
chat_msgs = []  # Массив для хранения сообщений чата
online_users = set()  # Задаем список онлайн пользователей
MAX_MESSAGES_COUNT = 100  # Ограничение для количества сообщений в чате

print('тест')
