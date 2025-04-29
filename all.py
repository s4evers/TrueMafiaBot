from telethon import TelegramClient
import asyncio
import time

# Параметры
api_id = 10953300
api_hash = '9c24426e5d6fa1d441913e3906627f87'
bot_username = '@TrueMafiaBot'  # Имя бота
group_id = "-здесь_укажите_ид_группы"  # ID группы
sessions = ['1 имя_сессия', '2 имя_сессия', '3 имя_сессия', '4 имя_сессия']  # Список сессий
session_to_game_name = {
    'имя_сессия': 'имя_профиля',
    'имя_сессия': 'имя_профиля',
    'имя_сессия': 'имя_профиля',
    'имя_профиля': 'имя_профиля'
}
don_game_name = None  # Переменная для имени Дона

# Логирование сообщения
async def log_message(session_name, msg, log_file):
    log_file.write(f"[{session_name}] Message ID: {msg.id}\n")
    log_file.write(f"TEXT: {msg.text}\n")
    if msg.buttons:
        log_file.write("Кнопки:\n")
        for row in msg.buttons:
            for button in row:
                log_file.write(f"  - {button.text}\n")
    else:
        log_file.write("Кнопки отсутствуют\n")
    log_file.write("\n")

# Логика start.py: регистрация аккаунтов
async def process_session(session_name):
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()
    print(f"[{session_name}] Клиент запущен (регистрация).")

    # Ищем сообщение с регистрацией
    async for msg in client.iter_messages(group_id, limit=100):
        if msg.text and "Ro'yxatdan o'tish boshlandi" in msg.text:
            print(f"\n[{session_name}] Найдено сообщение регистрации:")
            print(f"ID: {msg.id}\n")
            print("TEXT:\n", msg.text)

            # Получаем inline-кнопки
            if msg.buttons:
                print(f"[{session_name}] Найдено {len(msg.buttons)} кнопок.")
                for row in msg.buttons:
                    for button in row:
                        print(f"Кнопка: {button.text}")
                        if button.url:
                            link = button.url
                            print(f"Ссылка: {link}")
                            start_param = link.split("start=")[1]
                            print(f"Параметр для start: {start_param}")
                            await client.send_message(bot_username, f'/start {start_param}')
                            print(f"[{session_name}] Команда /start с параметром отправлена боту.")
                            break
            else:
                print(f"[{session_name}] Кнопок не найдено.")
            break
    await client.disconnect()

# Логика run.py: проверка ролей
async def check_messages_for_session(client, session_name):
    global don_game_name
    print(f"[{session_name}] Клиент запущен (проверка ролей).")

    async for msg in client.iter_messages(bot_username, limit=1):
        if not msg.text:
            print(f"[{session_name}] Сообщение без текста.")
            return None, False

        print(f"[{session_name}] Последнее сообщение от бота:")
        print(f"TEXT: {msg.text}")
        
        with open("log.txt", "a") as log_file:
            await log_message(session_name, msg, log_file)

        if "Siz- 🕵️‍ Komissar Katani!" in msg.text or "Xarakat qilish vaqti keldi!" in msg.text:
            print(f"[{session_name}] Персонаж — Комиссар! Ожидание целевого сообщения...")
            return "Komissar", True
        elif "Siz- 🤵🏻 Donsiz (Mafia sardori)!" in msg.text or "Mafia keyingi qurboni uchun ovoz berish o'tkazyapti:" in msg.text:
            print(f"[{session_name}] Персонаж — Дон!")
            don_game_name = session_to_game_name[session_name]
            print(f"[{session_name}] Игровое имя Дона: {don_game_name}")
            return "Don", False
        else:
            print(f"[{session_name}] Персонаж не Комиссар и не Дон.")
            return None, False

