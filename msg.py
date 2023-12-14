
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import asyncio
chat = []  # Массив для хранения сообщений чата
online_users = set()  # Задаем список онлайн пользователей
MAX_MSG = 50  # Ограничение для количества сообщений в чате

async def main():
    global chat
    put_markdown('# Убийца телеграмма')

    msg = output()
    put_scrollable(msg, height=500, keep_bottom=True)

    login = await input("Войти", required=True)
    online_users.add(login)

    chat.append(('>>', f'`{login}` вошёл(а) в чат'))
    msg.append(put_markdown(f'`{login}` войшёл(а) в чат'))

    refresh_task = run_async(refresh_msg(login, msg))

    while True:
        data = await input_group('Новое сообщение', [
            input(placeholder='Текст ...', name="rep"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate = lambda m: ('rep', 'Введите') if m["cmd"] == "Отправить" and not m['rep'] else None)

        if data is None:
            break

        msg.append(put_markdown(f"`{login}`: {data['rep']}"))
        chat.append((login, data['rep']))

    refresh_task.close()

    online_users.remove(login)
    toast('Вышли')
    msg.append(put_markdown(f'`{login}` вышел'))
    chat.append(( f'`{login}`вышел'))

    put_buttons(['Зайти снова'], onclick=lambda btn:run_js('window.location.reload()'))

async def refresh_msg(login, msg):
    global chat
    last_idx = len(chat)

    while True:
        await asyncio.sleep(1)
        
        for m in chat[last_idx:]:
            if m[0] != login: 
                msg.append(put_markdown(f"`{m[0]}`: {m[1]}"))
        
        if len(chat) > MAX_MSG:
            chat = chat[len(chat) // 2:]
        
        last_idx = len(chat)

if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)     