# Логика run.py: действия Комиссара
async def handle_komissar(client, session_name):
    global don_game_name
    print(f"[{session_name}] Обработка действий Комиссара...")

    for _ in range(12):  # 60 секунд, каждые 5 секунд
        async for msg in client.iter_messages(bot_username, limit=1):
            if msg.text and "Xarakat qilish vaqti keldi!" in msg.text:
                print(f"[{session_name}] Найдено целевое сообщение:")
                print(f"TEXT: {msg.text}")
                
                with open("log.txt", "a") as log_file:
                    await log_message(session_name, msg, log_file)

                if msg.buttons and len(msg.buttons) >= 2:
                    print(f"[{session_name}] Найдены кнопки:")
                    for row in msg.buttons:
                        for button in row:
                            print(f"  - {button.text}")

                    msg_id = msg.id
                    print(f"[{session_name}] ID сообщения: {msg_id}")

                    second_button = msg.buttons[1][0]
                    print(f"[{session_name}] Нажимаем вторую кнопку: {second_button.text}")
                    await second_button.click()
                    
                    print(f"[{session_name}] Ожидание 1 секунды...")
                    await asyncio.sleep(1)
                    print(f"[{session_name}] Ожидание дополнительных 2 секунд...")
                    await asyncio.sleep(2)
                    
                    updated_msg = await client.get_messages(bot_username, ids=msg_id)
                    if updated_msg and updated_msg.buttons:
                        print(f"[{session_name}] Обновлённое сообщение:")
                        print(f"TEXT: {updated_msg.text}")
                        
                        with open("log.txt", "a") as log_file:
                            await log_message(session_name, updated_msg, log_file)
                        
                        print(f"[{session_name}] Найдены кнопки для выбора жертвы:")
                        for row in updated_msg.buttons:
                            for button in row:
                                print(f"  - {button.text}")
                        
                        if don_game_name:
                            for row in updated_msg.buttons:
                                for button in row:
                                    print(f"[{session_name}] Проверяем кнопку: {button.text}")
                                    if button.text == don_game_name:
                                        print(f"[{session_name}] Нажимаем кнопку: {button.text}")
                                        await button.click()
                                        return True
                            print(f"[{session_name}] Дон {don_game_name} не найден в кнопках.")
                        else:
                            print(f"[{session_name}] Дон не определён.")
                        return False
                    else:
                        print(f"[{session_name}] Обновлённое сообщение не содержит кнопок.")
                        return False
                
                else:
                    print(f"[{session_name}] Недостаточно кнопок или кнопки отсутствуют.")
                    return False
        
        print(f"[{session_name}] Ожидание 5 секунд перед следующей проверкой...")
        await asyncio.sleep(5)
    
    print(f"[{session_name}] Целевое сообщение не найдено за 60 секунд.")
    return False

# Основная функция
async def main():
    global don_game_name

    # Шаг 1: Отправка /game от mi
    mi_client = TelegramClient('mi', api_id, api_hash)
    await mi_client.start()
    print("[mi] Отправляем команду /game в группу...")
    await mi_client.send_message(group_id, '/game')
    await mi_client.disconnect()
    
    # Ожидание 1 секунды
    print("Ожидание 1 секунды перед регистрацией...")
    time.sleep(1)

    # Шаг 2: Логика start.py (регистрация всех аккаунтов)
    print("Запуск регистрации аккаунтов...")
    tasks = [process_session(session) for session in sessions]
    await asyncio.gather(*tasks)

    # Шаг 3: Отправка /start от mi
    mi_client = TelegramClient('mi', api_id, api_hash)
    await mi_client.start()
    print("[mi] Отправляем команду /start в группу...")
    await mi_client.send_message(group_id, '/start')
    await mi_client.disconnect()
    
    # Ожидание 1 секунды
    print("Ожидание 1 секунды перед запуском run.py...")
    time.sleep(1)

    # Шаг 4: Логика run.py (проверка ролей и действия Комиссара)
    print("Запуск проверки ролей и действий Комиссара...")
    komissar_session = None
    clients_to_disconnect = []  # Список клиентов для отключения

    for session_name in sessions:
        print(f"\nПроверка сессии: {session_name}")
        client = TelegramClient(session_name, api_id, api_hash)
        await client.start()  # Запускаем клиент
        role, should_process = await check_messages_for_session(client, session_name)
        
        if role == "Komissar":
            komissar_session = (client, session_name)
        elif role == "Don":
            clients_to_disconnect.append(client)  # Добавляем для отключения
        else:
            clients_to_disconnect.append(client)  # Добавляем для отключения

    if komissar_session:
        client, session_name = komissar_session
        success = await handle_komissar(client, session_name)
        if success:
            print(f"[{session_name}] Действия Комиссара успешно выполнены.")
        else:
            print(f"[{session_name}] Не удалось выполнить действия Комиссара.")
        clients_to_disconnect.append(client)  # Добавляем Комиссара для отключения после действий
    else:
        print("Комиссар не найден среди аккаунтов.")

    # Отключаем все клиенты
    for client in clients_to_disconnect:
        await client.disconnect()

    if not don_game_name:
        print("Дон не найден среди аккаунтов.")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
